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

        self.actionChooseShape = QtWidgets.QAction(self)
        self.chooseIcon = QtGui.QIcon()
        self.chooseIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChooseShape.setIcon(self.chooseIcon)
        self.actionChooseShape.setObjectName("chooseShape")

        self.actionCleanWindow = QtWidgets.QAction(self)
        self.cleanIcon = QtGui.QIcon()
        self.cleanIcon.addPixmap(QtGui.QPixmap(":/ToolBar/clean.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCleanWindow.setIcon(self.cleanIcon)
        self.actionCleanWindow.setObjectName("chooseShape")

        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionEllips)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.actionPaletteLine)
        self.toolBar.addAction(self.actionPaletteBrush)
        self.toolBar.addAction(self.actionChooseShape)
        self.toolBar.addAction(self.actionCleanWindow)
        layout = QVBoxLayout()
        self.setLayout(layout)