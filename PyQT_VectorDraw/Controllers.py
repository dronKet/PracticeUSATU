from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QUndoStack, QUndoCommand, QColorDialog
import ListObject
import Logic
from ListObject import *


class Controller:
    def __init__(self, window):
        self.main_window = window
        self.begin = QPoint()
        self.destination = QPoint()
        self.delta_pos = QPoint(0, 0)
        self.last_pos = QPoint(0, 0)
        self.first_pos = QPoint(0, 0)
        self.shapes_op = ShapesOperations()

    def mouse_press_handler(self, event):
        pass

    def mouse_move_handler(self, event):
        pass

    def mouse_release_handler(self, event):
        pass


class ControllerCopyPaste(Controller):
    def __init__(self, window):
        super().__init__(window)
        self.copied_shapes_list = list()
        self.is_first_paste = False

    def copy(self):
        self.copied_shapes_list = self.shapes_op.selected_shapes(self.main_window.shapes).copy()
        closest_point = self.shapes_op.the_closest_shape_coords_to_point(self.copied_shapes_list)
        self.shapes_op.displace_shapes(self.copied_shapes_list, -closest_point)
        self.is_first_paste = True

    def paste(self):
        if self.copied_shapes_list:
            self.shapes_op.remove_excretion(self.main_window.shapes)
            if self.is_first_paste:
                self.main_window.shapes = self.copied_shapes_list + self.main_window.shapes
                self.is_first_paste = False
            self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                                  QPainter(self.main_window.main_area))


class ControllerAccidentalClick(Controller):
    def check_press_figure(self, shape, pos):
        if pos.x() > shape.upper_x and pos.y() > shape.upper_y and pos.x() < shape.lower_x and pos.y() < shape.lower_y:
            return True

    def mouse_press_handler(self, event):
        self.shapes_op.remove_excretion(self.main_window.shapes)
        self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                              QPainter(self.main_window.main_area))
        selected_shapes = list()
        temp_shape = 0
        for shape in self.main_window.shapes:
            if self.check_press_figure(shape, event.pos()):
                selected_shapes.append(shape)
        if len(selected_shapes) > 1:
            number_of_nested = {}
            maximum = -1
            current_count = -1
            for selected_shape in selected_shapes:
                current_count = selected_shape.in_excretion_shapes(selected_shapes)
                number_of_nested[current_count] = selected_shape
                if maximum < current_count:
                    maximum = current_count
            temp_shape = number_of_nested[maximum]
        elif len(selected_shapes) == 1:
            temp_shape = selected_shapes[0]
        if temp_shape != 0:
            temp_shape.is_selected = True
            temp_shape.draw(QPainter(self.main_window.main_area))
        self.main_window.update()


class ControllerFill(Controller):
    def fill(self, color):
        painter = QPainter(self.main_window.main_area)
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        for shape in self.main_window.shapes:
            if shape.is_selected:
                shape.brush_color = color
                # ControllerUndoRedo.undo_redo_stack.push(UndoRedoCommand())
                shape.draw(painter)
            if shape.in_excretion_shapes(self.main_window.shapes) != 0:
                shape.draw(painter)
        self.main_window.update()


class ControllerMove(Controller):
    def first_drawing(self):
        painter = QPainter(self.main_window.main_area)
        self.main_window.main_area.fill(Qt.white)
        for shape in self.main_window.shapes:
            if not shape.is_selected:
                shape.draw(painter)
        self.main_window.update()

    def draw_shape(self, painter):
        for shape in self.main_window.shapes:
            if shape.is_selected:
                shape.point = self.delta_pos
                shape.draw(painter)
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
        # self.main_window.main_area.fill(Qt.white)
        painter = QPainter(self.main_window.main_area)
        self.draw_shape(painter)
        for shape in self.main_window.shapes:
            if shape.is_selected:
                shape.lower_right_point += shape.point
                shape.upper_left_point += shape.point
                shape.upper_x = shape.upper_left_point.x()
                shape.upper_y = shape.upper_left_point.y()
                shape.lower_x = shape.lower_right_point.x()
                shape.lower_y = shape.lower_right_point.y()
                shape.point = QPoint(0, 0)


