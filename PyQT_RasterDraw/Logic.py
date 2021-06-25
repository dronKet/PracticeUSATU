import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QMainWindow, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt, QPoint, QRect


# from Form import Interface


class MainWindowLogic(QMainWindow):
    # Текущий цвет, которым будут рисоваться новые элементы
    draw_color_now = QColor(0, 0, 0)

    # Набор доступных инструментов
    draw_tools = {}

    # Текущий инструмент
    draw_tool_now_id = "draw_rectangle"


    def __init__(self, ui_init):
        super().__init__()
        self.ui = ui_init
        self.ui.setupUi(self)

        self.is_drawing = True


        # Создаем изображение, на котором будет рисовать пользователь
        self.drawing_surface = QPixmap(self.rect().size())
        self.drawing_surface.fill(Qt.white)
        # Создаем буферное изображение для инструментов, оно будет отрисовываться поверх основного
        self.tool_surface = QPixmap(self.rect().size())
        self.tool_surface.fill(QColor(0, 0, 0, 0))

        #Различная информация для инструментов
        self.tool_data = {}
        self.tool_data.setdefault("color",QColor(0,0,0))

        # Назначаем обработчики событий
        self.add_functions()

        # Инициализируем инструменты
        self.draw_tools.setdefault("draw_rectangle",ToolController_Figure_Rectangle(self))
        self.draw_tools.setdefault("draw_ellipse",ToolController_Figure_Ellipse(self))
        self.draw_tools.setdefault("draw_line",ToolController_Figure_Line(self))
        self.draw_tools.setdefault("draw_point",ToolController_Figure_Point(self))
        self.draw_tools.setdefault("draw_fill",ToolController_Fill(self))
        self.draw_tool_now = self.draw_tools["draw_rectangle"]


        # Выводим окно
        self.show()

    def add_functions(self):
        # self.btn_triang.clicked.connect(lambda: self.choose_shape("triang"))
        # self.btn_rect.clicked.connect(lambda: self.choose_shape("rect"))
        # self.btn_ellips.clicked.connect(lambda: self.choose_shape("ellips"))
        # self.btn_color_red.clicked.connect(lambda: self.set_color(QColor(255, 0, 0)))
        # self.btn_color_black.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        # self.btn_color_brush_red.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        #  self.btn_color_brush_black.clicked.connect(lambda: self.set_color(QColor(0, 0, 0)))
        self.ui.actionRectangle.triggered.connect(lambda: self.changeTool("draw_rectangle"))
        self.ui.actionChangeColor.triggered.connect(lambda: self.changeColor())
        self.ui.actionEllipse.triggered.connect(lambda: self.changeTool("draw_ellipse"))
        self.ui.actionLine.triggered.connect(lambda: self.changeTool("draw_line"))
        self.ui.actionPoint.triggered.connect(lambda: self.changeTool("draw_point"))
        self.ui.actionFill.triggered.connect(lambda: self.changeTool("draw_fill"))


    def changeTool(self,new_tool_id):
        self.draw_tool_now_id = new_tool_id
        self.draw_tool_now = self.draw_tools[new_tool_id]

    def changeColor(self):
        self.tool_data["color"] = QColorDialog.getColor()

        pixmap = QPixmap(":/tool_bar/tool_collor.png")
        mask = pixmap.createMaskFromColor(QColor(0,0,0),Qt.MaskOutColor)
        pixmap.fill(self.tool_data["color"])
        pixmap.setMask(mask)

        self.ui.actionChangeColor.setIcon(QIcon(pixmap))


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(self.draw_color_now)
        painter.drawPixmap(QPoint(), self.drawing_surface)
        painter.drawPixmap(QPoint(), self.tool_surface)

        painter.end()

    def mousePressEvent(self, event):
        self.draw_tool_now.mouse_press_handler(event)

    def mouseMoveEvent(self, event):
        self.draw_tool_now.mouse_move_handler(event)

    def mouseReleaseEvent(self, event):
        self.draw_tool_now.mouse_release_handler(event)

















#Базовый класс для инструментов
class ToolController:
    def __init__(self,window):
        self.main_window = window
        self.main_surface = window.drawing_surface
    def mouse_press_handler(self, event):
        pass
    def mouse_move_handler(self, event):
        pass
    def mouse_release_handler(self, event):
        pass


