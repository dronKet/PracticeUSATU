import sys
import numpy as np
import pyqtgraph as pg
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def read_file(file):
    name = ""
    coord = np.ndarray((0, 3))
    with open(file, mode='r') as f:
        for line_num, line in enumerate(f.readlines()):
            if line_num == 1:
                name = line.split()[3]
            elif line_num >= 12:
                splitted = line.split()
                x = float(splitted[1])
                y = float(splitted[2])
                z = float(splitted[3])
                coord = np.append(coord, [[x, y, z]], axis=0)
    return name, coord

class WellItem(QStandardItem):
    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.data = None
        self.plotItem = None
        self.textItem = None

    def set_data(self, data):
        self.data = data

    def set_plot_item(self, plot_item, text_item):
        self.plotItem = plot_item
        self.textItem = text_item

    def get_data(self):
        return self.data


class WellContainerItem(QStandardItem):
    def __init__(self):
        super().__init__()
        self.setCheckable(False)



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num_color = 0
        self.resize(1600, 900)
        splitter = QSplitter()
        self.setCentralWidget(splitter)

        self.treeView = QTreeView(self)
        self.treeView.setHeaderHidden(True)
        self.treeModel = None

        self.deleteWell = QAction("Удалить")
        self.deleteWell.triggered.connect(self.delete_selected_well)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.show_context_menu)

        self.tableView = QTableView(self)

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.showGrid(x=True, y=True, alpha=0.5)

        splitter.addWidget(self.treeView)
        splitter.addWidget(self.tableView)
        splitter.addWidget(self.plotWidget)

        self.toolbar = self.addToolBar("")
        self.toolbar.addAction("Открыть").triggered.connect(self.load_project_file)
        self.toolbar.addAction("Создать").triggered.connect(self.create_project_file)
        self.toolbar.addAction("Добавить скважины").triggered.connect(self.load_new_wells)

        self.projectPath = None

    def create_project_file(self):
        self.projectPath, tmp = QFileDialog.getSaveFileName(None, "Выберите местоположение файла и назовите его")
        self.create_new_project()

    def load_project_file(self):
        self.projectPath, tmp = QFileDialog.getOpenFileName(None, "Выберите проект")
        self.create_new_project()

    def load_new_wells(self):
        files, tmp = QFileDialog.getOpenFileNames(None, "Выберите файлы:")

        if not files:
            return

        container = self.create_container(str(datetime.today()))
        for file in files:
            name, coord = read_file(file)
            well = self.create_well(container)
            well.setText(name)
            well.set_data(coord)

    def delete_selected_well(self):
        well_idx = self.treeView.currentIndex()
        well = self.treeModel.itemFromIndex(well_idx)
        self.plotWidget.removeItem(well.plotItem)
        self.plotWidget.removeItem(well.textItem)
        well.parent().removeRow(well.row())

    def create_new_project(self):
        if self.projectPath:
            self.treeModel = QStandardItemModel()
            self.treeModel.dataChanged.connect(self.on_data_changed)
            self.treeView.setModel(self.treeModel)

    def on_data_changed(self, top_left, bottom_right, roles):
        if Qt.CheckStateRole in roles:
            item = self.treeModel.itemFromIndex(top_left)
            if type(item) is WellItem:
                if item.checkState() == Qt.Checked:
                    coord = item.get_data()[:, :2]
                    point = coord[-1]
                    plot_item = pg.PlotDataItem(coord, pen=1)
                    text_item = pg.TextItem(item.text(), anchor=(1, 1))
                    text_item.setPos(point[0], point[1])
                    item.set_plot_item(plot_item, text_item)
                    self.plotWidget.addItem(plot_item)
                    self.plotWidget.addItem(text_item)
                else:
                    self.plotWidget.removeItem(item.plotItem)
                    self.plotWidget.removeItem(item.textItem)
                    item.set_plot_item(None, None)

    def create_container(self, name):
        container = WellContainerItem()
        container.setText(name)
        self.treeModel.appendRow(container)
        return container

    def create_well(self, container_item):
        well = WellItem()
        container_item.appendRow(well)
        return well

    def show_context_menu(self, position):
        _contextMenu = QMenu()
        _contextMenu.addAction(self.deleteWell)
        self.deleteWell.setEnabled(False)
        idx = self.treeView.currentIndex()
        # Проверка на действительность индекса
        if not idx.isValid():
            return
        # Проверка на действительность индекса родителя
        if idx.parent().isValid():
            self.deleteWell.setEnabled(True)
        _contextMenu.exec_(self.treeView.viewport().mapToGlobal(position))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
