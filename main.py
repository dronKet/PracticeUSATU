import Window
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window.TableTrajectory()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
