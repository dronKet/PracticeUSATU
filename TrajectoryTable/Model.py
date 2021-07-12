from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QMessageBox, qApp
import numpy as np


def genData():
    data = np.random.rand(50, 3)
    return data


class Model(QSqlTableModel):
    def __init__(self, db, parent=None):
        super().__init__(parent, db)

        self.dataChanged.connect(self.on_dataChanged)

        self.min = [float('inf'), float('inf'), float('inf')]
        self.max = [float('-inf'), float('-inf'), float('-inf')]

    def minMax(self):
        return self.min, self.max

    def setWellTrajectory(self, data, idWell):
        for X, Y, Z in data:
            record = QSqlRecord()
            record.append(QSqlField("IdWell"))
            record.append(QSqlField("X"))
            record.append(QSqlField("Y"))
            record.append(QSqlField("Z"))
            record.setValue("IdWell", idWell)
            record.setValue("X", float(X))
            record.setValue("Y", float(Y))
            record.setValue("Z", float(Z))
            self.insertRecord(-1, record)

        self.min[0] = data[:, 0].min()
        self.min[1] = data[:, 1].min()
        self.min[2] = data[:, 2].min()
        self.max[0] = data[:, 0].max()
        self.max[1] = data[:, 1].max()
        self.max[2] = data[:, 2].max()

        self.submitAll()
        self.setFilter(f'IdWell="{idWell}"')

    def selectWellTrajectory(self, idWell):
        self.setFilter(f'IdWell="{idWell}"')
        self.on_dataChanged(self.index(0, 1), self.index(self.rowCount(), 1), roles=[])
        self.on_dataChanged(self.index(0, 2), self.index(self.rowCount(), 2), roles=[])
        self.on_dataChanged(self.index(0, 3), self.index(self.rowCount(), 3), roles=[])

    def on_dataChanged(self, topLeft, bottomRight, roles):
        if topLeft.column() != 0:
            column = topLeft.column() - 1
            self.min[column] = float('inf')
            self.max[column] = float('-inf')
            for row in range(self.rowCount()):
                data = float(self.index(row, column + 1).data())
                self.min[column] = min(data, self.min[column])
                self.max[column] = max(data, self.max[column])
