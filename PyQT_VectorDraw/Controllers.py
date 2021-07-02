from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
import ListObject
import Logic
from ListObject import ShapeObject


class Controller:
    def __init__(self, window):
        self.main_window = window
        self.begin = QPoint()
        self.destination = QPoint()
        self.delta_pos = QPoint(0, 0)
        self.last_pos = QPoint(0, 0)
        self.first_pos = QPoint(0, 0)
        self.k = 0

    def mouse_press_handler(self, event):
        pass

    def mouse_move_handler(self, event):
        pass

    def mouse_release_handler(self, event):
        pass


class ControllerАccidentalClick(Controller):
    def check_press_figure(self,shape,pos):
        if pos.x() > shape.upper_x and pos.y() > shape.upper_y and pos.x() < shape.lower_x and pos.y() < shape.lower_y:
            return True

    def excretion_pressed_figure(self,event):
        for shape in self.main_window.shapes:
            if self.check_press_figure(shape,event.pos()):
                shape.is_excretion=True
                shape.draw(self.main_window,QPainter(self.main_window.main_area))
                self.main_window.update

class ControllerMove(Controller):
    def first_drawing(self):
        painter=QPainter(self.main_window.main_area)
        self.main_window.main_area.fill(Qt.white)
        for shape in self.main_window.shapes:
            if not shape.is_excretion:
                print("drawed")
                shape.draw(self, painter)
        self.main_window.update()

    def draw_shape(self,painter):
        for shape in self.main_window.shapes:
            if shape.is_excretion:
                shape.point = self.delta_pos
                shape.draw(self, painter)
        self.main_window.update()

    def mouse_press_handler(self, event):
        self.first_pos = event.pos()
        self.first_drawing()

    def mouse_move_handler(self, event):
        self.delta_pos = event.pos() - self.first_pos
        painter = QPainter(self.main_window.external_area)
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        self.draw_shape(painter)

    def mouse_release_handler(self, event):
        self.delta_pos = event.pos() - self.first_pos
        #self.main_window.main_area.fill(Qt.white)
        painter = QPainter(self.main_window.main_area)
        self.draw_shape(painter)
        for shape in self.main_window.shapes:
            if shape.is_excretion:
                shape.lower_right_point += shape.point
                shape.upper_left_point += shape.point
                shape.point=QPoint(0,0)

class ControllerShape(Controller):
    def draw_shape(self, is_choose_mode):
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        painter = QPainter(self.main_window.external_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)
        if is_choose_mode:
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(rect.normalized())
        else:
            if self.main_window.choosed_shape["rect"] == 1:
                painter.drawRect(rect.normalized())
            elif self.main_window.choosed_shape["ellips"] == 1:
                painter.drawEllipse(rect.normalized())
            elif self.main_window.choosed_shape["line"] == 1:
                painter.drawLine(self.begin, self.destination)
        self.main_window.update()

    def mouse_press_handler(self, event, is_choose_mode=False):
        self.begin = event.pos()
        self.destination = event.pos()
        #self.draw_shape(is_choose_mode)

    def mouse_move_handler(self, event, is_choose_mode=False):
        self.destination = event.pos()
        if self.destination!=self.begin:
            self.draw_shape(is_choose_mode)

    def mouse_release_handler(self, event, is_choose_mode=False):
        self.destination = event.pos()
        if self.destination!=self.begin:
            painter = QPainter(self.main_window.main_area)
            painter.setPen(self.main_window.line_color)
            painter.setRenderHint(QPainter.Antialiasing)
            rect = QRect(self.begin, self.destination)
            if is_choose_mode:
                self.main_window.external_area.fill(QColor(0, 0, 0, 0))
                self.main_window.excretion_coords = [self.begin, self.destination]
            else:
                created_shape = False
                if self.main_window.choosed_shape["ellips"] == 1:
                    painter.drawEllipse(rect.normalized())
                    created_shape = [self.main_window.line_color, self.main_window.brush_color, "ellips", self.begin,
                                     self.destination, 2]
                elif self.main_window.choosed_shape["rect"] == 1:
                    painter.drawRect(rect.normalized())
                    created_shape = [self.main_window.line_color, self.main_window.brush_color, "rect", self.begin,
                                     self.destination, 2]
                elif self.main_window.choosed_shape["line"] == 1:
                    painter.drawLine(self.begin, self.destination)
                    created_shape = [self.main_window.line_color, self.main_window.brush_color, "line", self.begin,
                                     self.destination, 2]
                created_shape = ShapeObject(created_shape)
                self.main_window.shapes.append(created_shape)
                self.main_window.last_shapes_list=self.main_window.shapes
