import numpy as np
import sys
from PyQt5.QtWidgets import QFileDialog, QApplication

def file_reading(files):
    data = {}
    for filename in argv:
        filepath = "deviation/" + filename + ".dev"
        f = open(filepath, mode='r')
        for i in range(12):
            line = f.readline()
            if i == 2:
                name = line.split()[3]
                print(name)
        Z = np.array([np.array([float(line.split()[1]), float(line.split()[2]), float(line.split()[3])]) for line in f.readlines()])
        data[filename] = Z
    return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    files = QFileDialog.getOpenFileNames(None, "Выберите файлы:", "", "Text files (*.dev)")
    sys.exit(app.exec_())