#Базовый класс, отвечающий за рисование фигур
class ToolController_Figure(ToolController):
    is_draw_start = False
    is_accumulation = False


    def draw_figure(self, painter):
        pass


    def mouse_press_handler(self, event):
        self.point0 = event.pos()
        self.point1 = event.pos()
        self.is_draw_start = True

        # Поскольку размер фигуры задается перемещением мыши, нет смысла дублировать код
        # который отвечает за отрисовку фигуры на буферной поверхности
        self.mouse_move_handler(event)

    def mouse_move_handler(self, event):
        if self.is_draw_start:
            self.point1 = event.pos()

            # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
            # Затем на ней рисуется, как будет выглядить фигура при текущих параметрах
            painter = QPainter(self.main_window.tool_surface)
            painter.begin(self.main_window.tool_surface)
            painter.setPen(self.main_window.tool_data['color'])

            if (not self.is_accumulation):
                self.main_window.tool_surface.fill(QColor(0, 0, 0, 0))

            self.draw_figure(painter)

            painter.end()
            self.main_window.update()

    def mouse_release_handler(self, event):
        self.is_draw_start = False
        self.point1 = event.pos()

        painter = QPainter(self.main_window.drawing_surface)
        painter.drawPixmap(QPoint(), self.main_window.drawing_surface)
        painter.setPen(self.main_window.tool_data['color'])
        painter.drawPixmap(QPoint(), self.main_window.tool_surface)

        self.main_window.update()


#Инструмент, отвечающий за рисование прямоугольника
class ToolController_Figure_Rectangle(ToolController_Figure):
    def draw_figure(self, painter):
        rect = QRect(self.point0, self.point1)
        painter.drawRect(rect.normalized())


#Инструмент, отвечающий за рисование эллипса
class ToolController_Figure_Ellipse(ToolController_Figure):
    def draw_figure(self, painter):
        rect = QRect(self.point0, self.point1)
        painter.drawEllipse(rect)


#Инструмент, отвечающий за рисование прямой
class ToolController_Figure_Line(ToolController_Figure):
    def draw_figure(self, painter):
        painter.drawLine(self.point0, self.point1)


#Инструмент, отвечающий за рисование точки
class ToolController_Figure_Point(ToolController_Figure):
    def __init__(self,window):
        super(ToolController_Figure_Point, self).__init__(window)
        self.is_accumulation = True

    def draw_figure(self, painter):
        painter.drawLine(self.point0, self.point1)

    def mouse_move_handler(self,event):
        if self.is_draw_start:
            self.point0 = self.point1
        super(ToolController_Figure_Point, self).mouse_move_handler(event)






class ToolController_Fill(ToolController):

    def mouse_press_handler(self, event):

        # Сначала временная поверхность для рисования отчищается в цвет с нулевой прозрачностью
        # Затем на ней рисуется исходное изображение, но с заливкой, как будет выглядить фигура при текущих параметрах
        painter = QPainter(self.main_window.tool_surface)
        painter.begin(self.main_window.tool_surface)
        painter.setPen(self.main_window.tool_data['color'])

        self.main_window.tool_surface.fill(QColor(0, 0, 0, 0))

        # Сама заливка
        image = QImage(self.main_window.drawing_surface)
        set_checked = set()
        set_for_check = set()
        set_for_check.add((event.pos().x(),event.pos().y()))

        while True:
            self.fill(image, painter, image.pixelColor(event.pos()), set_checked, set_for_check, set_for_check.pop())
            if len(set_for_check)==0:
                break



        painter.end()




        self.main_window.update()

    def mouse_release_handler(self, event):
        painter = QPainter(self.main_window.drawing_surface)
        painter.drawPixmap(QPoint(), self.main_window.drawing_surface)
        painter.setPen(self.main_window.tool_data['color'])
        painter.drawPixmap(QPoint(), self.main_window.tool_surface)

        self.main_window.update()





    def fill(self, image, painter, right_color, set_checked,set_for_check,pos):
        set_checked.add(pos)
        painter.drawPoint(int(pos[0]), int(pos[1]))

        for i in (-1,0,1):
            for j in (-1,0,1):
                if not ((pos[0]+i,pos[1]+j) in set_checked) and pos[0]>=0 and pos[1]>=0 and pos[0]<image.width() and pos[1]<image.height() and not (abs(i)==abs(j)):
                    if image.pixelColor(pos[0]+i,pos[1]+j).getRgb() == right_color.getRgb():
                        set_for_check.add((pos[0]+i,pos[1]+j))