class ControllerSelect(Controller):
    def drawing_selected_rectangle(self):
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        painter = QPainter(self.main_window.external_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)
        pen = QPen(Qt.black, 2, Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(rect.normalized())
        self.main_window.update()

    def mouse_press_handler(self, event):
        self.begin = event.pos()
        self.destination = event.pos()
        self.shapes_op.remove_excretion(self.main_window.shapes)
        self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                              QPainter(self.main_window.main_area))

    def mouse_move_handler(self, event):
        self.destination = event.pos()
        if self.destination != self.begin:
            self.drawing_selected_rectangle()

    def mouse_release_handler(self, event):
        self.destination = event.pos()
        print("hi")
        if self.destination != self.begin:
            self.main_window.external_area.fill(QColor(0, 0, 0, 0))
            selected_rectangle = [QColor(0, 0, 0), QColor(255, 255, 255), "rectangle", self.begin,
                                  self.destination, 2]
            selected_rectangle_object = ShapeObject(selected_rectangle)
            for shape in self.main_window.shapes:
                if shape.in_shape(selected_rectangle_object):
                    shape.is_selected = True
            self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                                  QPainter(self.main_window.main_area))
        else:
            self.main_window.tools["accidentalClick"].mouse_press_handler(event)


class ControllerDelete(Controller):
    def delete_shapes(self):
        self.main_window.shapes = self.shapes_op.delete_shapes_from_array(self.main_window.shapes)
        self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                              QPainter(self.main_window.main_area))
        self.main_window.update()


class ControllerCut(Controller):
    def cut_shapes(self):
        self.main_window.tools["copy/paste"].copy()
        self.main_window.tools["delete"].delete_shapes()


class ControllerShape(Controller):
    def __init__(self, window, string):
        super().__init__(window)
        self.string = string

    def draw_shape(self):
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        painter = QPainter(self.main_window.external_area)
        painter.setPen(self.main_window.line_color)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.begin, self.destination)
        if self.string == "rectangle":
            painter.drawRect(rect.normalized())
        elif self.string == "ellips":
            painter.drawEllipse(rect.normalized())
        elif self.string == "line":
            painter.drawLine(self.begin, self.destination)
        self.main_window.update()

    def mouse_press_handler(self, event):
        self.shapes_op.remove_excretion(self.main_window.shapes)
        self.shapes_op.draw_only_shapes_array(self.main_window.shapes, self.main_window,
                                              QPainter(self.main_window.main_area))
        self.begin = event.pos()
        self.destination = event.pos()

    def mouse_move_handler(self, event):
        self.destination = event.pos()
        if self.destination != self.begin:
            self.draw_shape()

    def mouse_release_handler(self, event, is_choose_mode=False):
        self.destination = event.pos()
        if self.destination != self.begin:
            painter = QPainter(self.main_window.main_area)
            painter.setPen(self.main_window.line_color)
            painter.setRenderHint(QPainter.Antialiasing)
            rect = QRect(self.begin, self.destination)
            created_shape = False
            if self.string == "ellips":
                painter.drawEllipse(rect.normalized())
                created_shape = [self.main_window.line_color, self.main_window.brush_color, "ellips", self.begin,
                                 self.destination, 2]
            elif self.string == "rectangle":
                painter.drawRect(rect.normalized())
                created_shape = [self.main_window.line_color, self.main_window.brush_color, "rectangle", self.begin,
                                 self.destination, 2]
            elif self.string == "line":
                painter.drawLine(self.begin, self.destination)
                created_shape = [self.main_window.line_color, self.main_window.brush_color, "line", self.begin,
                                 self.destination, 2]
            created_shape = ShapeObject(created_shape)
            self.main_window.shapes.append(created_shape)
            self.main_window.last_shapes_list = self.main_window.shapes
            self.main_window.undo_redo.undo_redo_stack.push(UndoRedoCommand(self.main_window.undo_redo))
            self.main_window.update()


class ControllerUndoRedo:
    def __init__(self, window):
        self.step_stack = []
        self.current_step = -1
        self.main_window = 0
        self.undo_redo_stack = QUndoStack()
        self.main_window = window
        self.save_stage()

    def save_stage(self):
        while len(self.step_stack) > self.current_step + 1:
            del self.step_stack[-1]
        self.step_stack.append(self.main_window.shapes.copy())
        self.current_step += 1

    def set_now_stage(self):
        self.main_window.shapes = self.step_stack[self.current_step].copy()
        self.main_window.external_area.fill(QColor(0, 0, 0, 0))
        self.re_drawing_areas()
        self.main_window.update()

    def re_drawing_areas(self):
        self.main_window.main_area.fill(Qt.white)
        painter = QPainter(self.main_window.main_area)
        for shape in self.main_window.shapes:
            shape.draw(painter)
            self.main_window.update()

    def undo(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.set_now_stage()

    def redo(self):
        if self.current_step < len(self.step_stack) - 1:
            self.current_step += 1
            self.set_now_stage()


class UndoRedoCommand(QUndoCommand):
    def __init__(self, undo_redo):
        super(UndoRedoCommand, self).__init__()
        undo_redo.save_stage()
        self.undo_redo = undo_redo

    def undo(self):
        self.undo_redo.undo()

    def redo(self):
        self.undo_redo.redo()
