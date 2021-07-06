from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Model import *


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.model = Model(self)
        self.model.loadData(testData)

        # self.model.TableModel.setHeaderData(0, Qt.Orientation.Horizontal, "Id")
        # self.model.TableModel.setHeaderData(1, Qt.Orientation.Horizontal, "X")
        # self.model.TableModel.setHeaderData(2, Qt.Orientation.Horizontal, "Y")
        # self.model.TableModel.setHeaderData(3, Qt.Orientation.Horizontal, "Z")

        self.view = QTableView(self)
        self.view.setModel(self.model.TableModel)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.view2 = QTableView(self)
        self.view2.setModel(self.model.TableModel)
        self.view2.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.view.setColumnHidden(0, True)
        # self.view.resizeRowsToContents()

        delegate = TableDelegate(self.view)
        self.view.setItemDelegate(delegate)

        self.firstColor = QColor("white")
        self.secondColor = QColor("black")

        self.firstColorButton = QPushButton(self)
        self.firstColorButton.setStyleSheet('QPushButton {background-color: ' + self.firstColor.name() + '; border: '
                                                                                                         'none;}')
        self.firstColorButton.clicked.connect(self.clickedFirst)

        self.secondColorButton = QPushButton(self)
        self.secondColorButton.setStyleSheet('QPushButton {background-color: ' + self.secondColor.name() + '; border: '
                                                                                                           'none;}')
        self.secondColorButton.clicked.connect(self.clickedSecond)

        labelWellName = QLabel('TestName')
        labelWellName.setContentsMargins(0, 0, 0, 0)

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
        vbox.addWidget(labelWellName)
        vbox.addWidget(labelPalletName)
        vbox.addLayout(hboxColorFirst)
        vbox.addLayout(hboxColorSecond)
        vbox.addWidget(self.view)
        vbox.addWidget(self.view2)

        self.setLayout(vbox)

    def clickedFirst(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.firstColorButton.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')
            self.firstColor = color

    def clickedSecond(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.secondColorButton.setStyleSheet('QPushButton {background-color: ' + color.name() + '; border: none;}')
            self.secondColor = color


class TableDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # data = float(index.data(Qt.ItemDataRole.DisplayRole))
        # if index.column() == 3:
        #     option.backgroundBrush = QColor(int(data * 40. + 20.), 0, 0)

        # if index.column() == 2:
        #     option.backgroundBrush = QColor(0, int(data * 40. + 20.), 0)

        # if index.column() == 1:
        #     option.backgroundBrush = QColor(0, 0, int(data * 40. + 20.))

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setFrame(False)
        editor.setMaxLength(100)
        validator = QDoubleValidator(0., 999999.9, 20)
        validator.setLocale(QLocale("en"))
        editor.setValidator(validator)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setText(str(value))

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, Qt.ItemDataRole.EditRole)






