from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from GUI import Ui_MainWindow
from Logic import MainWindowLogic


app = QApplication([])
ui = Ui_MainWindow()
window = MainWindowLogic(ui)
app.exec()

