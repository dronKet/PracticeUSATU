import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 50, 1280, 960)

        btn = QtWidgets.QPushButton(self)
        btn.move(10,10)
        btn.setText("Выбрать файлы")
        btn.adjustSize()
        btn.clicked.connect(self.get_file_names)

    def get_file_names(self):
        files = QFileDialog.getOpenFileNames(None, "Выберите файлы:", "", "Text files (*.dev)")
        print(self.file_reading(files[0]))

    def file_reading(self, files):
        data = {}
        for file in files:
            f = open(file, mode='r')
            array_list = []
            for linenum, line in enumerate(f.readlines()):
                if linenum == 1:
                    name = line.split()[3]
                elif linenum >= 12:
                    x = float(line.split()[1])
                    y = float(line.split()[2])
                    z = float(line.split()[3])
                    array = np.array([x, y, z])
                    array_list.append(array)
            array_array = np.array(array_list)
            data[name] = array_array
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())