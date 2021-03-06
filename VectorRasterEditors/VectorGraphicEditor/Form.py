from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
from .Resources.Icons import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.window_width, self.window_height = 800, 480
        MainWindow.setMinimumSize(self.window_width, self.window_height)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.saveAction = QtWidgets.QAction(MainWindow)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(":/ToolBar/rect.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionSave.setIcon(icon1)
        self.saveAction.setObjectName("actionSave")

        self.saveAsAction = QtWidgets.QAction(MainWindow)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(":/ToolBar/rect.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionSave.setIcon(icon1)
        self.saveAsAction.setObjectName("actionSaveAs")

        self.loadAction = QtWidgets.QAction(MainWindow)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(":/ToolBar/rect.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.actionSave.setIcon(icon1)
        self.loadAction.setObjectName("actionSave")

       # self.menubar = QtWidgets.QMenuBar(MainWindow)
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionEllips = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ToolBar/ellips.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEllips.setIcon(icon)
        self.actionEllips.setObjectName("actionEllips")

        self.actionRectangle = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/ToolBar/rect.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRectangle.setIcon(icon1)
        self.actionRectangle.setObjectName("actionRectangle")

        icon_pix = QPixmap(MainWindow.rect().size())
        self.actionPalette = QtWidgets.QAction(MainWindow)
        self.paletteIcon = QtGui.QIcon()
        self.paletteIcon.addPixmap(QtGui.QPixmap(icon_pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPalette.setIcon(self.paletteIcon)
        self.actionPalette.setObjectName("actionPalette")

        self.actionCleanWindow = QtWidgets.QAction(MainWindow)
        self.cleanIcon = QtGui.QIcon()
        self.cleanIcon.addPixmap(QtGui.QPixmap(":/ToolBar/clean.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCleanWindow.setIcon(self.cleanIcon)
        self.actionCleanWindow.setObjectName("chooseShape")

        self.lineAction = QtWidgets.QAction(MainWindow)
        self.lineIcon = QtGui.QIcon()
        #self.lineIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lineAction.setIcon(self.lineIcon)
        self.lineAction.setObjectName("actionline")

        self.moveAction = QtWidgets.QAction(MainWindow)
        self.moveIcon = QtGui.QIcon()
        #self.lineIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moveAction.setIcon(self.moveIcon)
        self.moveAction.setObjectName("actionmove")

        self.undoAction = QtWidgets.QAction(MainWindow)
        self.undoIcon = QtGui.QIcon()
        #self.lineIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoAction.setIcon(self.undoIcon)
        self.undoAction.setObjectName("actionundo")

        self.redoAction = QtWidgets.QAction(MainWindow)
        self.redoIcon = QtGui.QIcon()
        #self.lineIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redoAction.setIcon(self.redoIcon)
        self.redoAction.setObjectName("actionredo")

        self.selectAction = QtWidgets.QAction(MainWindow)
        self.selectIcon = QtGui.QIcon()
        self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectAction.setIcon(self.selectIcon)
        self.selectAction.setObjectName("selectaction")

        self.fillAction = QtWidgets.QAction(MainWindow)
        self.fillIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fillAction.setIcon(self.fillIcon)
        self.fillAction.setObjectName("selectaction")

        self.changeSizeAction = QtWidgets.QAction(MainWindow)
        self.changeSizeActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeSizeAction.setIcon(self.changeSizeActionIcon)
        self.changeSizeAction.setObjectName("changesizeaction")

        self.copyAction = QtWidgets.QAction(MainWindow)
        self.copyActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copyAction.setIcon(self.copyActionIcon)
        self.copyAction.setObjectName("copyaction")

        self.pasteAction = QtWidgets.QAction(MainWindow)
        self.pasteActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pasteAction.setIcon(self.pasteActionIcon)
        self.pasteAction.setObjectName("changesizeaction")

        self.deleteAction = QtWidgets.QAction(MainWindow)
        self.deleteActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteAction.setIcon(self.deleteActionIcon)
        self.deleteAction.setObjectName("deleteaction")

        self.cutAction = QtWidgets.QAction(MainWindow)
        self.cutActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cutAction.setIcon(self.cutActionIcon)
        self.cutAction.setObjectName("deleteaction")

        self.changeSizeAction = QtWidgets.QAction(MainWindow)
        self.changeSizeActionIcon = QtGui.QIcon()
        #self.selectIcon.addPixmap(QtGui.QPixmap(":/ToolBar/choose.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeSizeAction.setIcon(self.changeSizeActionIcon)
        self.changeSizeAction.setObjectName("changesizeaction")

        '''actionFile = self.toolBar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction(self.saveAction)
        actionFile.addAction(self.saveAsAction)
        actionFile.addAction(self.loadAction)
        actionFile.addSeparator()'''


        #self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionEllips)
        self.toolBar.addAction(self.actionRectangle)
        self.toolBar.addAction(self.lineAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.selectAction)
        self.toolBar.addAction(self.moveAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPalette)
        self.toolBar.addAction(self.fillAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.undoAction)
        self.toolBar.addAction(self.redoAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.changeSizeAction)
        self.toolBar.addAction(self.actionCleanWindow)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.copyAction)
        self.toolBar.addAction(self.pasteAction)
        self.toolBar.addAction(self.deleteAction)
        self.toolBar.addAction(self.cutAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction("New")
        self.toolBar.addAction(self.saveAction)
        self.toolBar.addAction(self.saveAsAction)
        self.toolBar.addAction(self.loadAction)

        layout = QVBoxLayout()
        MainWindow.setLayout(layout)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.lineAction.setText(_translate("MainWindow", "Line"))
        self.moveAction.setText(_translate("MainWindow", "Move"))
        self.undoAction.setText(_translate("MainWindow", "Undo"))
        self.redoAction.setText(_translate("MainWindow", "Redo"))
        self.selectAction.setText(_translate("MainWindow", "Select"))
        self.fillAction.setText(_translate("MainWindow", "Fill"))
        self.saveAction.setText(_translate("MainWindow", "Save"))
        self.loadAction.setText(_translate("MainWindow", "Load"))
        self.saveAsAction.setText(_translate("MainWindow", "SaveAs"))
        self.changeSizeAction.setText(_translate("MainWindow", "ChangeSize"))
        self.copyAction.setText(_translate("MainWindow", "Copy"))
        self.pasteAction.setText(_translate("MainWindow", "Paste"))
        self.deleteAction.setText(_translate("MainWindow", "Delete"))
        self.cutAction.setText(_translate("MainWindow", "Cut"))
      #  self.actionRectangle.setText(_translate("MainWindow", "Rectangle"))
       # self.actionEllips.setText(_translate("MainWindow", "Ellips"))
       # self.actionEllips.setToolTip(_translate("MainWindow", "Ellips"))
       # self.actionChangeColor.setText(_translate("MainWindow", "ChangeColor"))
       # self.actionChangeColor.setToolTip(_translate("MainWindow", "ChangeColor"))