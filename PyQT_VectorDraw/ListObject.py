from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QColor, QPen


class ShapeObject:
    def __init__(self, properties):
        self.properties = properties
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
        self.is_selected = False

    def update_properties(self):
        self.properties[0] = self.line_color
        self.properties[1] = self.brush_color
        self.properties[2] = self.name
        self.properties[3] = self.upper_left_point
        self.properties[4] = self.lower_right_point
        self.properties[5] = self.line_thickness

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

        if self.is_selected:
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setBrush(QColor(0, 0, 0, 0))
            painter.setPen(pen)
            painter.drawRect(rect.normalized())

    def in_excretion_shapes(self, other_shapes):
        counter = 0
        for other_shape in other_shapes:
            if other_shape.is_selected:
                if other_shape.upper_x < self.upper_x and other_shape.upper_y < self.upper_y and other_shape.lower_x > self.lower_x and other_shape.lower_y > self.lower_y:
                    counter += 1
        return counter

    def in_shape(self, other_shape):
        print(other_shape.upper_x > self.upper_x)
        if other_shape.upper_x < self.upper_x and other_shape.upper_y < self.upper_y and other_shape.lower_x > self.lower_x and other_shape.lower_y > self.lower_y:
            return True
        elif other_shape.upper_x > self.upper_x and other_shape.upper_y < self.upper_y and other_shape.lower_x < self.lower_x and other_shape.lower_y > self.lower_y:
            return True
        elif other_shape.upper_x < self.upper_x and other_shape.upper_y > self.upper_y and other_shape.lower_x > self.lower_x and other_shape.lower_y < self.lower_y:
            return True
        elif other_shape.upper_x > self.upper_x and other_shape.upper_y > self.upper_y and other_shape.lower_x < self.lower_x and other_shape.lower_y < self.lower_y:
            return True
        return False

    def copy(self):
        self.update_properties()
        clone_shape = ShapeObject(self.properties)
        clone_shape.is_selected = self.is_selected
        clone_shape.point = self.point
        return clone_shape


class ShapesOperations():
    def shapes_count(self, shapes_array):
        counter = 0
        for shape in shapes_array:
            counter += 1
        return counter

    def remove_excretion(self, shapes_array):
        for shape in shapes_array:
            shape.is_selected = False

    def draw_only_shapes_array(self, shapes_array, window, painter):
        window.main_area.fill(Qt.white)
        for shape in shapes_array:
            shape.draw(painter)
        window.update()

    def draw_shapes_array(self, shapes_array, window, painter):
        for shape in shapes_array:
            shape.draw(painter)
        window.update()

    def selected_shapes(self, shapes_array):
        selected_shapes_list = list()
        for shape in shapes_array:
            if shape.is_selected:
                selected_shapes_list.append(shape.copy())
        return selected_shapes_list

    def the_closest_shape_coords_to_point(self, shapes_array, point=QPoint(0, 0)):
        closest_coords = QPoint(-1, -1)
        for shape in shapes_array:
            if closest_coords.x() == -1:
                closest_coords.setX(shape.upper_x)
                closest_coords.setY(shape.upper_y)
            elif point.dotProduct(point, shape.upper_left_point) < point.dotProduct(point, closest_coords):
                closest_coords.setX(shape.upper_x)
                closest_coords.setY(shape.upper_y)
        return closest_coords

    def displace_shapes(self, shapes_array, point):
        for shape in shapes_array:
            shape.upper_left_point = shape.upper_left_point + point
            shape.lower_right_point = shape.lower_right_point + point
            shape.upper_x = shape.upper_left_point.x()
            shape.upper_y = shape.upper_left_point.y()
            shape.lower_x = shape.lower_right_point.x()
            shape.lower_y = shape.lower_right_point.y()

    def delete_shapes_from_array(self,shapes_array):
        temp_shapes_array=list()
        for shape in shapes_array:
            if not shape.is_selected:
                temp_shapes_array.append(shape.copy())
        return temp_shapes_array.copy()