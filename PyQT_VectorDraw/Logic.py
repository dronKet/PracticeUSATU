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
        self.control_move = ControllerMove(self)
        self.begin = QPoint()
        self.destination = QPoint()
        self.last_shapes_list=self.shapes
        self.undo_redo=ControllerUndoRedo(self)
        self.add_functions()


    def add_functions(self):
        self.ui.actionRectangle.triggered.connect(lambda: self.choose_shape("rect"))
        self.ui.actionEllips.triggered.connect(lambda: self.choose_shape("ellips"))
        self.ui.actionPaletteLine.triggered.connect(self.line_color_dialog)
        self.ui.actionPaletteBrush.triggered.connect(self.brush_color_dialog)
        self.ui.actionChooseShape.triggered.connect(self.excretion_trigger)
        self.ui.actionCleanWindow.triggered.connect(self.clean_window)
        self.ui.moveAction.triggered.connect(self.move_method)
        self.ui.lineAction.triggered.connect(lambda: self.choose_shape("line"))
        self.ui.undoAction.triggered.connect(self.undo_redo.undo_redo_stack.undo)
        self.ui.redoAction.triggered.connect(self.undo_redo.undo_redo_stack.redo)
        #self.ui.undoAction.triggered.connect(ControllerUndoRedo.undo_redo_stack.undo)
        #self.ui.redoAction.triggered.connect(ControllerUndoRedo.undo_redo_stack.redo)


    def clean_window(self):
        self.off_tools()
        self.main_area.fill(Qt.white)
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.update()
        self.shapes.clear()

    def off_tools(self):
        self.is_drawing = False
        self.is_choose_mode = False
        self.is_fill_mode = False
        self.is_move_mode = False


    def excretion_trigger(self):
        self.off_tools()
        self.rm_excretion()
        self.is_choose_mode=True

    def choose_shape(self, shape):
        self.off_tools()
        self.is_drawing = True
        for key in self.choosed_shape:
            self.choosed_shape[key] = 0
        self.choosed_shape[shape] = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.main_area)
        painter.drawPixmap(QPoint(), self.external_area)

    def are_selected_items(self):
        for shape in self.shapes:
            if shape.is_excretion:
                return True
        return False

    def mousePressEvent(self, event):
        # fill_control=ControllerFill(self)
        if event.buttons() & Qt.LeftButton:
            if self.are_selected_items() and not self.is_move_mode:
                self.rm_excretion()
                self.re_drawing_areas()
            if self.is_drawing:
                self.control.mouse_press_handler(event)
            elif self.are_selected_items() and self.is_move_mode:
                self.control_move.mouse_press_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_press_handler(event, self.is_choose_mode)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                self.control.mouse_move_handler(event)
            elif self.is_move_mode:
                self.control_move.mouse_move_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_move_handler(event, self.is_choose_mode)

    def move_method(self):
        self.off_tools()
        self.is_move_mode=True

    def line_color_dialog(self):
        color = QColorDialog.getColor()
        self.line_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteLine.setIcon(self.ui.icon2)
        self.change_line_color(color)

    def brush_color_dialog(self):
        color = QColorDialog.getColor()
        self.off_tools()
        self.is_fill_mode = True
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon3.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteBrush.setIcon(self.ui.icon3)
        self.fill(color)

    def rm_excretion(self):
        painter = QPainter(self.main_area)
        for shape in self.shapes:
            shape.is_excretion=False
            for shape in self.shapes:
                shape.draw(self, painter)
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            if self.is_drawing:
                self.last_shapes_list = None
                self.control.mouse_release_handler(event)
                self.re_drawing_areas()

            elif self.is_move_mode:
                self.is_choose_mode = False
                self.control_move.mouse_release_handler(event)

            elif self.is_choose_mode:
                self.last_shapes_list = None
                self.control.mouse_release_handler(event, self.is_choose_mode)
                self.search_hits()
                self.re_drawing_areas()

            if self.last_shapes_list==None:
                self.rm_excretion()
                random_click=ControllerАccidentalClick(self)
                random_click.excretion_pressed_figure(event)
                self.off_tools()
                self.last_shapes_list=list()

    def fill(self,color):
            painter = QPainter(self.main_area)
            self.external_area.fill(QColor(0, 0, 0, 0))
            for shape in self.shapes:
                if shape.is_excretion:
                    shape.brush_color = color
                    #ControllerUndoRedo.undo_redo_stack.push(UndoRedoCommand())
                    shape.draw(self, painter)
                if shape.in_excretion_shape(self.shapes)!=0:
                    shape.draw(self,painter)
            self.update()

    def change_line_color(self,color):
        painter = QPainter(self.external_area)
        for shape in self.shapes:
            if shape.is_excretion:
                shape.line_color = color
                ControllerUndoRedo.undo_redo_stack.push(UndoRedoCommand())
                shape.draw(self, painter)

    def search_hits(self):
        excr = self.excretion_coords
        self.excretion_coords=False
        if excr != False:
            for shape in self.shapes:
                if excr[0].x() < shape.upper_x and excr[0].y() < shape.upper_y and excr[1].x() > shape.lower_x and excr[
                    1].y() > shape.lower_y:
                    shape.is_excretion=True


    def re_drawing_areas(self):
        self.main_area.fill(Qt.white)
        painter = QPainter(self.main_area)
        for shape in self.shapes:
            shape.draw(self, painter)
        self.update()




if __name__ == "__main__":
    from Controllers import ControllerShape, ControllerMove, ControllerАccidentalClick,ControllerUndoRedo,UndoRedoCommand
    import sys
    app = QApplication([])
    window = MainWindowLogic()
    window.show()
    app.exec()
