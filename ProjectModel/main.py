import sys
import numpy as np
import pyqtgraph as pg
import uuid
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from VectorRasterEditors.GraphicsEditors import VectorEditor
from VectorRasterEditors.GraphicsEditors import RasterEditor

QCoreApplication.addLibraryPath('../venv/Lib/site-packages/PyQt5/Qt5/plugins')


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
        self.id = None
        self.setCheckable(True)
        self.data = None
        self.plotItem = None
        self.textItem = None

    def set_data(self, data):
        self.data = data

    def set_plot_item(self, plot_item, text_item):
        self.plotItem = plot_item
        self.textItem = text_item

    def set_id(self, well_id):
        self.id = well_id

    def get_data(self):
        return self.data

    def get_id(self):
        return self.id


class WellContainerItem(QStandardItem):
    def __init__(self):
        super().__init__()
        self.id = None
        self.setCheckable(False)

    def set_id(self, container_id):
        self.id = container_id

    def get_id(self):
        return self.id


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.num_color = 0
        self.resize(1600, 900)
        splitter = QSplitter()
        self.setCentralWidget(splitter)

        self.treeView = QTreeView(self)
        self.treeView.setHeaderHidden(True)
        self.deleteWell = QAction("Удалить")
        self.deleteWell.triggered.connect(self.delete_selected_well)
        self.addWellIcon = QAction("Добавить иконку")
        self.addWellIcon.triggered.connect(self.load_icon)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.show_context_menu)
        self.treeModel = None

        self.icon_path = None


        self.db = None
        self.tableView = QTableView(self)
        self.folderModel = None
        self.folderTableName = "Folders"
        self.wellModel = None
        self.wellTableName = "Wells"
        self.trajectoriesModel = None
        self.trajectoriesTableName = "Trajectories"

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.showGrid(x=True, y=True, alpha=0.5)

        splitter.addWidget(self.treeView)
        splitter.addWidget(self.tableView)
        splitter.addWidget(self.plotWidget)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction("Открыть").triggered.connect(self.load_project_file)
        self.toolbar.addAction("Создать").triggered.connect(self.create_project_file)
        self.toolbar.addAction("Добавить скважины").triggered.connect(self.load_new_wells)
        self.toolbar.addAction("Векторный редактор").triggered.connect(VectorEditor)
        self.toolbar.addAction("Растровый редактор").triggered.connect(RasterEditor)
        # self.toolbar.addAction("Сохранить план").triggered.connect()

        self.projectPath = None

    def create_project_file(self):
        self.projectPath, tmp = QFileDialog.getSaveFileName(None, "Создайте проект")
        if not self.projectPath:
            return

        open(self.projectPath, mode='w').close()
        self.connect_database()
        self.db.exec(f'CREATE TABLE {self.folderTableName}(IdFolder VARCHAR(40), '
                     f'Name VARCHAR(40))')
        self.db.exec(f'CREATE TABLE {self.wellTableName}(IdFolder VARCHAR(40), '
                     f'IdWell VARCHAR(40), Name VARCHAR(40))')
        self.db.exec(f'CREATE TABLE {self.trajectoriesTableName}(IdWell VARCHAR(40), '
                     f'X REAL, Y REAL, Z REAL)')
        self.create_table_model()

    def load_project_file(self):
        self.projectPath, tmp = QFileDialog.getOpenFileName(None, "Откройте проект")
        if not self.projectPath:
            return

        self.connect_database()
        self.create_table_model()
        self.load_table_models_from_db()

    def connect_database(self):
        if self.projectPath:
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            self.db.setDatabaseName(self.projectPath)
            if not self.db.open():
                QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                     qApp.tr("Unable to establish a database connection.\n"
                                             "This example needs SQLite support. Please read "
                                             "the Qt SQL driver documentation for information "
                                             "how to build it.\n\n"
                                             "Click Cancel to exit."),
                                     QMessageBox.Cancel)

    def create_table_model(self):
        self.folderModel = QSqlTableModel(None, self.db)
        self.folderModel.setTable(self.folderTableName)
        self.folderModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.folderModel.select()

        self.wellModel = QSqlTableModel(None, self.db)
        self.wellModel.setTable(self.wellTableName)
        self.wellModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.wellModel.select()

        self.trajectoriesModel = QSqlTableModel(None, self.db)
        self.trajectoriesModel.setTable(self.trajectoriesTableName)
        self.trajectoriesModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.trajectoriesModel.select()

        self.fetch_more_rows_in_tables()

        self.treeModel = QStandardItemModel()
        self.treeModel.dataChanged.connect(self.on_data_changed)
        self.treeView.setModel(self.treeModel)

    def load_table_models_from_db(self):
        row_count = self.folderModel.rowCount()
        for i in range(row_count):
            folder_id = self.folderModel.index(i, 0).data(Qt.EditRole)
            folder_name = self.folderModel.index(i, 1).data(Qt.EditRole)
            container = self.create_model_container(folder_name, folder_id)

            well_num_row_list = self.wellModel.match(self.wellModel.index(0, 0), Qt.EditRole, folder_id, hits=-1)
            for well_num_row in well_num_row_list:
                well_id = self.wellModel.index(well_num_row.row(), 1).data(Qt.EditRole)
                well_name = self.wellModel.index(well_num_row.row(), 2).data(Qt.EditRole)

                trajectories_num_row_list = self.trajectoriesModel.match(self.trajectoriesModel.index(0, 0),
                                                                         Qt.EditRole, well_id, hits=-1)
                coord = np.ndarray((0, 3))
                for trajectories_num_row in trajectories_num_row_list:
                    x = self.trajectoriesModel.index(trajectories_num_row.row(), 1).data(Qt.EditRole)
                    y = self.trajectoriesModel.index(trajectories_num_row.row(), 2).data(Qt.EditRole)
                    z = self.trajectoriesModel.index(trajectories_num_row.row(), 3).data(Qt.EditRole)
                    coord = np.append(coord, [[x, y, z]], axis=0)
                self.create_model_well(container, well_name, coord, well_id)

    def load_new_wells(self):
        files, tmp = QFileDialog.getOpenFileNames(None, "Выберите файлы")

        if not files:
            return

        self.treeView.setUpdatesEnabled(False)
        container_name = str(datetime.today())
        container_id = str(uuid.uuid4())
        container = self.create_model_container(container_name, container_id)
        self.create_db_container(container_name, container_id)
        for file in files:
            name, coord = read_file(file)
            well_id = str(uuid.uuid4())
            self.create_model_well(container, name, coord, well_id)
            self.create_db_well(container, name, coord, well_id)
        self.folderModel.submitAll()
        self.wellModel.submitAll()
        self.trajectoriesModel.submitAll()
        self.treeView.setUpdatesEnabled(True)
        self.fetch_more_rows_in_tables()

    def create_model_container(self, name, container_id):
        container = WellContainerItem()
        container.setText(name)
        container.set_id(container_id)
        self.treeModel.appendRow(container)
        return container

    def create_db_container(self, name, container_id):
        record = QSqlRecord()
        record.append(QSqlField("IdFolder"))
        record.append(QSqlField("Name"))
        record.setValue("IdFolder", container_id)
        record.setValue("Name", name)
        self.folderModel.insertRecord(-1, record)

    def create_model_well(self, container_item, name, coord, well_id):
        well = WellItem()
        well.setText(name)
        well.set_data(coord)
        well.set_id(well_id)
        container_item.appendRow(well)
        return well

    def create_db_well(self, container_item, name, coord, well_id):
        record = QSqlRecord()
        record.append(QSqlField("IdFolder"))
        record.append(QSqlField("IdWell"))
        record.append(QSqlField("Name"))
        record.setValue("IdFolder", container_item.get_id())
        record.setValue("IdWell", well_id)
        record.setValue("Name", name)
        self.wellModel.insertRecord(-1, record)

        for X, Y, Z in coord:
            record = QSqlRecord()
            record.append(QSqlField("IdWell"))
            record.append(QSqlField("X"))
            record.append(QSqlField("Y"))
            record.append(QSqlField("Z"))
            record.setValue("IdWell", well_id)
            record.setValue("X", float(X))
            record.setValue("Y", float(Y))
            record.setValue("Z", float(Z))
            self.trajectoriesModel.insertRecord(-1, record)

    def load_icon(self):
        well_idx = self.treeView.currentIndex()
        well = self.treeModel.itemFromIndex(well_idx)
        file = QFileDialog.getOpenFileName(self, "", "", "*.png;;*.jpg")
        self.icon_path = file

        if not self.icon_path == '':
            l = self.icon_path[0].split('.')
            # pixmap=QPixmap()
            # pixmap.load(self.icon_path[0], l[-1])
            icon = QIcon(self.icon_path[0])
            well.setIcon(icon)

    def show_context_menu(self, position):
        _contextMenu = QMenu()
        _contextMenu.addAction(self.deleteWell)
        _contextMenu.addAction(self.addWellIcon)
        self.deleteWell.setEnabled(False)
        idx = self.treeView.currentIndex()

        if not idx.isValid():
            return

        if idx.parent().isValid():
            self.deleteWell.setEnabled(True)
        _contextMenu.exec_(self.treeView.viewport().mapToGlobal(position))

    def delete_selected_well(self):
        well_idx = self.treeView.currentIndex()
        well = self.treeModel.itemFromIndex(well_idx)
        well_id = well.get_id()
        self.plotWidget.removeItem(well.plotItem)
        self.plotWidget.removeItem(well.textItem)
        well.parent().removeRow(well.row())

        well_idx_list = self.wellModel.match(self.wellModel.index(0, 1), Qt.EditRole, well_id, hits=-1)
        for well_idx in well_idx_list:
            self.wellModel.removeRow(well_idx.row())
        trajectories_id_list = self.trajectoriesModel.match(self.trajectoriesModel.index(0, 0), Qt.EditRole, well_id,
                                                            hits=-1)
        for trajectories_id in trajectories_id_list:
            self.trajectoriesModel.removeRows(trajectories_id.row(), 1)
        self.wellModel.submitAll()
        self.trajectoriesModel.submitAll()
        self.fetch_more_rows_in_tables()

    def fetch_more_rows_in_tables(self):
        while self.folderModel.canFetchMore():
            self.folderModel.fetchMore()
        while self.wellModel.canFetchMore():
            self.wellModel.fetchMore()
        while self.trajectoriesModel.canFetchMore():
            self.trajectoriesModel.fetchMore()

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
                    icon = item.icon()
                    pixmap = icon.pixmap(24, 24)
                    # Нужно создать Item картинки, добавить удаление
                else:
                    self.plotWidget.removeItem(item.plotItem)
                    self.plotWidget.removeItem(item.textItem)
                    item.set_plot_item(None, None)
        if Qt.DecorationRole in roles:
            item = self.treeModel.itemFromIndex(top_left)
            if type(item) is WellItem:
                pass
                # Получение иконки


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
