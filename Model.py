from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QMessageBox, qApp

testData = [[155493.83000, 139550.56000, 55.430000000],
            [155493.83000, 139550.56000, 45.430000000],
            [153.43494879, 0.0640584421, 0.1921753287],
            [155493.84000, 139550.54000, 35.430000000],
            [155493.81000, 139550.52000, 25.430000000],
            [155493.79000, 139550.56000, 15.430000000],
            [155493.85000, 139550.59000, 5.4300000000]]

testData2 = [[155493.0, 139550.56000, 55.430000000],
             [155493.83000, 139550.56000, 45.430000000],
             [153.43494879, 0.0640584421, 0.0],
             [155493.84000, 139550.54000, 35.430000000],
             [155493.81000, 139550.52000, 25.430000000],
             [0, 139550.56000, 15.430000000],
             [155493.85000, 139550.59000, 5.4300000000]]


class Model(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tableName = "trajectory"
        self.dataBaseName = ":memory:"
        self.connectionName = "TRAJECTORY"
        self.driver = "QSQLITE"

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        if not self.db.open():
            QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                 qApp.tr("Unable to establish a database connection.\n"
                                         "This example needs SQLite support. Please read "
                                         "the Qt SQL driver documentation for information "
                                         "how to build it.\n\n"
                                         "Click Cancel to exit."),
                                 QMessageBox.Cancel)

        self.db.exec(f'CREATE TEMP TABLE {self.tableName} (Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                      f'X REAL, Y REAL, Z REAL)')

        self.tableModel = QSqlTableModel(None, self.db)
        self.tableModel.setTable(self.tableName)
        self.tableModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.tableModel.select()

        self.TableModel.setHeaderData(0, Qt.Orientation.Horizontal, "Id")
        self.TableModel.setHeaderData(1, Qt.Orientation.Horizontal, "X")
        self.TableModel.setHeaderData(2, Qt.Orientation.Horizontal, "Y")
        self.TableModel.setHeaderData(3, Qt.Orientation.Horizontal, "Z")

        self.xMin = float('inf')
        self.yMin = float('inf')
        self.zMin = float('inf')
        self.xMax = float('-inf')
        self.yMax = float('-inf')
        self.zMax = float('-inf')

    def FillData(self, data):
        for X, Y, Z in data:
            record = QSqlRecord()
            record.append(QSqlField("X"))
            record.append(QSqlField("Y"))
            record.append(QSqlField("Z"))
            record.setValue("X", X)
            record.setValue("Y", Y)
            record.setValue("Z", Z)

    @property
    def TableModel(self):
        return self.tableModel
