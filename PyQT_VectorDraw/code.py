import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, \
    QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF
from Form import Ui_MainWindow
from Controllers import Controller, ControllerShape


class MainWindowLogic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.control = ControllerShape(self)
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.ui = Ui_MainWindow()
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

        self.begin = QPoint()
        self.destination = QPoint()
        self.add_functions()
        self.count_shapes = 0

    def add_functions(self):
        self.ui.actionRectangle.triggered.connect(lambda: self.choose_shape("rect"))
        self.ui.actionEllips.triggered.connect(lambda: self.choose_shape("ellips"))
        self.ui.actionPaletteLine.triggered.connect(self.line_color_dialog)
        self.ui.actionPaletteBrush.triggered.connect(self.brush_color_dialog)
        self.ui.actionChooseShape.triggered.connect(self.excretion_trigger)
        self.ui.actionCleanWindow.triggered.connect(self.clean_window)
        self.ui.lineAction.triggered.connect(lambda: self.choose_shape("line"))

    def clean_window(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(Qt.white)
        self.update()
        self.count_shapes = 0
        self.coordinates_shapes.clear()

    def excretion_trigger(self):
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
                self.control.mouse_press_handler(event)
            elif self.is_fill_mode:
                #  fill_control.mouse_press_handler(event)
                self.begin = event.pos()
                self.destination = event.pos()
                for dots in self.coordinates_shapes:
                    if dots[1].x() < self.begin.x() and dots[1].y() < self.begin.y() and dots[
                        2].x() > self.destination.x() and dots[2].y() > self.destination.y():
                        painter = QPainter(self.main_area)
                        painter.setBrush(self.brush_color)
                        rect = QRect(dots[1], dots[2])
                        if dots[0] == "rect":
                            painter.drawRect(rect.normalized())
                        elif dots[0] == "ellips":
                            painter.drawEllipse(rect.normalized())
                        break
                self.update()
            elif self.is_choose_mode:
                self.control.mouse_press_handler(event,self.is_choose_mode)


    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                self.control.mouse_move_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_move_handler(event,self.is_choose_mode)

    def line_color_dialog(self):
        color = QColorDialog.getColor()
        self.line_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteLine.setIcon(self.ui.icon2)

    def brush_color_dialog(self):
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
            elif self.is_choose_mode:
                self.control.mouse_release_handler(event,self.is_choose_mode)


class ShapeObject:
    def __init__(self, properties):
        self.line_color = properties[0]
        self.brush_color = properties[1]
        self.upper_left_point = properties[2]
        self.lower_right_point = properties[3]
        # self.line_thickness=
        # self.legth_thickness





if __name__ == "__main__":
    import sys

    app = QApplication([])
    window = MainWindowLogic()
    window.show()
    app.exec()
