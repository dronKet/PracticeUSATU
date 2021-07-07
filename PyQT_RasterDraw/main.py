from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication

from GUI import Ui_MainWindow
from Logic import MainWindowLogic

QCoreApplication.addLibraryPath('../venv/Lib/site-packages/PyQt5/Qt5/plugins')
app = QApplication([])
ui = Ui_MainWindow()
window = MainWindowLogic(ui)
window.show()
app.exec()

