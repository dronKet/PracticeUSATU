from PyQt5.QtCore import QFile, QIODevice, QByteArray
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QDialogButtonBox

from VectorGraphicEditor.Logic import *
from RasterGraphicEditor.Logic import *


class GraphicsEditor(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.project_widget = widget
        self.window_width, self.window_height = 640, 480
        self.setMinimumSize(self.window_width, self.window_height)
        #hbox = QHBoxLayout()
        #hbox.addWidget(widget)
        vbox = QVBoxLayout()
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Apply", QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton("Cancel", QDialogButtonBox.RejectRole)
        #vbox.addLayout(hbox)
        vbox.addWidget(widget)
        vbox.addWidget(self.buttonBox)
        self.setLayout(vbox)

    def load_data_from_bytearray(self, byte_array):
        pass

    def load_data_to_bytearray(self, byte_array):
        pass


class VectorEditor(GraphicsEditor):
    def __init__(self):
        super().__init__(VectorEditorWindow())
        self.byte_array=QByteArray()

    def load_data_from_bytearray(self):
        # renderer = QSvgRenderer()
        renderer = QSvgRenderer()
        renderer.load(self.byte_array)
        painter=self.project_widget.widget.painter
        renderer.render(painter)
        painter.end()
        self.project_widget.update()

    def load_data_to_bytearray(self):
        input = QFile("untitled.svg")
        if input.open(QIODevice.ReadOnly):
            self.byte_array = QByteArray(input.readAll())
            input.close()
        return self.byte_array


class RasterEditor(GraphicsEditor):
    def __init__(self):
        super().__init__(RasterEditorWindow())

    def load_data_from_bytearray(self, byte_array):
        self.project_widget.central_widget.drawing_surface.loadFromData(byte_array)
        self.project_widget.update()

    def load_data_to_bytearray(self):
        byte_array = QByteArray()
        buffer = QtCore.QBuffer(byte_array)
        buffer.open(QtCore.QIODevice.WriteOnly)
        self.project_widget.central_widget.drawing_surface.save(buffer,'png')
        return byte_array


if __name__ == "__main__":
    import sys

    app = QApplication([])
    window = VectorEditor()
    window.load_data_to_bytearray()
    window.load_data_from_bytearray()
    window.show()
    app.exec()



