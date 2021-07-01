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
        self.point=QPoint(0,0)
        self.is_excretion =False

    def draw(self, window, painter):
        pen = QPen(self.line_color, self.line_thickness, Qt.SolidLine)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRect(self.upper_left_point+self.point, self.lower_right_point+self.point)
        painter.setBrush(self.brush_color)
        if self.name == "rect":
            painter.drawRect(rect.normalized())
        elif self.name == "ellips":
            painter.drawEllipse(rect.normalized())
        elif self.name == "line":
            painter.drawLine(self.upper_left_point+self.point, self.lower_right_point+self.point)