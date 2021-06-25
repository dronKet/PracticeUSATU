import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, \
    QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
from Form import Ui_MainWindow


class MainWindowLogic(QMainWindow):
    def __init__(self, form):
        super().__init__()
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.ui = form
        self.ui.setupUi(self)
        self.is_drawing = True
        self.is_choose_mode = False
        self.is_fill_mode = False
        self.choosed_shape = {"rect": 0, "triang": 0, "ellips": 0}
        self.coordinates_shapes = list()
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        self.begin, self.destination = QPoint(), QPoint()
        self.add_functions()
        self.count_shapes = 0
        self.show()

    def add_functions(self):
        self.ui.actionRectangle.triggered.connect(lambda: self.choose_shape("rect"))
        self.ui.actionEllips.triggered.connect(lambda: self.choose_shape("ellips"))
        self.ui.actionPaletteLine.triggered.connect(self.lineColorDialog)
        self.ui.actionPaletteBrush.triggered.connect(self.brushColorDialog)
        # self.actionChooseShape.triggered.connect(self.ChooseShape)
        self.ui.actionCleanWindow.triggered.connect(self.CleanWindow)

    def CleanWindow(self):
        self.pix.fill(Qt.white)
        self.update()
        self.count_shapes = 0
        self.coordinates_shapes.clear()

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
        painter.setPen(self.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(QPoint(), self.pix)
        if self.is_drawing:
            if not self.begin.isNull() and not self.destination.isNull():
                rect = QRect(self.begin, self.destination)
                if self.choosed_shape["rect"] == 1:
                    painter.drawRect(rect.normalized())
                elif self.choosed_shape["ellips"] == 1:
                    painter.drawEllipse(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = event.pos()
            if self.is_fill_mode:
                for dots in self.coordinates_shapes:
                    if dots[1].x() < self.begin.x() and dots[1].y() < self.begin.y() and dots[
                        2].x() > self.destination.x() and dots[2].y() > self.destination.y():

                        painter = QPainter(self.pix)
                        #  painter.drawPixmap(QPoint(), self.pix)
                        painter.setBrush(self.brush_color)
                        rect = QRect(dots[1], dots[2])
                        if dots[0] == "rect":
                            print("ok")
                            painter.drawRect(rect.normalized())
                        elif dots[0] == "ellips":
                            painter.drawEllipse(rect.normalized())
                        break
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
        self.ui.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteLine.setIcon(self.ui.icon2)


    def brushColorDialog(self):
        color = QColorDialog.getColor()
        print(color)
        self.is_drawing = False
        self.is_fill_mode = True
        self.brush_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon3.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteBrush.setIcon(self.ui.icon3)


    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pix)
            painter.setPen(self.line_color)
            painter.setRenderHint(QPainter.Antialiasing)
            if self.is_drawing:
                if self.choosed_shape["rect"] == 1:
                    painter.drawRect(rect.normalized())
                    self.coordinates_shapes.append(["rect", self.begin, self.destination])
                elif self.choosed_shape["ellips"] == 1:
                    painter.drawEllipse(rect.normalized())
                    self.coordinates_shapes.append(["ellips", self.begin, self.destination])
                self.count_shapes += 1
            # print(self.coordinates_shapes)
            self.begin, self.destination = QPoint(), QPoint()
            self.update()




if __name__ == "__main__":
    import sys

    app = QApplication([])
    ui = Ui_MainWindow()
    window = MainWindowLogic(ui)
    app.exec()
