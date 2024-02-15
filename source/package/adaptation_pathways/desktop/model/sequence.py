from PySide6 import QtCore  # , QtGui, QtWidgets
from PySide6.QtCore import Qt

from ...action import Action


class SequenceModel(QtCore.QAbstractTableModel):

    _sequences: list[tuple[Action, Action]]
    _headers: tuple[str, str]

    def __init__(self, sequences: list[tuple[Action, Action]]):
        super().__init__()
        self._sequences = sequences
        self._headers = ("From action", "To action")

    def flags(self, index):  # pylint: disable=unused-argument
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    # pylint: disable=inconsistent-return-statements
    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            action = self._sequences[index.row()][index.column()]
            return f"{action}"

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            sequence = self._sequences[index.row()]
            self._sequences[index.row()] = (
                *sequence[: index.column()],
                Action(value),
                *sequence[index.column() :],
            )
            return True

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._sequences)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._headers)

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
