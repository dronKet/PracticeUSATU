import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
from Form import Interface


class Example(Interface):
    def __init__(self):
        super().__init__()
        self.is_drawing = True
        self.is_choose_mode = False
        self.choosed_shape = {"rect": 0, "triang": 0, "ellips": 0}
        self.coordinates_shapes = list()
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        self.begin, self.destination = QPoint(), QPoint()
        self.add_functions()
        self.count_shapes = 0
        self.show()

    def add_functions(self):
        self.actionRectangle.triggered.connect(lambda: self.choose_shape("rect"))
        self.actionEllips.triggered.connect(lambda: self.choose_shape("ellips"))
        self.actionPaletteLine.triggered.connect(self.lineColorDialog)
        self.actionPaletteBrush.triggered.connect(self.brushColorDialog)
        self.actionChooseShape.triggered.connect(self.ChooseShape)
        self.actionCleanWindow.triggered.connect(self.CleanWindow)

    def CleanWindow(self):
        self.pix.fill(Qt.white)
        self.update()

    def ChooseShape(self):
        self.is_drawing = False
        self.is_choose_mode = True

    def choose_shape(self, shape):
        self.is_drawing = True
        for key in self.choosed_shape:
            self.choosed_shape[key] = 0
        # print(shape)
        self.choosed_shape[shape] = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(self.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull() and self.is_drawing:
            rect = QRect(self.begin, self.destination)
            if self.choosed_shape["rect"] == 1:
                painter.drawRect(rect.normalized())
            elif self.choosed_shape["ellips"] == 1:
                painter.drawEllipse(rect.normalized())

        painter.end()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = event.pos()
            ''' if self.is_choose_mode:
                for dots in self.coordinates_shapes:
                    # if QRect(dots[1],dots[2])<QRect(self.begin,self.destination):
                    if dots[1] > self.begin and dots[2] < self.destination:
                        painter = QPainter(self)
                        painter.drawPixmap(QPoint(), self.pix)
                        if not self.begin.isNull() and not self.destination.isNull():
                            rect = QRect(self.begin, self.destination)
                            if self.coordinates_shapes[0] == "rect":
                                painter.drawRect(rect.normalized())
                            elif self.coordinates_shapes[0] == "ellips":
                                painter.drawEllipse(rect.normalized())
                        break'''

            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.is_drawing:
            self.destination = event.pos()
            self.update()

    def lineColorDialog(self):
        color = QColorDialog.getColor()
        self.line_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteLine.setIcon(self.icon2)

    def brushColorDialog(self):
        color = QColorDialog.getColor()
        print(color)
        self.brush_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.icon3.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteBrush.setIcon(self.icon3)

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pix)
            painter.setPen(self.line_color)
            painter.setRenderHint(QPainter.Antialiasing)
            if self.choosed_shape["rect"] == 1:
                painter.drawRect(rect.normalized())
                self.coordinates_shapes.append(["rect", self.begin, self.destination])
            elif self.choosed_shape["ellips"] == 1:
                painter.drawEllipse(rect.normalized())
                self.coordinates_shapes.append(["ellips", self.begin, self.destination])
            # print(self.coordinates_shapes)
            self.begin, self.destination = QPoint(), QPoint()
            self.count_shapes += 1
            self.update()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = Example()
    # ex.show()
    sys.exit(app.exec_())
