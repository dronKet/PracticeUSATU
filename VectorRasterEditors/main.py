
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QApplication
from GraphicsEditors import VectorEditor, RasterEditor


def test(w1,w2):
    w2.load_data_from_bytearray(w1.load_data_to_bytearray())

def testRasterEditor():
    app = QApplication([])
    window = RasterEditor()
    window2 = RasterEditor()
    window.load_data_from_bytearray(QByteArray())
    window.buttonBox.buttons()[0].clicked.connect(lambda: test(window, window2))
    window.show()
    app.exec()

    window2.show()
    app.exec()

def testVectorEditor():
    import sys

    app = QApplication([])
    window = VectorEditor()
    window.load_data_to_bytearray()
    window.load_data_from_bytearray()
    window.show()
    app.exec()


if __name__ == '__main__':
    testVectorEditor()
    #testRasterEditor()




