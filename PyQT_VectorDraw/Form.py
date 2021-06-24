from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget , QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton,QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
import Resources.Icons

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.actionPaletteLine = QtWidgets.QAction(self)
        icon2 = QtGui.QIcon()
        path="C:\\Users\\Динар\\Desktop\\Game_View\\photos\\pallite.PNG"
        icon2.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteLine.setIcon(icon2)
        self.actionPaletteLine.setObjectName("actionPalette")

        self.actionPaletteBrush = QtWidgets.QAction(self)
        icon2 = QtGui.QIcon()
        path="C:\\Users\\Динар\\Desktop\\Game_View\\photos\\pallite.PNG"
        icon2.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaletteBrush.setIcon(icon2)
        self.actionPaletteBrush.setObjectName("actionPalette")

        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionEllips)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.actionPaletteLine)
        self.toolBar.addAction(self.actionPaletteBrush)
        layout = QVBoxLayout()
        self.setLayout(layout)