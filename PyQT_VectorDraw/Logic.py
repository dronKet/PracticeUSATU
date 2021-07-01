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


    def clean_window(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(Qt.white)
        self.update()
        self.count_shapes = 0
        self.shapes.clear()
        self.is_drawing = False
        self.is_choose_mode = False
        self.is_fill_mode = False
        self.is_move_mode = False
        self.shapes_in_excretion_area.clear()
        self.shapes.clear()

    def excretion_trigger(self):
        self.is_drawing = False
        if self.is_choose_mode:
            for shape in self.shapes_in_excretion_area:
                self.shapes.append(shape)
        self.is_choose_mode = True
        #self.external_area.fill(Qt.white)
        self.shapes_in_excretion_area.clear()

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
            elif self.is_choose_mode and self.excretion_coords == False:
                print("is_choose_mode")
                self.control.mouse_press_handler(event, self.is_choose_mode)
            if self.excretion_coords != False and self.is_choose_mode and self.is_move_mode:
                print("is_move_mode")
                self.is_choose_mode = False
                self.control_move.mouse_press_handler(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                self.control.mouse_move_handler(event)
            elif self.is_choose_mode and self.excretion_coords == False:
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

            elif self.is_choose_mode and self.excretion_coords == False:
                self.control.mouse_release_handler(event, self.is_choose_mode)
                self.search_hits()
                self.re_drawing_areas()

            if self.excretion_coords != False and self.is_move_mode and self.is_choose_mode:
                self.is_choose_mode = False
                self.control_move.mouse_release_handler(event)

    def fill(self):
        if self.shapes_in_excretion_area.__ne__([]):
            painter = QPainter(self.external_area)
            for shape in self.shapes_in_excretion_area:
                shape.brush_color = self.brush_color
                shape.draw(self, painter)

    def change_line_color(self):
        if self.shapes_in_excretion_area.__ne__([]):
            painter = QPainter(self.external_area)
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
                else:
                    temp_list.append(shape)
            self.shapes = temp_list

    def re_drawing_areas(self):
        self.main_area.fill(Qt.white)
        #self.external_area.fill(Qt.white)
        painter1 = QPainter(self.external_area)
        #painter1.drawPixmap(QPoint(), self.external_area)
        painter2 = QPainter(self.main_area)
        #painter2.drawPixmap(QPoint(), self.main_area)
        for shape in self.shapes_in_excretion_area:
            shape.draw(self,painter1)
        for shape in self.shapes:
            shape.draw(self,painter2)
        #self.update()

    def add_functions(self):
        self.ui.actionRectangle.triggered.connect(lambda: self.choose_shape("rect"))
        self.ui.actionEllips.triggered.connect(lambda: self.choose_shape("ellips"))
        self.ui.actionPaletteLine.triggered.connect(self.line_color_dialog)
        self.ui.actionPaletteBrush.triggered.connect(self.brush_color_dialog)
        self.ui.actionChooseShape.triggered.connect(self.excretion_trigger)
        self.ui.actionCleanWindow.triggered.connect(self.clean_window)
        self.ui.moveAction.triggered.connect(self.move_method)
        self.ui.lineAction.triggered.connect(lambda: self.choose_shape("line"))



if __name__ == "__main__":
    from Controllers import ControllerShape
    from Controllers import ControllerMove
    import sys

    app = QApplication([])
    window = MainWindowLogic()
    window.show()
    app.exec()
