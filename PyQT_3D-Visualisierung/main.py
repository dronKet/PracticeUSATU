import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow

def file_reading(files):
    data = {}
    for file in files:
        f = open(file, mode='r')
        array_list = []
        for linenum, line in enumerate(f.readlines()):
            if linenum == 1:
                name = line.split()[3]
            if linenum >= 12:
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
    window = QMainWindow
    window.setGeometry(300, 250, 350, 200)
    window.show()

    #files = QFileDialog.getOpenFileNames(None, "Выберите файлы:", "", "Text files (*.dev)")
    #print(file_reading(files[0]))
    sys.exit(app.exec_())