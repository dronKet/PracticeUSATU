from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TrajectoryTable.Model import Model, genData
from TrajectoryTable.Delegate import TableDelegate


class TableTrajectory(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QTableView(self)

        self.firstColorButton = QPushButton(self)
        self.firstColorButton.setStyleSheet('QPushButton {background-color: ' + QColor('blue').name() +
                                            '; border: none;}')
        self.firstColorButton.clicked.connect(self.clickedFirst)

        self.secondColorButton = QPushButton(self)
        self.secondColorButton.setStyleSheet('QPushButton {background-color: ' + QColor('red').name() +
                                             '; border: none;}')
        self.secondColorButton.clicked.connect(self.clickedSecond)

        self.labelWellName = QLabel('Скважина:')
        self.labelWellName.setContentsMargins(0, 0, 0, 0)
        labelPalletName = QLabel('Палитра:')
        labelPalletName.setContentsMargins(0, 0, 0, 0)

        hboxColorFirst = QHBoxLayout()
        hboxColorFirst.addWidget(QLabel('От'))
        hboxColorFirst.addWidget(self.firstColorButton)
        hboxColorFirst.setContentsMargins(0, 0, 0, 0)
        hboxColorFirst.setSpacing(0)

        hboxColorSecond = QHBoxLayout()
        hboxColorSecond.addWidget(QLabel('До'))
        hboxColorSecond.addWidget(self.secondColorButton)
        hboxColorSecond.setContentsMargins(0, 0, 0, 0)
        hboxColorSecond.setSpacing(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.labelWellName)
        vbox.addWidget(labelPalletName)
        vbox.addLayout(hboxColorFirst)
        vbox.addLayout(hboxColorSecond)
        vbox.addWidget(self.view)

        self.setLayout(vbox)

    def clickedFirst(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.firstColorButton.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')
            self.view.itemDelegate().setFirstColor(color)

    def clickedSecond(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.secondColorButton.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')
            self.view.itemDelegate().setSecondColor(color)
