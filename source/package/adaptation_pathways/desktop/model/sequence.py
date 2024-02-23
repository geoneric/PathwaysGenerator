from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt

from ...action import Action
from ...plot.colour import Colour


class SequenceModel(QtCore.QAbstractTableModel):

    _sequences: list[list[Action]]
    _headers: tuple[str, str]
    _colour_by_action: dict[Action, Colour]

    def __init__(
        self, sequences: list[list[Action]], colour_by_action: dict[Action, Colour]
    ):
        super().__init__()
        self._sequences = sequences
        self._headers = ("From action", "To action")
        self._colour_by_action = colour_by_action

    # pylint: disable=inconsistent-return-statements
    def data(self, index, role):
        if role == Qt.DisplayRole:
            action = self._sequences[index.row()][index.column()]
            return action.name

        if role == Qt.DecorationRole:
            action = self._sequences[index.row()][index.column()]
            colour = self._colour_by_action[action]
            return QtGui.QColor.fromRgbF(*colour)

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._sequences)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._headers)

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

    def removeRows(self, row, nr_rows, parent):  # pylint: disable=unused-argument
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + nr_rows - 1)
        del self._sequences[row : row + nr_rows]
        self.endRemoveRows()
        return True
