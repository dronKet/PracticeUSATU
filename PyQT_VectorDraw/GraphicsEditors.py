from PyQt5.QtCore import QFile, QIODevice, QByteArray
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QDialogButtonBox

from Logic import *


class GraphicsEditor(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.prject_widget = widget
        self.window_width, self.window_height = 640, 480
        self.setMinimumSize(self.window_width, self.window_height)
        vbox = QVBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Apply", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        vbox.addWidget(widget)
        vbox.addWidget(self.buttonBox)
        self.setLayout(vbox)
        self.byte_array=QByteArray()

    def load_data_from_bytearray(self, byte_array):
        pass

    def load_data_to_bytearray(self, byte_array):
        pass


class VectorEditor(GraphicsEditor):
    def __init__(self):
        super().__init__(VectorEditorWindow())

    def load_data_from_bytearray(self):
        # renderer = QSvgRenderer()
        renderer = QSvgRenderer()
        renderer.load(self.byte_array)
        painter=self.prject_widget.widget.painter
        renderer.render(painter)
        painter.end()
        self.prject_widget.update()

    def load_data_to_bytearray(self):
        input = QFile("untitled.svg")
        if input.open(QIODevice.ReadOnly):
            self.byte_array = QByteArray(input.readAll())
            input.close()


if __name__ == "__main__":
    import sys

    app = QApplication([])
    window = VectorEditor()
    #window.load_data_to_bytearray()
    #window.load_data_from_bytearray()
    window.show()
    app.exec()