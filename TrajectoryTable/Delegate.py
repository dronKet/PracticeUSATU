from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from TrajectoryTable.Model import *


class TableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = QVariantAnimation()
        self.animation.setStartValue(QColor('blue'))
        self.animation.setEndValue(QColor('red'))

    def setFirstColor(self, firstColor: QColor):
        self.animation.setStartValue(firstColor)

    def initStyleOption(self, option: 'QStyleOptionViewItem', index: QModelIndex):
        super().initStyleOption(option, index)
        if index.column() != 0:
            col = index.column() - 1
            minimum, maximum = index.model().minMax()
            valMin = minimum[col]
            valMax = maximum[col]
            if valMin == valMax:
                data = 0.
            else:
                data = (float(index.data(Qt.ItemDataRole.DisplayRole)) - valMin) / (valMax - valMin)

            color = self.animation.interpolated(self.animation.startValue(), self.animation.endValue(), data)
            option.backgroundBrush = color

    def setSecondColor(self, secondColor: QColor):
        self.animation.setEndValue(secondColor)

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            return None
        editor = QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(float('-inf'))
        editor.setMaximum(float('inf'))
        editor.setDecimals(16)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        editor.setValue(float(value))

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.ItemDataRole.EditRole)
