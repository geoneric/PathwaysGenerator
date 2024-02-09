from PySide6 import QtCore  # , QtGui, QtWidgets
from PySide6.QtCore import Qt


# pylint: disable-next=wrong-import-order, unused-import
from __feature__ import snake_case  # isort:skip


# TODO The model could contain (action, tipping point) tuples
#      When editing, actions can be selected from a list of defined actions
#      Is can be made impossible to store information about non-existing (removed?) actions


class TippingPointModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._header = ["Action", "Tipping point"]

    # pylint: disable=inconsistent-return-statements, no-else-return
    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                # Action name
                name = self._data[index.row()][index.column()]
                edition = 0
                return f"{name}[{edition}]"
            else:
                # Tipping point: a number
                return str(self._data[index.row()][index.column()])

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._data)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._data[0])

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
