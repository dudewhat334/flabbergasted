from PyQt5 import QtWidgets, QtGui

class ColorButton(QtWidgets.QPushButton):
    def __init__(self, color, callback):
        super().__init__()
        self.color = color
        self.setFixedSize(40, 20)
        self.update_style()
        self.clicked.connect(self.choose_color)
        self.callback = callback

    def update_style(self):
        self.setStyleSheet(
            f"background-color: rgb({self.color[0]}, {self.color[1]}, {self.color[2]}); border: 1px solid #888; color: white;")

    def choose_color(self):
        col = QtWidgets.QColorDialog.getColor(QtGui.QColor(*self.color))
        if col.isValid():
            self.color = [col.red(), col.green(), col.blue()]
            self.update_style()
            self.callback(self.color)