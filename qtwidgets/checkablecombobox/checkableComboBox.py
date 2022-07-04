from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QMenu, QListView, QTreeView
from PyQt5.QtGui import QStandardItemModel, QMouseEvent, QStandardItem, QCloseEvent
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, pyqtProperty
import sys





class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# class FieldDataCode(metaclass=Singleton):
class PlaceholderIdCode:
    code = 12011983

class ComboListView(QListView):
    RIGHT = pyqtSignal(QPoint)
    DELETE = pyqtSignal(int)

    def __init__(self, parent=None):
        super(ComboListView, self).__init__(parent)
        self.RIGHT.connect(self.showMenu)

    def showMenu(self, pos):
        menu = QMenu()
        clear_action = menu.addAction("Delete", self.delete_item)
        action = menu.exec_(self.mapToGlobal(pos))

    def delete_item(self):
        self.DELETE.emit(self.currentIndex().row())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            super(ComboListView, self).mousePressEvent(event)
        elif event.button() == Qt.RightButton:
            self.RIGHT.emit(event.pos())



# creating checkable combo box class
class CheckableComboBox_ABS(QComboBox):
    CHECKED_ITEMS_READY = pyqtSignal(list)
    DELETE = pyqtSignal(int)

    def __init__(self, parent):
        try:
            import pydevd_pycharm

            pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        except Exception as error:
            print(f'Warning the debugger in not loaded:: {error}')
        super(CheckableComboBox_ABS, self).__init__(parent)
        # self.view().mousePressEvent.connect(self.handle_item_pressed)
        self.list_view = ComboListView
        self.placeholders_id_code = PlaceholderIdCode()
        self.setView(self.list_view())
        self.view().pressed.connect(self.handle_item_pressed)
        self.view().DELETE.connect(lambda x: self.DELETE.emit(x))
        self.setModel(QStandardItemModel(self))
        self._changed = True
        self.checkedItems = []
        self.setDuplicatesEnabled(False)
        self.setInsertPolicy(self.InsertAtTop)
        self._selection_is_present = ''
        self._selection_is_not_present = ''
        self._no_columns = 'No colums'
        self._placeholder_is_inserted = False
        self.map_cat_id = {}


    @pyqtProperty(str)
    def selection_is_present(self):
        return self._selection_is_present

    @selection_is_present.setter
    def selection_is_present(self, value):
        self._selection_is_present = value
        self.insert_placeholder()

    @pyqtProperty(str)
    def no_available_field_text(self):
        return self._no_columns

    @no_available_field_text.setter
    def no_available_field_text(self, value):
        self._no_columns = value


    @pyqtProperty(str)
    def selection_is_not_present(self):
        return self._selection_is_not_present

    @selection_is_not_present.setter
    def selection_is_not_present(self, value):

        self._selection_is_not_present = value
        self.insert_placeholder()

    def get_all_checked(self):
        return self.checkedItems

    # def clear(self) -> None:
    #     super(CheckableComboBox_ABS, self).clear()
    #     self._placeholder_is_inserted = False
    #     self.insert_placeholder()

    def insert_placeholder(self):
        if not self._placeholder_is_inserted:
            if not self.count():
                placeholder = self._no_columns
            elif not self.checkedItems:
                placeholder = self._selection_is_not_present
            else:
                placeholder = self._selection_is_present
            if placeholder is not None:
                self.addItem(placeholder, self.placeholders_id_code)
                self._placeholder_is_inserted = True
            self.setCurrentIndex(self.count() - 1 if self.count() > 0 else 0)


    def remove_placeholders(self):
        row = self.findData(self.placeholders_id_code)
        while row != -1:  # ritorna indice del primo rigo che trova, se non trova -1 usare un while
            self.removeItem(row)
            row = self.findData(self.placeholders_id_code)
        self._placeholder_is_inserted = False

    def hidePopup(self):
        if not self._changed:
            self.insert_placeholder()
            super(CheckableComboBox_ABS, self).hidePopup()
            self.check_items()
            # self.CHECKED_ITEMS_READY.emit([item.text() for item in self.checkedItems])
            self.CHECKED_ITEMS_READY.emit(self.checkedItems)
        self._changed = False

    def closeEvent(self, a0: QCloseEvent) -> None:
        self._changed = True # porcaround per non far triggerare hidePopup
        a0.accept()

    def showPopup(self) -> None:
        self.remove_placeholders()
        super(CheckableComboBox_ABS, self).showPopup()
        if not self.count():
            self.insert_placeholder()


    # when any item get pressed
    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)
        # make it check if unchecked and vice-versa
        state = not item.checkState()
        item.setCheckState(state)
        # calling method
        self.check_items()
        if self.checkedItems and not state:
                last_checked = self.checkedItems[-1]
                self.setCurrentIndex(last_checked.index().row())
        self._changed = True

    def unselect_all(self):
        checked_items_num = len(self.checkedItems)
        for x in range(checked_items_num):
            item = self.checkedItems.pop()
            item.setCheckState(False)
        self.remove_placeholders()
        self.insert_placeholder()

    def get_checked_items(self):
        return self.check_items()

    # method called by check_items
    def item_checked(self, index):
        item = self.model().item(index, 0)
        if item.text() != self._selection_is_present and item.text() != self._selection_is_not_present:
            state = item.checkState()
            return state
        else:
            return False

    def get_item_from_str(self, label):
        index = self.findText(label)
        if index != -1:
            return self.model().item(index, 0)
        else:
            return None

    def convert_str_list_to_items(self, str_list):
        _str_list = list()
        for element in str_list:
            if not isinstance(element, QStandardItem):
                if isinstance(element, str):
                    item = self.get_item_from_str(element)
                    if item:
                        _str_list.append(item)
                    else:
                        print(f'warning - update checked tags failed - {element}')
                else:
                    print(f'warning - update checked tags failed - {element}')
            else:
                _str_list.append(element)
        return _str_list

    def set_checked_items(self, checked:list):
        checked = self.convert_str_list_to_items(checked)
        self.checkedItems.clear()
        for i in range(self.count()):
            item = self.model().item(i, 0)
            if item in checked:
                checked.pop()
                item.setCheckState(True)
                self.checkedItems.append(item)
            else:
                item.setCheckState(False)
        self.remove_placeholders()
        self.insert_placeholder()

    # calling method
    def check_items(self):
        # blank list
        self.checkedItems.clear()
        # traversing the items
        for i in range(self.count()):
            # if item is checked add it to the list
            if self.item_checked(i):
                self.checkedItems.append(self.model().item(i, 0))
        return self.checkedItems

    def addItem(self, text: str, data) -> None:
        if self._placeholder_is_inserted and self.count() == 1: # nel caso iniziale in cui sono presettatti degli items
            self.remove_placeholders()
        return super(CheckableComboBox_ABS, self).addItem(text, data)


    def addItems(self, items_text, already_selected) -> None:
        self.clear()
        # already_selected = [tag.category_obj.name for tag in already_selected]

        for item_text in items_text:
            if isinstance(item_text, str):
                data = items_text
            else:
                item_text, data = item_text.name, item_text
            super(CheckableComboBox_ABS, self).addItem(item_text, data)
        rows = self.count()
        for row in range(rows):
            item = self.model().item(row, 0)
            item_data = item.data()
            if item_data != self.placeholders_id_code:
                if item.text() not in already_selected :
                    item.setCheckState(False)
                else:
                    item.setCheckState(True)
        self.remove_placeholders()
        self.insert_placeholder()
        self.check_items()

class CheckableComboBox(CheckableComboBox_ABS):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.showMenu)
        self.selection_is_present = 'Visible Fields'
        self.selection_is_not_present = 'Selected Fields'
        # test
        items = [f'test {x} ' for x in range(9)]
        already_selected = list(filter(lambda x: items.index(x) % 2 == 0, items))
        self.addItems(items, already_selected)
        # end test






