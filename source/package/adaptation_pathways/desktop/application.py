import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication  # , QFileDialog

import adaptation_pathways as ap

from .model.sequence import SequenceModel
from .model.tipping_point import TippingPointModel
from .path import Path


# pylint: disable-next=wrong-import-order, unused-import
from __feature__ import snake_case  # isort:skip

loader = QUiLoader()


try:
    from ctypes import windll  # type: ignore

    my_app_id = f"nl.adaptation_pathways.pathway_generator.{ap.__version__}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except ImportError:
    pass


class MainUI(QObject):  # Not a widget
    def __init__(self):
        super().__init__()
        self.name = "Adaptation Pathway Generator"
        self.version = f"{ap.__version__}"

        self.ui = loader.load(Path.ui("main_window.ui"), None)
        self.ui.window_title = f"{self.name} - {self.version}"
        self.ui.show()

        self.ui.action_open.set_icon(QIcon(Path.icon("folder-open-table.png")))
        self.ui.action_save.set_icon(QIcon(Path.icon("disk.png")))

        self.ui.action_open.triggered.connect(self.open_sequences_table)
        self.ui.action_about.triggered.connect(self.show_about_dialog)

        # https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
        # https://www.pythonguis.com/faq/editing-pyqt-tableview/

        data = [
            ["current", "a"],
            ["a", "b"],
            ["b", "c"],
        ]
        self.sequence_model = SequenceModel(data)
        self.ui.table_sequences.set_model(self.sequence_model)

        data = [
            ["current", 2020],
            ["a", 2030],
            ["b", 2040],
            ["c", 2050],
        ]
        self.tipping_point_model = TippingPointModel(data)
        self.ui.table_tipping_points.set_model(self.tipping_point_model)

    @Slot()
    def open_sequences_table(self):
        pass
        # TODO Open a table (*.txt (see networkx doc for format convention))
        # pathname = QFileDialog.get_open_file_name(
        #     self.ui, "Open File", "/home", "Images (*.png *.xpm *.jpg)"
        # )
        # print(pathname)

    @Slot()
    def show_about_dialog(self):
        dialog = loader.load(Path.ui("about_dialog.ui"), self.ui)
        dialog.set_window_title(f"About {self.name}")
        dialog.text.set_text("*Meh*!")
        dialog.show()


def application():
    app = QApplication(sys.argv)
    app.set_window_icon(QIcon(Path.icon("icon.svg")))
    _ = MainUI()
    app.exec()

    return 0
