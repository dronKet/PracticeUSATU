from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Model import *


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.model = Model(self)
        self.model.loadData(testData)

        self.model.TableModel.setHeaderData(0, Qt.Orientation.Horizontal, "Id")
        self.model.TableModel.setHeaderData(1, Qt.Orientation.Horizontal, "X")
        self.model.TableModel.setHeaderData(2, Qt.Orientation.Horizontal, "Y")
        self.model.TableModel.setHeaderData(3, Qt.Orientation.Horizontal, "Z")

        self.view = QTableView(self)
        self.view.setModel(self.model.TableModel)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setColumnHidden(0, True)
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()
        # self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # delegate = ColorDelegate(self.view)
        # self.view.setItemDelegate(delegate)

        self.firstColor = QPushButton(self)
        self.firstColor.setStyleSheet('QPushButton {background-color: white; border: none;}')
        self.firstColor.clicked.connect(self.clickedFirst)

        self.secondColor = QPushButton(self)
        self.secondColor.setStyleSheet('QPushButton {background-color: black; border: none;}')
        self.secondColor.clicked.connect(self.clickedSecond)

        labelWellName = QLabel('TestName')
        labelWellName.setContentsMargins(0, 0, 0, 0)

        labelPalletName = QLabel('Палитра')
        labelPalletName.setContentsMargins(0, 0, 0, 0)

        hboxColorFirst = QHBoxLayout()
        hboxColorFirst.addWidget(QLabel('От'), alignment=Qt.AlignLeft)
        hboxColorFirst.addWidget(self.firstColor, alignment=Qt.AlignLeft)
        hboxColorFirst.setContentsMargins(0, 0, 0, 0)
        hboxColorFirst.setSpacing(0)

        hboxColorSecond = QHBoxLayout()
        hboxColorSecond.addWidget(QLabel('До'), alignment=Qt.AlignLeft)
        hboxColorSecond.addWidget(self.secondColor, alignment=Qt.AlignLeft)
        hboxColorSecond.setContentsMargins(0, 0, 0, 0)
        hboxColorSecond.setSpacing(0)

        vbox = QVBoxLayout()
        vbox.addWidget(labelWellName)
        vbox.addWidget(labelPalletName)
        vbox.addLayout(hboxColorFirst)
        vbox.addLayout(hboxColorSecond)
        vbox.addWidget(self.view)

        self.setLayout(vbox)

    def clickedFirst(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.firstColor.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')

    def clickedSecond(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.secondColor.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')


class ColorDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        data = index.data(Qt.ItemDataRole.DisplayRole)
        if index.column() == 3:
            option.backgroundBrush = QColor(int(data * 40. + 20.), 0, 0)

        if index.column() == 2:
            option.backgroundBrush = QColor(0, int(data * 40. + 20.), 0)

        if index.column() == 1:
            option.backgroundBrush = QColor(0, 0, int(data * 40. + 20.))
