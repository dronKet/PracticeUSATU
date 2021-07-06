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

        self.createConnection()
        self.tableModel = QSqlTableModel(self, QSqlDatabase.database(self.connectionName))
        self.tableModel.setEditStrategy(QSqlTableModel.OnManualSubmit)

        self.xMin = float('inf')
        self.yMin = float('inf')
        self.zMin = float('inf')
        self.xMax = float('-inf')
        self.yMax = float('-inf')
        self.zMax = float('-inf')

    def createConnection(self):
        dataBase = QSqlDatabase.addDatabase(self.driver, self.connectionName)
        dataBase.setDatabaseName(self.dataBaseName)
        if not dataBase.open():
            QMessageBox.critical(None, qApp.tr("Cannot open database"),
                                 qApp.tr("Unable to establish a database connection.\n"
                                         "This example needs SQLite support. Please read "
                                         "the Qt SQL driver documentation for information "
                                         "how to build it.\n\n"
                                         "Click Cancel to exit."),
                                 QMessageBox.Cancel)
            return False

    def loadData(self, data):
        dataBase = QSqlDatabase.database(self.connectionName)
        dataBase.exec(f'DROP TABLE IF EXISTS {self.tableName}')
        dataBase.exec(f'CREATE TEMP TABLE {self.tableName} (Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                      f'X REAL, Y REAL, Z REAL)')
        self.tableModel.setTable(self.tableName)

        insertDataQuery = QSqlQuery(dataBase)
        for X, Y, Z in data:
            # record = self.tableModel.record()
            # record.remove(record.indexOf("Id"))
            # record.setValue("X", X)
            # record.setValue("Y", Y)
            # record.setValue("Z", Z)

            # if self.tableModel.insertRecord(-1, record):
            #     self.tableModel.submitAll()
            # else:
            #     dataBase.rollback()
            #     QMessageBox.warning(None, "Database Error",
            #                         insertDataQuery.lastError().text())

            if not insertDataQuery.exec(f'INSERT INTO {self.tableName} (X, Y, Z) VALUES ({X}, {Y}, {Z})'):
                QMessageBox.warning(None, "Database Error",
                                    insertDataQuery.lastError().text())
            else:
                self.xMin = min(self.xMin, X)
                self.yMin = min(self.yMin, Y)
                self.zMin = min(self.zMin, Z)
                self.xMax = max(self.xMax, X)
                self.yMax = max(self.yMax, Y)
                self.zMax = max(self.zMax, Z)

        insertDataQuery.finish()
        self.tableModel.select()

    @property
    def TableModel(self):
        return self.tableModel
