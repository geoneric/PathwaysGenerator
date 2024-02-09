from PySide6 import QtCore  # , QtGui, QtWidgets
from PySide6.QtCore import Qt


### # pylint: disable-next=wrong-import-order, unused-import
### from __feature__ import snake_case  # isort:skip


# TODO The model can contain (from action, to action) tuples (Action instances, including
#      multiple revisions of the same action)
#      When editing, actions can be selected from a list of already defined actions or new ones
#      can be added.
#      When removing actions, a warning must be shown when tipping point info will also be removed.


class SequenceModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._header = ["From action", "To action"]

    # pylint: disable=inconsistent-return-statements
    def data(self, index, role):
        if role == Qt.DisplayRole:
            name = self._data[index.row()][index.column()]
            edition = 0
            return f"{name}[{edition}]"

    def rowCount(self, index):  # pylint: disable=unused-argument
        return len(self._data)

    def columnCount(self, index):  # pylint: disable=unused-argument
        return len(self._data[0])

    # pylint: disable=inconsistent-return-statements
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._header[section]
