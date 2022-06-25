import sys
import os
if 'PyQt5' in sys.modules:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import pyqtSignal as Signal

else:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal

# import pydevd_pycharm
#
# pydevd_pycharm.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)

#REGEX string
# rules:
minimum_capitals = 1
minimum_lowers = 1
minimum_special_char = 1
minimum_number = 1
minimum_length = 8
maximum_length = 100
validator_regex = r'^(?=.*([A-Z]){' + str(minimum_capitals) + r',})(?=.*[!@#$&*]{'+ str(minimum_special_char)+ r',})(?=.*[0-9]{' + str(minimum_number) + r',})(?=.*[a-z]{' + str(minimum_lowers) + r',}).{' + str(minimum_length) + r',' + str(maximum_length) +r'}$'

class PasswordEdit(QtWidgets.QLineEdit):
    """
    Password LineEdit with icons to show/hide password entries.
    Based on this example https://kushaldas.in/posts/creating-password-input-widget-in-pyqt.html by Kushal Das.
    """

    def __init__(self, parent=None, show_visibility=True, *args, **kwargs):
        super().__init__(*args,parent=parent, **kwargs)
        visible_icon_path = os.path.join(os.path.dirname(__file__),'icons','eye.svg')
        hidden_icon_path = os.path.join(os.path.dirname(__file__),'icons','hidden.svg')
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

    def on_toggle_visibility_Action(self):
        if not self.password_shown:
            self.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)




