import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,QSpinBox
from PyQt5.QtWidgets import QMainWindow, QColorDialog, QUndoStack, QUndoCommand, QFileDialog, QDialog, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QIcon, QImage, QClipboard
from PyQt5.QtCore import Qt, QPoint, QRect
from .DrawingTools import *
from .GUI import *
#from DrawingTools import ToolController_Select,ToolController_Move,ToolController_Fill,ToolController_Paste
#from DrawingTools import ToolController_Copy,ToolController_Figure_Line,ToolController_Figure_Ellipse
#from DrawingTools import ToolController_Figure_Rectangle,ToolController_Figure_Point,UndoRedoController



class RasterEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RasterEditorWindow()

        self.ui.setupUi(self)
        self.setWindowTitle("This is not a bug, this is a feature")

        self.central_widget = SceneLogic(self)

        # Назначаем обработчики событий
        self.central_widget.add_functions(self.ui)

        scroll_area = QtWidgets.QScrollArea()
        #scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(scroll_area)

        self.setStatusBar(None)

        #scroll_area.resize(200, 200)

        #self.setCentralWidget(self.central_widget)
        #self.setCentralWidget(self.ui.scrollArea)








class SceneLogic(QWidget):
    # Текущий цвет, которым будут рисоваться новые элементы
    draw_color_now = QColor(0, 0, 0)

    # Набор доступных инструментов
    draw_tools = {}

    # Текущий инструмент
    draw_tool_now_id = "draw_rectangle"

    # Путь к файлу, с которым работает программа в данный момент
    worked_file_path = ''

    def __init__(self,window):
        super().__init__()

        self.is_drawing = True
        self.setFixedWidth(900)
        self.setFixedHeight(700)

        self.main_window = window


        # Создаем изображение, на котором будет рисовать пользователь
        self.drawing_surface = QImage(QPixmap(self.rect().size()))
        self.drawing_surface.fill(Qt.white)
        # Создаем буферное изображение для инструментов, оно будет отрисовываться поверх основного
        self.tool_surface = QPixmap(self.rect().size())#QImage(QPixmap(self.rect().size()))
        self.tool_surface.fill(QColor(0, 0, 0, 0))

        #Различная информация для инструментов
        self.tool_data = {}
        self.tool_data.setdefault("color",QColor(0,0,0))

        UndoRedoController.init(self)

        # Инициализируем инструменты
        self.draw_tools.setdefault("none",ToolController(self))
        self.draw_tools.setdefault("draw_rectangle",ToolController_Figure_Rectangle(self))
        self.draw_tools.setdefault("draw_ellipse",ToolController_Figure_Ellipse(self))
        self.draw_tools.setdefault("draw_line",ToolController_Figure_Line(self))
        self.draw_tools.setdefault("draw_point",ToolController_Figure_Point(self))
        self.draw_tools.setdefault("draw_fill",ToolController_Fill(self))
        self.draw_tools.setdefault("select",ToolController_Select(self))
        self.draw_tools.setdefault("copy",ToolController_Copy(self,self.draw_tools["select"]))
        self.draw_tools.setdefault("move",ToolController_Move(self))
        self.draw_tools.setdefault("paste",ToolController_Paste(self,self.draw_tools["move"]))
        self.draw_tools.setdefault("cut",ToolController_Cut(self))
        self.draw_tools.setdefault("delete",ToolController_Delete(self))
        self.draw_tool_now = self.draw_tools["draw_rectangle"]


        # Выводим окно
        self.show()

    def showdialog(self):
        dlg = QDialog()
        dlg.resize(300, 150)
        windowFlag=0
        windowFlag |= Qt.CustomizeWindowHint
        windowFlag |= Qt.WindowCloseButtonHint
        dlg.setWindowFlags(windowFlag)
        label_h = QLabel("Ширина", dlg)
        label_w = QLabel("Длина", dlg)
        label_h.move(25, 25)
        label_w.move(25, 50)
        line_h = QSpinBox(dlg)
        line_h.setRange(1, 100000)
        line_h.move(100, 25)
        line_h.setValue(self.height())
        line_w = QSpinBox(dlg)
        line_w.setRange(1, 100000)
        line_w.setValue(self.width())
        line_w.move(100, 50)
        line_w.setRange(1,100000)
        button_ok = QPushButton(dlg)
        button_ok.setText("Применить")
        button_ok.move(25, 100)
        button_cansel = QPushButton(dlg)
        button_cansel.setText("Отмена")
        button_cansel.move(200, 100)
        button_cansel.clicked.connect(lambda: dlg.reject())
        button_ok.clicked.connect(lambda: dlg.accept())
        button_ok.clicked.connect(lambda: self.change_scene_size(int(line_h.value()), int(line_w.value())))
        dlg.setWindowTitle("Изменить размер изображения")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()


    def change_scene_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)

        old_surf = self.drawing_surface

        # Создаем изображение, на котором будет рисовать пользователь
        self.drawing_surface = QImage(QPixmap(self.rect().size()))
        self.drawing_surface.fill(Qt.white)
        # Создаем буферное изображение для инструментов, оно будет отрисовываться поверх основного
        self.tool_surface = QPixmap(self.rect().size())
        self.tool_surface.fill(QColor(0, 0, 0, 0))

        painter = QPainter(self.drawing_surface)
        painter.drawImage(QPoint(),old_surf)
        self.update()



    def add_functions(self,ui):
        ui.actionRectangle.triggered.connect(lambda: self.changeTool("draw_rectangle"))
        ui.actionChangeColor.triggered.connect(lambda: self.changeColor())
        ui.actionEllipse.triggered.connect(lambda: self.changeTool("draw_ellipse"))
        ui.actionLine.triggered.connect(lambda: self.changeTool("draw_line"))
        ui.actionPoint.triggered.connect(lambda: self.changeTool("draw_point"))
        ui.actionFill.triggered.connect(lambda: self.changeTool("draw_fill"))
        ui.actionDelete.triggered.connect(lambda: self.changeTool("delete"))
        ui.actionSelect.triggered.connect(lambda: self.changeTool("select"))
        ui.actionCopy.triggered.connect(lambda: self.draw_tools["copy"].press_button_handler())
        ui.actionPaste.triggered.connect(lambda: self.draw_tools["paste"].press_button_handler())
        ui.actionCut.triggered.connect(lambda: self.draw_tools["cut"].press_button_handler())
        ui.actionUndo.triggered.connect(lambda: UndoRedoController.undo_redo_stack.undo())
        ui.actionRedo.triggered.connect(lambda: UndoRedoController.undo_redo_stack.redo())
        ui.actionFileSaveAs.triggered.connect(lambda: self.fileSaveAs())
        ui.actionFileSave.triggered.connect(lambda: self.fileSave())
        ui.actionFileOpen.triggered.connect(lambda: self.fileOpen())
        ui.actionChangeSize.triggered.connect(lambda: self.showdialog())


    def fileOpen(self):
        file = QFileDialog.getOpenFileName(self, "", "", "*.png;;*.jpg")
        self.worked_file_path = file

        if not self.worked_file_path=='':
            l=self.worked_file_path[0].split('.')
            print(l[-1])
            self.drawing_surface.load(self.worked_file_path[0],l[-1])

    def fileSave(self):
        if self.worked_file_path=='':
            self.fileSaveAs()
        else:
            l=self.worked_file_path[0].split('.')
            print(l[-1])
            self.drawing_surface.save(self.worked_file_path[0],l[-1])


    def fileSaveAs(self):
        file = QFileDialog.getSaveFileName(self,"","untitled.png","*.png;;*.jpg;;*.*")
        #print(QtGui.QImageWriter.supportedImageFormats())
        if not file=='':
            self.worked_file_path = file
            self.fileSave()





    def changeTool(self,new_tool_id):
        if not self.draw_tool_now_id == new_tool_id:
            self.draw_tool_now.deactivation_this_tool()
            self.draw_tool_now_id = new_tool_id
            self.draw_tool_now = self.draw_tools[new_tool_id]
            self.draw_tool_now.activation_this_tool()

    def changeColor(self):
        self.tool_data["color"] = QColorDialog.getColor()

        pixmap = QPixmap(":/tool_bar/tool_collor.png")
        mask = pixmap.createMaskFromColor(QColor(0,0,0),Qt.MaskOutColor)
        pixmap.fill(self.tool_data["color"])
        pixmap.setMask(mask)

        self.main_window.ui.actionChangeColor.setIcon(QIcon(pixmap))


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setPen(self.draw_color_now)
        painter.drawImage(QPoint(), self.drawing_surface)
        painter.drawPixmap(QPoint(), self.tool_surface)

        painter.end()
        self.update()

    def mousePressEvent(self, event):
        self.draw_tool_now.mouse_press_handler(event)
        self.update()

    def mouseMoveEvent(self, event):
        self.draw_tool_now.mouse_move_handler(event)
        self.update()

    def mouseReleaseEvent(self, event):
        self.draw_tool_now.mouse_release_handler(event)
        self.update()