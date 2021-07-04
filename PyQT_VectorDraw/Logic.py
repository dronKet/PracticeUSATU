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
        self.tools = {}
        # self.tools["fill"]=ControllerFill(self)
        # self.tools["change_color"]=ControllerChangeColor(self)
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.color= QColor(0, 0, 0)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.shapes = list()
        self.excretion_coords = False
        self.main_area = QPixmap(self.rect().size())
        self.main_area.fill(Qt.white)
        self.external_area = QPixmap(self.rect().size())
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.begin = QPoint()
        self.destination = QPoint()
        self.undo_redo = ControllerUndoRedo(self)
        self.current_tool = Controller(self)
        self.tools["rectangle"] = ControllerShape(self, "rectangle")
        self.tools["ellips"] = ControllerShape(self, "ellips")
        self.tools["line"] = ControllerShape(self, "line")
        self.tools["move"] = ControllerMove(self)
        self.tools["select"] = ControllerSelect(self)
        self.tools["accidentalClick"] = ControllerAccidentalClick(self)
        self.tools["fill"] = ControllerFill(self)
        self.add_functions()

    def add_functions(self):
        self.ui.actionRectangle.triggered.connect(lambda: self.change_tool("rectangle"))
        self.ui.actionEllips.triggered.connect(lambda: self.change_tool("ellips"))
        self.ui.lineAction.triggered.connect(lambda: self.change_tool("line"))
        # self.ui.actionPalette.triggered.connect(lambda: self.change_tool("change_color"))
        self.ui.selectAction.triggered.connect(lambda: self.change_tool("select"))
        self.ui.moveAction.triggered.connect(lambda: self.change_tool("move"))
        self.ui.fillAction.triggered.connect(lambda: self.tools["fill"].fill(self.color))
        self.ui.actionPalette.triggered.connect(self.change_color)
        self.ui.actionCleanWindow.triggered.connect(self.clean_window)
        self.ui.undoAction.triggered.connect(self.undo_redo.undo_redo_stack.undo)
        self.ui.redoAction.triggered.connect(self.undo_redo.undo_redo_stack.redo)

    def change_tool(self, name_of_tool):
        self.current_tool = self.tools[name_of_tool]

    def change_color(self):
        color = QColorDialog.getColor()
        self.color=color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.paletteIcon.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPalette.setIcon(self.ui.paletteIcon)

    def clean_window(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.update()
        self.shapes.clear()

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
            self.current_tool.mouse_press_handler(event)
        '''if event.buttons() & Qt.LeftButton:
            if self.are_selected_items() and not self.is_move_mode:
                self.rm_excretion()
                self.re_drawing_areas()
            if self.is_drawing:
                self.current_tool.mouse_press_handler(event)
            elif self.are_selected_items() and self.is_move_mode:
                self.control_move.mouse_press_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_press_handler(event, self.is_choose_mode)'''

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.current_tool.mouse_move_handler(event)
        '''if event.buttons() & Qt.LeftButton:
            if self.is_drawing:
                self.current_tool.mouse_move_handler(event)
            elif self.is_move_mode:
                self.control_move.mouse_move_handler(event)
            elif self.is_choose_mode:
                self.control.mouse_move_handler(event, self.is_choose_mode)'''

    def line_color_dialog(self):
        color = QColorDialog.getColor()
        self.line_color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        self.ui.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.actionPaletteLine.setIcon(self.ui.icon2)
        self.change_line_color(color)

    def mouseReleaseEvent(self, event):
        self.current_tool.mouse_release_handler(event)
        '''if event.button() & Qt.LeftButton:
            if self.is_drawing:
                self.last_shapes_list = None
                self.current_tool.mouse_release_handler(event)
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
                self.last_shapes_list=list()'''

    def fill(self, color):
        painter = QPainter(self.main_area)
        self.external_area.fill(QColor(0, 0, 0, 0))
        for shape in self.shapes:
            if shape.is_excretion:
                shape.brush_color = color
                # ControllerUndoRedo.undo_redo_stack.push(UndoRedoCommand())
                shape.draw(self, painter)
            if shape.in_excretion_shapes(self.shapes) != 0:
                shape.draw(self, painter)
        self.update()

    def change_line_color(self, color):
        painter = QPainter(self.external_area)
        for shape in self.shapes:
            if shape.is_excretion:
                shape.line_color = color
                ControllerUndoRedo.undo_redo_stack.push(UndoRedoCommand())
                shape.draw(self, painter)


if __name__ == "__main__":
    from Controllers import *
    import sys

    app = QApplication([])
    window = MainWindowLogic()
    window.show()
    app.exec()
