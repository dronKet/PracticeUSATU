from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
import Resources.Icons


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.brush_color = QColor(255, 255, 255)
        self.line_color = QColor(0, 0, 0)
        self.window_width, self.window_height = 800, 480
        self.setMinimumSize(self.window_width, self.window_height)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionEllips = QtWidgets.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ToolBar/ellips.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEllips.setIcon(icon)
        self.actionEllips.setObjectName("actionEllips")

        self.actionRectangle = QtWidgets.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ToolBar/rect.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRectangle.setIcon(icon1)
        self.actionRectangle.setObjectName("actionRectangle")

        icon_pix = QPixmap(self.rect().size())
        self.actionPaletteLine = QtWidgets.QAction(self)
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteLine.setIcon(self.icon2)
        self.actionPaletteLine.setObjectName("actionPalette")

        self.actionPaletteBrush = QtWidgets.QAction(self)
        self.icon3 = QtGui.QIcon()
        self.icon3.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteBrush.setIcon(self.icon3)
        self.actionPaletteBrush.setObjectName("highlight")

        icon_pix.fill(QColor(125, 125, 125))
        label = QLabel()
        label.setText("haha")
        label.setPixmap(icon_pix)
        #icon_pix
        self.actionChooseShape = QtWidgets.QAction(self)
        self.icon4 = QtGui.QIcon()
        self.icon4.addPixmap(QtGui.QPixmap(":/Resources/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChooseShape.setIcon(self.icon4)
        self.actionChooseShape.setObjectName("highlight")

        self.actionBrushShape = QtWidgets.QAction(self)
        self.brushIcon = QtGui.QIcon()
        self.brushIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBrushShape.setIcon(self.brushIcon)
        self.actionBrushShape.setObjectName("brushShape")

        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionEllips)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.actionPaletteLine)
        self.toolBar.addAction(self.actionPaletteBrush)
        self.toolBar.addAction(self.actionBrushShape)
        layout = QVBoxLayout()
        self.setLayout(layout)