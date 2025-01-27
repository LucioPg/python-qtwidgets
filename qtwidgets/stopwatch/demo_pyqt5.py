from PyQt5 import QtCore, QtGui, QtWidgets
from qtwidgets.palette import PaletteHorizontal, PaletteVertical


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        palette = PaletteVertical('paired12')
        palette.selected.connect(self.show_selected_color)
        self.setCentralWidget(palette)

    def show_selected_color(self, c):
        print("Selected: {}".format(c))


app = QtWidgets.QApplication([])
w = Window()
w.show()
app.exec_()





