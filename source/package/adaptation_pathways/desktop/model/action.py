from PySide6 import QtCore, QtGui  # , QtWidgets
from PySide6.QtCore import Qt

from ...action import Action
from ...plot.colour import Colour


class ActionModel(QtCore.QAbstractTableModel):

    _actions: list[tuple[Action, Colour, int]]
    _headers: tuple[str, str, str]

    def __init__(self, actions: list[tuple[Action, Colour, int]]):

        super().__init__()
        self._actions = actions
        self._headers = ("Name", "Colour", "Tipping point")

    # def flags(self, index):
    #     _flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

    #     return _flags | Qt.ItemIsEditable if index.column() != 1 else _flags

    # pylint: disable=inconsistent-return-statements, no-else-return
    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            record = self._actions[index.row()]
            if index.column() == 0:
                action = record[0]
                return action.name
            elif index.column() == 2:
                tipping_point = record[2]
                return f"{tipping_point}"
            else:
                return ""
        elif role == Qt.BackgroundRole:
            if index.column() == 1:
                colour = self._actions[index.row()][1]
                return QtGui.QColor.fromRgbF(*colour)

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         record = self._actions[index.row()]
    #         if index.column() == 0:
    #             action = record[0]
    #             action.name = value
    #             return True
    #         elif index.column() == 1:
    #             # TODO
    #             pass
    #             return True
    #         else:
    #             self._actions[index.row()] = \
    #                 (*record[:index.column()], int(value), *record[index.column():])
    #             return True

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._actions)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._headers)

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
