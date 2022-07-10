from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QMenu, QListView, QTreeView
from PyQt5.QtGui import QStandardItemModel, QMouseEvent, QStandardItem, QCloseEvent, QHideEvent, QShowEvent
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, pyqtProperty, QTimer
import sys

class PlaceholderIdCode:
    code = 12011983

class ComboListView(QListView):
    RIGHT = pyqtSignal(QPoint)
    DELETE = pyqtSignal(int)

    def __init__(self, parent=None, combo = None):
        super(ComboListView, self).__init__(parent)
        self.RIGHT.connect(self.showMenu)
        self.combo = combo

    def showMenu(self, pos):
        menu = QMenu()
        clear_action = menu.addAction("Delete", self.delete_item)
        action = menu.exec_(self.mapToGlobal(pos))

    def delete_item(self):
        self.DELETE.emit(self.currentIndex().row())

    def mousePressEvent(self, event: QMouseEvent):

        if event.button() == Qt.LeftButton:
            # item = self.model()
            super(ComboListView, self).mousePressEvent(event)
        elif event.button() == Qt.RightButton:
            self.RIGHT.emit(event.pos())
        else:
            print(event.type())

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        return

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        # porkaround to avoid weird change of the index
        super(ComboListView, self).mouseDoubleClickEvent(e)
        QTimer.singleShot(100, self._update_parent_placeholder)

    def _update_parent_placeholder(self):
        parent: CheckableComboBox_ABS = self.combo
        if parent:
            parent.update_placeholder()
        parent._changed = False

    def showEvent(self, a0: QShowEvent) -> None:
        parent: CheckableComboBox_ABS = self.combo
        if parent:
            parent.remove_placeholders()
        super(ComboListView, self).showEvent(a0)

    def hideEvent(self, a0: QHideEvent) -> None:
        parent: CheckableComboBox_ABS = self.combo
        if parent:
            parent.insert_placeholder()
        super(ComboListView, self).hideEvent(a0)



# creating checkable combo box class
class CheckableComboBox_ABS(QComboBox):
    CHECKED_ITEMS_READY = pyqtSignal(list)
    DELETE = pyqtSignal(int)

    def __init__(self, parent):
        # try:
        #     import pydevd_pycharm
        #
        #     pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        # except Exception as error:
        #     print(f'Warning the debugger in not loaded:: {error}')
        super(CheckableComboBox_ABS, self).__init__(parent)
        # self.view().mousePressEvent.connect(self.handle_item_pressed)
        self.list_view = ComboListView
        self.placeholders_id_code = PlaceholderIdCode()
        self.setView(self.list_view(combo=self))
        self.view().pressed.connect(self.handle_item_pressed)
        # self.view().DELETE.connect(lambda x: self.DELETE.emit(x))
        self.setModel(QStandardItemModel(self))
        # self.setModel(CustomItemModel(self))
        self._changed = True
        self._checkedItems = []
        self.setDuplicatesEnabled(False)
        self.setInsertPolicy(self.InsertAtTop)
        self._selection_is_present = ''
        self._selection_is_not_present = ''
        self._no_columns = 'No colums'
        self.map_cat_id = {}


    @property
    def checkedItems(self):
        return self._checkedItems

    @checkedItems.setter
    def checkedItems(self, checkedItems:list):
        if self._checkedItems != checkedItems:
            self._checkedItems = checkedItems
            self.CHECKED_ITEMS_READY.emit(checkedItems)


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

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        pass

    def insert_placeholder(self):
        if not self._placeholder_is_inserted():
            if not self.count():
                placeholder = self._no_columns
            elif not self.checkedItems:
                placeholder = self._selection_is_not_present
            else:
                placeholder = self._selection_is_present
            if placeholder is not None:
                super(CheckableComboBox_ABS, self).addItem(placeholder, self.placeholders_id_code)
        placeholder_row = self.findData(self.placeholders_id_code)
        self.setCurrentIndex(placeholder_row if placeholder_row != -1 else 0)


    def get_placeholder(self) -> tuple:
        row = self.findData(self.placeholders_id_code)
        if row != -1:  # ritorna indice del primo rigo che trova
            return self.itemText(row), row
        else:
            return None, None


    def _placeholder_is_inserted(self):
        return True if self.findData(self.placeholders_id_code) != -1 else False

    def remove_placeholders(self):
        row = self.findData(self.placeholders_id_code)
        while row != -1:  # ritorna indice del primo rigo che trova, se non trova -1 usare un while
            self.removeItem(row)
            row = self.findData(self.placeholders_id_code)

    def hidePopup(self):
        if not self._changed:
            self.insert_placeholder()
            super(CheckableComboBox_ABS, self).hidePopup()
            self.check_items()
            # self.CHECKED_ITEMS_READY.emit([item.text() for item in self.checkedItems])
            # self.CHECKED_ITEMS_READY.emit(self.checkedItems)
        self._changed = False

    def closeEvent(self, a0: QCloseEvent) -> None:
        self._changed = True # porkaround per non far triggerare hidePopup
        a0.accept()

    def showPopup(self) -> None:
        self.remove_placeholders()
        super(CheckableComboBox_ABS, self).showPopup()
        if not self.count():
            self.insert_placeholder()
    def setCurrentIndex(self, index: int) -> None:
        placeholder_row = self.findData(self.placeholders_id_code)
        super(CheckableComboBox_ABS, self).setCurrentIndex(placeholder_row if placeholder_row != -1 else index)

    # when any item get pressed
    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)
        # make it check if unchecked and vice-versa
        state = not item.checkState()
        item.setCheckState(state)
        # calling method
        self.check_items()
        self._changed = True

    def unselect_all(self):
        checked_items_num = len(self.checkedItems)
        for x in range(checked_items_num):
            item = self.checkedItems.pop()
            item.setCheckState(False)

    def get_checked_items(self):
        return self.check_items()

    # method called by check_items
    def item_checked(self, index):
        item = self.model().item(index, 0)
        if not isinstance(item.data(Qt.UserRole), PlaceholderIdCode):
            state = item.checkState()
            return state
        else:
            item.setCheckable(False)
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

    def addItem(self, text: str, data=None) -> None:
        if data is None:
            data = text
        super(CheckableComboBox_ABS, self).addItem(text, data)
        row = self.count() - 1 if self.count() - 1 >= 0 else 0
        item = self.model().item(row, 0)
        item.setCheckable(True)
        self.update_placeholder()

    def addItems(self, items_text, already_selected) -> None:
        self.clear()
        for item_text in items_text:
            if isinstance(item_text, str):
                data = item_text
            else:
                item_text, data = item_text.name, item_text
            self.addItem(item_text, data)
        rows = self.count()
        for row in range(rows):
            item = self.model().item(row, 0)
            item_data = item.data()
            if item_data != self.placeholders_id_code:
                if item.text() not in already_selected :
                    item.setCheckState(False)
                else:
                    item.setCheckState(True)
        self.update_placeholder()
        self.check_items()

    def update_placeholder(self):
        self.remove_placeholders()
        self.insert_placeholder()

class CheckableComboBox(CheckableComboBox_ABS):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.showMenu)
        self.selection_is_present = 'Visible Fields'
        self.selection_is_not_present = 'Selected Fields'
        #test
        # items = [f'test {x} ' for x in range(9)]
        # already_selected = list(filter(lambda x: items.index(x) % 2 == 0, items))
        # already_selected = list()
        # self.addItems(items, already_selected)
        #end test



