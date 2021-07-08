import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtSvg import QSvgGenerator, QSvgRenderer
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog, \
    QMainWindow, QFormLayout, QGroupBox, QLabel, QScrollArea, QFileDialog, QDialog, QLineEdit, QSpinBox
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QPen, QIcon
from PyQt5.QtCore import Qt, QPoint, QRect, QLineF, pyqtSignal, QSize
from Form import Ui_MainWindow
from Controllers import *


class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.widget = DrawingScene()
        self.main_area=self.widget.main_area
        self.rect_size=self.widget.rect().size()
        self.widget.add_functions(self.ui)
        # self.setCentralWidget(self.widget)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)
        self.setCentralWidget(scroll)
        self.setStatusBar(None)


class DrawingScene(QWidget):
    def __init__(self):
        super().__init__()
        self.tools = {}
        # self.tools["fill"]=ControllerFill(self)
        # self.tools["change_color"]=ControllerChangeColor(self)
        self.brush_color = QColor(255, 255, 255)
        self.file_path = ''
        self.line_color = QColor(0, 0, 0)
        self.color = QColor(0, 0, 0)
        self.shapes = list()
        self.excretion_coords = False
        self.main_area = QPixmap(self.rect().size())
        self.main_area.fill(Qt.white)
        self.painter=QPainter(self.main_area)
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
        self.tools["delete"] = ControllerDelete(self)
        self.tools["copy/paste"] = ControllerCopyPaste(self)
        self.tools["cut"] = ControllerCut(self)
        self.default_w=self.width()
        self.default_h=self.height()
        self.shapes_op = ShapesOperations()

    def showdialog(self):
        dlg = QDialog()
        dlg.resize(300, 200)

        label_w = QLabel("Ширина", dlg)
        label_h = QLabel("Длина", dlg)
        label_w.move(25, 50)
        label_h.move(25, 100)
        line_w = QSpinBox(dlg)
        line_h = QSpinBox(dlg)
        line_w.setRange(1,5000)
        line_h.setRange(1, 5000)
        #line_w.setValue(self.width())
        line_w.setValue(self.main_area.width())
        #line_h.setValue(self.height())
        line_h.setValue(self.main_area.height())
        line_w.move(100, 50)
        line_h.move(100, 100)
        button_ok = QPushButton(dlg)
        button_ok.setText("Применить")
        button_ok.move(25, 150)

        button_default = QPushButton(dlg)
        button_default.setText("По умолчанию")
        button_default.move(100, 150)
        #button_cancel = QPushButton(dlg)
        #button_cancel.setText("Отмена")
        #button_cancel.move(200, 100)
        #button_cancel.clicked.connect(dlg.reject)
       # button_ok.clicked.connect(dlg.accept)
        button_default.clicked.connect(lambda: self.change_scene_size(self.default_w, self.default_h))
        button_ok.clicked.connect(lambda: self.change_scene_size(line_w.value(), line_h.value()))
        dlg.setWindowTitle("Смена размера сцена")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()

    def change_scene_size(self, width, height):
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.main_area = QPixmap(self.rect().size())
        self.main_area.fill(Qt.white)
        self.external_area = QPixmap(self.rect().size())
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.shapes_op.draw_only_shapes_array(self.shapes, self, QPainter(self.main_area))

    def add_functions(self, ui):
        ui.actionRectangle.triggered.connect(lambda: self.change_tool("rectangle"))
        ui.actionEllips.triggered.connect(lambda: self.change_tool("ellips"))
        ui.lineAction.triggered.connect(lambda: self.change_tool("line"))
        # self.ui.actionPalette.triggered.connect(lambda: self.change_tool("change_color"))
        ui.selectAction.triggered.connect(lambda: self.change_tool("select"))
        ui.moveAction.triggered.connect(lambda: self.change_tool("move"))
        ui.fillAction.triggered.connect(lambda: self.tools["fill"].fill(self.color))
        ui.actionPalette.triggered.connect(lambda: self.change_color(ui))
        ui.copyAction.triggered.connect(self.tools["copy/paste"].copy)
        ui.pasteAction.triggered.connect(self.tools["copy/paste"].paste)
        ui.deleteAction.triggered.connect(self.tools["delete"].delete_shapes)
        ui.cutAction.triggered.connect(self.tools["cut"].cut_shapes)
        ui.actionCleanWindow.triggered.connect(self.clean_window)
        ui.undoAction.triggered.connect(self.undo_redo.undo_redo_stack.undo)
        ui.redoAction.triggered.connect(self.undo_redo.undo_redo_stack.redo)
        # ui.changeSizeAction.triggered.connect(self.change_scene_size)
        ui.changeSizeAction.triggered.connect(self.showdialog)
        ui.saveAction.triggered.connect(self.fileSave)
        ui.saveAsAction.triggered.connect(self.fileSaveAs)
        ui.loadAction.triggered.connect(self.fileLoad)

    def fileLoad(self):
        file = QFileDialog.getOpenFileName(self, "", "", "*.svg;;*.pdf;;*.png;;*.jpg")
        self.file_path = file

        if not self.file_path == '':
            path_list = self.file_path[0].split('.')
            print(path_list[-1])
            image = QIcon(self.file_path[0]).pixmap(QSize())
            if path_list[-1] == 'svg':
                renderer = QSvgRenderer(self.file_path[0])
                print(self.file_path[0])
                self.main_area = QPixmap(self.rect().size())
                self.main_area.fill(Qt.white);
                painter = QPainter(self.main_area)
                renderer.render(painter)
                self.update()
            else:
                self.main_area.load(self.file_path[0], path_list[-1])

    def fileSave(self):
        if self.file_path == '':
            self.fileSaveAs()
        else:
            path_list = self.file_path[0].split('.')
            if path_list[-1] == 'svg':
                self.generate_svg()
            elif path_list[-1] == 'pdf':
                self.generate_pdf()
            else:
                self.main_area.save(self.file_path[0], path_list[-1])

    def generate_pdf(self):
        printer = QPrinter()
        printer.setOutputFileName(self.file_path[0])
        pdf_painter = QPainter(printer)
        pdf_painter.fillRect(QRect(0, 0, self.width(), self.height()), Qt.white)
        self.shapes_op.draw_only_shapes_array(self.shapes, self, pdf_painter)
        # self.shapes[0].draw(svg_painter)
        pdf_painter.end()

    def generate_svg(self):
        generator = QSvgGenerator()
        generator.setFileName(self.file_path[0])
        generator.setSize(QSize(self.width(), self.height()))
        generator.setViewBox(QRect(0, 0, self.width(), self.height()))
        svg_painter = QPainter(generator)
        svg_painter.fillRect(QRect(0, 0, self.width(), self.height()), Qt.white)
        self.shapes_op.draw_only_shapes_array(self.shapes, self, svg_painter)
        # self.shapes[0].draw(svg_painter)
        svg_painter.end()

    def fileSaveAs(self):
        file = QFileDialog.getSaveFileName(self, "", "untitled.svg", "*.svg;;*.pdf;;*.png;;*.jpg;;*.*")
        # print(QtGui.QImageWriter.supportedImageFormats())
        if not file == '':
            self.file_path = file
            self.fileSave()

    def change_tool(self, name_of_tool):
        self.current_tool = self.tools[name_of_tool]

    def change_color(self, ui):
        color = QColorDialog.getColor()
        self.color = color
        icon_pix = QPixmap(self.rect().size())
        icon_pix.fill(color)
        ui.paletteIcon.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ui.actionPalette.setIcon(ui.paletteIcon)

    def clean_window(self):
        self.main_area.fill(Qt.white)
        self.external_area.fill(QColor(0, 0, 0, 0))
        self.update()
        self.shapes.clear()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.main_area)
        painter.drawPixmap(QPoint(), self.external_area)

    def mousePressEvent(self, event):
        # fill_control=ControllerFill(self)
        if event.buttons() & Qt.LeftButton:
            self.current_tool.mouse_press_handler(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.current_tool.mouse_move_handler(event)

    def mouseReleaseEvent(self, event):
        self.current_tool.mouse_release_handler(event)


if __name__ == "__main__":
    from Controllers import *
    import sys

    app = QApplication([])
    window = VectorEditorWindow()
    window.show()
    app.exec()
