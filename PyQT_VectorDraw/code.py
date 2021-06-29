import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, \
    QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QPen
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF
from Form import Ui_MainWindow


class MainWindowLogic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.control = ControllerShape(self)
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.is_drawing = False
        self.is_choose_mode = False
        self.is_fill_mode = False
        self.is_move_mode = False
        self.choosed_shape = {"rect": 0, "triang": 0, "ellips": 0, "line": 0}
        self.shapes = list()
        self.excretion_coords = False
        self.main_area = QPixmap(self.rect().size())
        self.main_area.fill(Qt.white)
        self.external_area = QPixmap(self.rect().size())
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.shapes_in_excretion_area = list()
        self.control_move = ControllerMove(self)
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
        self.ui.moveAction.triggered.connect(self.move_method)
        self.ui.lineAction.triggered.connect(lambda: self.choose_shape("line"))

    def clean_window(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(Qt.white)
        self.update()
        self.count_shapes = 0
        self.shapes.clear()

    def excretion_trigger(self):
        self.is_drawing = False
        self.is_choose_mode = True
        self.external_area.fill(Qt.white)
        for shape in self.shapes_in_excretion_area:
            self.shapes.append(shape)
        self.shapes_in_excretion_area.clear()

    #  self.update()

    def choose_shape(self, shape):
        self.is_drawing = True
        self.is_choose_mode = False
        for key in self.choosed_shape:
            self.choosed_shape[key] = 0
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
            elif self.is_choose_mode:
                self.control.mouse_press_handler(event, self.is_choose_mode)
            if self.excretion_coords != False and self.is_choose_mode and self.is_move_mode:
                self.is_choose_mode = False
                self.control_move.mouse_press_handler(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                self.control.mouse_move_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_move_handler(event, self.is_choose_mode)
            if self.excretion_coords != False and self.is_move_mode:
                self.is_choose_mode = False
                self.control_move.mouse_move_handler(event)

    def move_method(self):
        self.is_drawing = False
        self.is_fill_mode = False
        if self.is_choose_mode:
            self.is_move_mode = True

    def line_color_dialog(self):
        color = QColorDialog.getColor()
        self.line_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteLine.setIcon(self.ui.icon2)

        self.change_line_color()

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
        self.fill()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            if self.is_drawing:
                self.control.mouse_release_handler(event)
            #  elif self.is_fill_mode:

            elif self.is_choose_mode:
                self.control.mouse_release_handler(event, self.is_choose_mode)
                self.search_hits()

            if self.excretion_coords != False and self.is_move_mode and self.is_choose_mode:
                self.is_choose_mode = False
                self.control_move.mouse_release_handler(event)

    def fill(self):
        if self.shapes_in_excretion_area.__ne__([]):
            painter = QPainter(self.external_area)
            painter.drawPixmap(QPoint(), self.external_area)
            print(self.shapes_in_excretion_area)
            for shape in self.shapes_in_excretion_area:
                shape.brush_color = self.brush_color
                shape.draw(self, painter)

    def change_line_color(self):
        if self.shapes_in_excretion_area.__ne__([]):
            painter = QPainter(self.external_area)
            painter.drawPixmap(QPoint(), self.external_area)
            print(self.shapes_in_excretion_area)
            for shape in self.shapes_in_excretion_area:
                shape.line_color = self.line_color
                shape.draw(self, painter)

    def search_hits(self):
        excr = self.excretion_coords
        if excr != False:
            temp_list = list()
            for shape in self.shapes:
                if excr[0].x() < shape.upper_x and excr[0].y() < shape.upper_y and excr[1].x() > shape.lower_x and excr[
                    1].y() > shape.lower_y:
                    self.shapes_in_excretion_area.append(shape)
                    # self.shapes.pop(shape)
                else:
                    temp_list.append(shape)
            self.shapes = temp_list


class ShapeObject:
    def __init__(self, properties):
        self.line_color = properties[0]
        self.brush_color = properties[1]
        self.name = properties[2]
        self.upper_left_point = properties[3]
        self.upper_x = self.upper_left_point.x()
        self.upper_y = self.upper_left_point.y()
        self.lower_right_point = properties[4]
        self.lower_x = self.lower_right_point.x()
        self.lower_y = self.lower_right_point.y()
        self.line_thickness = properties[5]
        self.point=QPoint(0,0)

    def draw(self, window, painter):
        pen = QPen(self.line_color, self.line_thickness, Qt.SolidLine)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.upper_left_point+self.point, self.lower_right_point++self.point)
        painter.setBrush(self.brush_color)
        if self.name == "rect":
            painter.drawRect(rect.normalized())
        elif self.name == "ellips":
            painter.drawEllipse(rect.normalized())
        elif self.name == "line":
            painter.drawLine(self.upper_left_point+self.point, self.lower_right_point+self.point)


class Controller:
    def __init__(self, window):
        self.main_window = window
        # self.main_surface = window.drawing_surface
        self.begin = QPoint()
        self.destination = QPoint()
        self.first_pos = 0

    def mouse_press_handler(self, event):
        pass

    def mouse_move_handler(self, event):
        pass

    def mouse_release_handler(self, event):
        pass


class ControllerMove(Controller):
    #  def __init__(self):
    #    super().__init__()
    def draw_shape(self):
        painter = QPainter(self.main_window.external_area)
        painter.drawPixmap(QPoint(), self.main_window.external_area)
        for shape in self.main_window.shapes_in_excretion_area:
            # print(shape.upper_left_point + self.first_pos)
            # print(shape.lower_right_point+self.first_pos)
            shape.point=self.first_pos
            #shape.upper_left_point = self.first_pos
            #shape.lower_right_point = self.first_pos
            shape.draw(self, painter)
        self.main_window.update()

    def mouse_press_handler(self, event):
        self.first_pos = event.pos()
        # self.begin = event.pos()
        # self.destination = event.pos()
        # print(2)

    # self.draw_shape()

    def mouse_move_handler(self, event):
        self.first_pos = event.pos() - self.first_pos
        print(self.first_pos)
        self.main_window.external_area.fill(Qt.white)
        self.draw_shape()

    def mouse_release_handler(self, event):
        self.first_pos = event.pos() - self.first_pos
        self.draw_shape()


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
        self.draw_shape(is_choose_mode)

    def mouse_move_handler(self, event, is_choose_mode=False):
        self.destination = event.pos()
        self.draw_shape(is_choose_mode)

    def mouse_release_handler(self, event, is_choose_mode=False):
        self.destination = event.pos()
        painter = QPainter(self.main_window.main_area)
        painter.drawPixmap(QPoint(), self.main_window.main_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)

        if is_choose_mode:
            painter = QPainter(self.main_window.external_area)
            painter.drawPixmap(QPoint(), self.main_window.external_area)
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(rect.normalized())
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
            self.main_window.count_shapes += 1


if __name__ == "__main__":
    import sys

    app = QApplication([])
    window = MainWindowLogic()
    window.show()
    app.exec()
