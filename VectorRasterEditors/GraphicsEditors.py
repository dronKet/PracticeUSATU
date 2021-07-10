from PyQt5.QtCore import QFile, QIODevice, QByteArray
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QDialogButtonBox

from .VectorGraphicEditor.Logic import *
from .RasterGraphicEditor.Logic import *


class GraphicsEditor(QWidget):
    def __init__(self, widget):
        super().__init__()
        #setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        graphics_editor_dialog=QDialog()
        vbox = QVBoxLayout()
        vbox.addWidget(widget)
        graphics_editor_dialog.setLayout(vbox)
        windowFlag=0
        windowFlag |= Qt.CustomizeWindowHint
        windowFlag |= Qt.WindowMinimizeButtonHint
        windowFlag |= Qt.WindowMaximizeButtonHint
        windowFlag |= Qt.WindowCloseButtonHint
        graphics_editor_dialog.setWindowFlags(windowFlag)
        graphics_editor_dialog.exec()


class VectorEditor(GraphicsEditor):
    def __init__(self):
        super().__init__(VectorEditorWindow())


class RasterEditor(GraphicsEditor):
    def __init__(self):
        super().__init__(RasterEditorWindow())


if __name__ == "__main__":
    import sys

    app = QApplication([])
    window = RasterEditor()
    window.show()
    app.exec()
