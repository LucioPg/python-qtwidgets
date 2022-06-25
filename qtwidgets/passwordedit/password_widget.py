import sys, os, re

if 'PyQt5' in sys.modules:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, pyqtProperty as Property

else:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal


# import pydevd_pycharm
#
# pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)


class ValidationEnum:
    minimum_capitals = 1
    minimum_lowers = 1
    minimum_special_char = 1
    minimum_number = 1
    minimum_length = 8
    maximum_length = 100

    def as_dict(self):
        return dict(minimum_capitals=self.minimum_capitals,
                    minimum_lowers=self.minimum_lowers,
                    minimum_special_char=self.minimum_special_char,
                    minimum_number=self.minimum_number,
                    minimum_length=self.minimum_length,
                    maximum_length=self.maximum_length)


class PasswordEdit(QtWidgets.QLineEdit):
    """
    Password LineEdit with icons to show/hide password entries.
    Based on this example https://kushaldas.in/posts/creating-password-input-widget-in-pyqt.html by Kushal Das.
    Validation rules are also configurable properties that can be setted into the designer.
    If the validation is valid the validation_ok signal will be emitted.
    """
    validation_ok = Signal()
    validation_failed = Signal()

    def __init__(self, parent=None, show_visibility=True, *args, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        visible_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'eye.svg')
        hidden_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'hidden.svg')
        self._validation_rules = ValidationEnum()
        self.visibleIcon = QtGui.QIcon(visible_icon_path)
        self.hiddenIcon = QtGui.QIcon(hidden_icon_path)
        self.setEchoMode(QtWidgets.QLineEdit.Password)

        if show_visibility:
            # Add the password hide/shown toggle at the end of the edit box.
            self.togglepasswordAction = self.addAction(
                self.visibleIcon,
                QtWidgets.QLineEdit.TrailingPosition
            )
            self.togglepasswordAction.triggered.connect(self.on_toggle_visibility_Action)

        self.password_shown = False
        self.returnPressed.connect(self.validate)
        self.validation_failed.connect(self.show_tooltip)

    def on_toggle_visibility_Action(self):
        if not self.password_shown:
            self.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)

    @Property(int)
    def maximum_length(self):
        return self._validation_rules.maximum_length

    @maximum_length.setter
    def maximum_length(self, maximum_length):
        if self._validation_rules.maximum_length != maximum_length:
            if maximum_length <= self._validation_rules.minimum_length:
                maximum_length = self._validation_rules.minimum_length
            elif maximum_length > 200:
                maximum_length = 200
            self._validation_rules.maximum_length = maximum_length

    @Property(int)
    def minimum_length(self):
        return self._validation_rules.minimum_length

    @minimum_length.setter
    def minimum_length(self, minimum_length):
        if self._validation_rules.minimum_length != minimum_length:
            tot_minima = sum(map(int, [val for opt, val in self._validation_rules.as_dict().items() if
                                       opt not in ['minimum_length', 'maximum_length']]))
            if minimum_length <= tot_minima:
                minimum_length = tot_minima
            self._validation_rules.minimum_length = minimum_length

    @Property(int)
    def minimum_number(self):
        return self._validation_rules.minimum_number

    @minimum_number.setter
    def minimum_number(self, minimum_number):
        if self._validation_rules.minimum_number != minimum_number:
            if minimum_number <= 0:
                minimum_number = 1
            self._validation_rules.minimum_number = minimum_number

    @Property(int)
    def minimum_special_char(self):
        return self._validation_rules.minimum_special_char

    @minimum_special_char.setter
    def minimum_special_char(self, minimum_special_char):
        if self._validation_rules.minimum_special_char != minimum_special_char:
            if minimum_special_char <= 0:
                minimum_special_char = 1
            self._validation_rules.minimum_special_char = minimum_special_char

    @Property(int)
    def minimum_lowers(self):
        return self._validation_rules.minimum_lowers

    @minimum_lowers.setter
    def minimum_lowers(self, minimum_lowers):
        if self._validation_rules.minimum_lowers != minimum_lowers:
            if minimum_lowers <= 0:
                minimum_lowers = 1
            self._validation_rules.minimum_lowers = minimum_lowers

    @Property(int)
    def minimum_capitals(self):
        return self._validation_rules.minimum_capitals

    @minimum_capitals.setter
    def minimum_capitals(self, minimum_capitals):
        if self._validation_rules.minimum_capitals != minimum_capitals:
            if minimum_capitals <= 0:
                minimum_capitals = 1
            self._validation_rules.minimum_capitals = minimum_capitals

    @property
    def validation_rules(self):
        return self._validation_rules

    @validation_rules.setter
    def validation_rules(self, rules):
        if self._validation_rules != rules:
            self._validation_rules = rules

    def _build_validation_regex(self):
        rules = self._validation_rules
        return r'^(?=.*([A-Z]){' + str(rules.minimum_capitals) + r',})(?=.*[!@#$&*]{' + str(
            rules.minimum_special_char) + r',})(?=.*[0-9]{' + str(rules.minimum_number) + r',})(?=.*[a-z]{' + str(
            rules.minimum_lowers) + r',}).{' + str(rules.minimum_length) + r',' + str(
            rules.maximum_length) + r'}$'

    def _validate(self, text):
        pattern = self._build_validation_regex()
        return bool(re.match(pattern, text))

    def validate(self):
        text = self.text()
        if text:
            if self._validate(text):
                self.validation_ok.emit()
            else:
                self.validation_failed.emit()

    def show_tooltip(self):
        QtWidgets.QToolTip.showText(self.mapToGlobal(QtCore.QPoint(0, 0)), self._build_tooltip(),
                                    self, self.rect(), 3000)

    def _build_tooltip(self):
        opts = self._validation_rules.as_dict()
        info = f'The password should have:\n'
        chain = ', '.join([f'{opt.replace("_", " ")}: {value}' for opt, value in opts.items()])
        return f'{info}{chain}'
