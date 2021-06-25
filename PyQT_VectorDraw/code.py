import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, \
    QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF
from Form import Ui_MainWindow


class MainWindowLogic(QMainWindow):
    def __init__(self, form):
        super().__init__()
        self.control = ControllerShape(self)
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.ui = form
        self.ui.setupUi(self)
        self.is_drawing = True
        self.is_choose_mode = False
        self.is_fill_mode = False
        self.choosed_shape = {"rect": 0, "triang": 0, "ellips": 0, "line": 0}
        self.coordinates_shapes = list()

        self.main_area = QPixmap(self.rect().size())
        self.main_area.fill(Qt.white)

        self.external_area = QPixmap(self.rect().size())
        self.external_area.fill(QColor(0, 0, 0, 0))

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
        self.ui.lineAction.triggered.connect(lambda: self.choose_shape("line"))

    def CleanWindow(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(Qt.white)
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
        painter.drawPixmap(QPoint(), self.main_area)
        painter.drawPixmap(QPoint(), self.external_area)

    def mousePressEvent(self, event):
        # fill_control=ControllerFill(self)
        if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                print("ok")
                self.control.mouse_press_handler(event)
            elif self.is_fill_mode:
                #  fill_control.mouse_press_handler(event)
                self.begin = event.pos()
                self.destination = event.pos()
                if self.is_fill_mode:
                    for dots in self.coordinates_shapes:
                        if dots[1].x() < self.begin.x() and dots[1].y() < self.begin.y() and dots[
                            2].x() > self.destination.x() and dots[2].y() > self.destination.y():
                            painter = QPainter(self.main_area)
                            #  painter.drawPixmap(QPoint(), self.pix)
                            painter.setBrush(self.brush_color)
                            rect = QRect(dots[1], dots[2])
                            if dots[0] == "rect":
                                # print(ok)
                                painter.drawRect(rect.normalized())
                            elif dots[0] == "ellips":
                                painter.drawEllipse(rect.normalized())
                            break
                self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.is_drawing:
            self.control.mouse_move_handler(event)

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
            if self.is_drawing:
                self.control.mouse_release_handler(event)


class Controller:
    def __init__(self, window):
        self.main_window = window
        # self.main_surface = window.drawing_surface
        self.begin = QPoint()
        self.destination = QPoint()

    def mouse_press_handler(self, event):
        pass

    def mouse_move_handler(self, event):
        pass

    def mouse_release_handler(self, event):
        pass


class ControllerShape(Controller):
    def draw_shape(self):
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        painter = QPainter(self.main_window.external_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)
        # line = QLineF(self.begin.x(),self.begin.y(), self.destination.x(),self.destination.y())
        if self.main_window.choosed_shape["rect"] == 1:
            painter.drawRect(rect.normalized())
        elif self.main_window.choosed_shape["ellips"] == 1:
            painter.drawEllipse(rect.normalized())
        elif self.main_window.choosed_shape["line"] == 1:
            painter.drawLine(self.begin, self.destination)
        self.main_window.update()

    def mouse_press_handler(self, event):
        self.begin = event.pos()
        self.destination = event.pos()

        self.draw_shape()

    def mouse_move_handler(self, event):
        self.destination = event.pos()
        self.draw_shape()

    def mouse_release_handler(self, event):
        self.destination = event.pos()
        painter = QPainter(self.main_window.main_area)
        painter.drawPixmap(QPoint(), self.main_window.main_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)
        if self.main_window.choosed_shape["ellips"] == 1:
            painter.drawEllipse(rect.normalized())
            self.main_window.coordinates_shapes.append(["ellips", self.begin, self.destination])
        elif self.main_window.choosed_shape["rect"] == 1:
            painter.drawRect(rect.normalized())
            self.main_window.coordinates_shapes.append(["rect", self.begin, self.destination])
        elif self.main_window.choosed_shape["line"] == 1:
            painter.drawLine(self.begin, self.destination)
        self.main_window.count_shapes += 1


if __name__ == "__main__":
    import sys

    app = QApplication([])
    ui = Ui_MainWindow()
    window = MainWindowLogic(ui)
    app.exec()
