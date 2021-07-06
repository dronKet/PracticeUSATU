from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QPen


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
        self.point = QPoint(0, 0)
        self.is_excretion = False

    def draw(self, painter):
        pen = QPen(self.line_color, self.line_thickness, Qt.SolidLine)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.upper_left_point + self.point, self.lower_right_point + self.point)
        painter.setBrush(self.brush_color)
        if self.name == "rectangle":
            painter.drawRect(rect.normalized())
        elif self.name == "ellips":
            painter.drawEllipse(rect.normalized())
        elif self.name == "line":
            painter.drawLine(self.upper_left_point + self.point, self.lower_right_point + self.point)

        if self.is_excretion:
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setBrush(QColor(0, 0, 0, 0))
            painter.setPen(pen)
            painter.drawRect(rect.normalized())

    def in_excretion_shapes(self, other_shapes):
        counter = 0
        for other_shape in other_shapes:
            if other_shape.is_excretion:
                if other_shape.upper_x < self.upper_x and other_shape.upper_y < self.upper_y and other_shape.lower_x > self.lower_x and other_shape.lower_y > self.lower_y:
                    counter += 1
        return counter

    def in_shape(self, other_shape):
        if other_shape.upper_x < self.upper_x and other_shape.upper_y < self.upper_y and other_shape.lower_x > self.lower_x and other_shape.lower_y > self.lower_y:
            return True
        return False


class ShapesOperations():
    def shapes_count(self, shapes_array):
        counter = 0
        for shape in shapes_array:
            counter += 1
        return counter

    def remove_excretion(self, shapes_array):
        for shape in shapes_array:
            shape.is_excretion = False

    def draw_only_shapes_array(self, shapes_array, window, painter):
        window.main_area.fill(Qt.white)
        for shape in shapes_array:
            shape.draw(painter)
        window.update()

    def draw_shapes_array(self, shapes_array, window, painter):
        for shape in shapes_array:
            shape.draw(painter)
        window.update()

