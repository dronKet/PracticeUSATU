import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget , QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect


class Example(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.is_drawing=True
        self.line_color=QColor(0,0,0)
        self.choosed_shape = {"rect": 0, "triang": 0, "ellips": 0}
        self.coordinates_shapes=list()
        self.window_width, self.window_height = 800, 480
        self.setMinimumSize(self.window_width, self.window_height)
        self.btn_rect = QtWidgets.QPushButton(self)
        self.btn_rect.move(0, 15)
        self.btn_rect.setText("Rectangle")
        self.btn_rect.adjustSize()
        self.count_shapes=0
        self.btn_triang = QtWidgets.QPushButton(self)
        self.btn_triang.move(80, 15)
        self.btn_triang.setText("Triangle")
        self.btn_triang.adjustSize()
        self.btn_triang = QtWidgets.QPushButton(self)
        self.btn_triang.move(80, 15)
        self.btn_triang.setText("Triangle")
        self.btn_triang.adjustSize()

        self.btn_ellips = QtWidgets.QPushButton(self)
        self.btn_ellips.move(160, 15)
        self.btn_ellips.setText("Ellips")
        self.btn_ellips.adjustSize()

        self.btn_color_red = QtWidgets.QPushButton(self)
        self.btn_color_red.move(480, 15)
        self.btn_color_red.resize(5,5)
        self.btn_color_red.setText("Red")
        self.btn_color_red.adjustSize()

        self.label=QtWidgets.QLabel(self)
        self.label.move(480,0)
        self.label.setText("Цвета линии")

        self.label_color=QtWidgets.QLabel(self)
        self.label_color.move(480,0)
        self.label_color.setText("Цвета линии")



        self.btn_color_brush_red = QtWidgets.QPushButton(self)
        self.btn_color_brush_red.move(600, 15)
        #self.btn_colorbrush__black.resize(5,5)
        self.btn_color_brush_red.setText("Red")
        self.btn_color_brush_red.adjustSize()

        self.btn_color_brush_black = QtWidgets.QPushButton(self)
        self.btn_color_brush_black.move(600, 50)
        #self.btn_colorbrush__black.resize(5,5)
        self.btn_color_brush_black.setText("Black")
        self.btn_color_brush_black.adjustSize()

        self.label_color=QtWidgets.QLabel(self)
        self.label_color.move(600,0)
        self.label_color.setText("Цвета Заливки")


        self.btn_color_black = QtWidgets.QPushButton(self)
        self.btn_color_black.move(480, 50)
        #self.btn_color_black.resize(5,5)
        self.btn_color_black.setText("Black")
        self.btn_color_black.adjustSize()

        self.btn_distinguish = QtWidgets.QPushButton(self)
        self.btn_distinguish.move(320, 15)
        self.btn_distinguish.setText("Distinguish")
        self.btn_distinguish.adjustSize()


        layout = QVBoxLayout()
        self.setLayout(layout)
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        self.begin, self.destination = QPoint(), QPoint()
        self.add_functions()
        self.show()

    def add_functions(self):
        self.btn_triang.clicked.connect(lambda: self.choose_shape("triang"))
        self.btn_rect.clicked.connect(lambda: self.choose_shape("rect"))
        self.btn_ellips.clicked.connect(lambda: self.choose_shape("ellips"))
        self.btn_distinguish.clicked.connect(self.distinguish)
        self.btn_color_red.clicked.connect(lambda: self.set_color(QColor(255, 0, 0)))
        self.btn_color_black.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        self.btn_color_brush_red.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        self.btn_color_brush_black.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))

    def distinguish(self):
        self.is_drawing =False
        #self.pix = QPixmap(self.rect().size())

    def set_color(self,color):
        print(color)
        self.line_color=color

    def choose_shape(self, shape):
        self.is_drawing=True
        for key in self.choosed_shape:
            self.choosed_shape[key] = 0
        # print(shape)
        self.choosed_shape[shape] = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(self.line_color)
        painter.drawPixmap(QPoint(), self.pix)
        if not self.begin.isNull() and not self.destination.isNull() and self.is_drawing:
            rect = QRect(self.begin, self.destination)
            if self.choosed_shape["rect"] == 1:
                painter.drawRect(rect.normalized())
            elif self.choosed_shape["ellips"] == 1:
                painter.drawEllipse(rect.normalized())

        painter.end()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = event.pos()
            if not self.is_drawing:
                setBrush(QColor(200, 0, 0))
                print("OK")
                for dots in self.coordinates_shapes:
                    #if QRect(dots[1],dots[2])<QRect(self.begin,self.destination):
                    if dots[1]>self.begin and dots[2]<self.destination:
                        painter = QPainter(self)
                        painter.begin(self)
                        painter.drawPixmap(QPoint(), self.pix)
                        if not self.begin.isNull() and not self.destination.isNull():
                            rect = QRect(self.begin, self.destination)
                            if self.coordinates_shapes[0] == "rect":
                                painter.drawRect(rect.normalized())
                            elif self.coordinates_shapes[0] == "ellips":
                                painter.drawEllipse(rect.normalized())
                        painter.end()
                        break

            self.update()

    def mouseMoveEvent(self, event):
        #print(self.is_drawing)
        if event.buttons() & Qt.LeftButton and self.is_drawing:
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pix)
            painter.setPen(self.line_color)
            if self.choosed_shape["rect"] == 1:
                painter.drawRect(rect.normalized())
                self.coordinates_shapes.append(["rect",self.begin, self.destination])
            elif self.choosed_shape["ellips"] == 1:
                painter.drawEllipse(rect.normalized())
                self.coordinates_shapes.append(["ellips",self.begin, self.destination])
            #print(self.coordinates_shapes)
            self.begin, self.destination = QPoint(), QPoint()
            self.count_shapes+=1
            self.update()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = Example()
    # ex.show()
    sys.exit(app.exec_())
