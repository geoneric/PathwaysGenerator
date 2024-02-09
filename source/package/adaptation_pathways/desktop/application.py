import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication  # , QFileDialog

import adaptation_pathways as ap

# from ..graph import read_sequences, read_tipping_points, sequence_graph_to_pathway_map
from .model.sequence import SequenceModel
from .model.tipping_point import TippingPointModel
from .path import Path
from .widget.pathway_map import PathwayMapWidget
from .widget.sequence_graph import SequenceGraphWidget


# from io import StringIO


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
        self.ui.setWindowTitle(f"{self.name} - {self.version}")
        self.ui.show()

        self.ui.action_open.setIcon(QIcon(Path.icon("folder-open-table.png")))
        self.ui.action_save.setIcon(QIcon(Path.icon("disk.png")))

        self.ui.action_open.triggered.connect(self.open_dataset)
        self.ui.action_about.triggered.connect(self.show_about_dialog)

        # https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
        # https://www.pythonguis.com/faq/editing-pyqt-tableview/

        data = [
            ["current", "a"],
            ["a", "b"],
            ["b", "c"],
        ]
        self.sequence_model = SequenceModel(data)
        self.ui.table_sequences.setModel(self.sequence_model)

        data = [
            ["current", 2020],
            ["a", 2030],
            ["b", 2040],
            ["c", 2050],
        ]
        self.tipping_point_model = TippingPointModel(data)
        self.ui.table_tipping_points.setModel(self.tipping_point_model)

        # TODO Plot the data from the models, using our own plot routines
        # - Finish refactoring our plot routines

        sequence_graph_widget = SequenceGraphWidget(
            parent=None, width=5, height=4, dpi=100
        )
        sequence_graph_widget.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.ui.plot_tab_widget.addTab(sequence_graph_widget, "Sequence graph")

        pathway_map_widget = PathwayMapWidget(parent=None, width=5, height=4, dpi=100)
        pathway_map_widget.axes.plot([4, 3, 2, 1, 0], [10, 1, 20, 3, 40])
        self.ui.plot_tab_widget.addTab(pathway_map_widget, "Pathway map")

        self.ui.splitter.setSizes((100, 100))

    @Slot()
    def open_dataset(self):
        # sequences = pd.DataFrame([
        #         ["current", "a"],
        #         ["a", "b"],
        #         ["b", "c"],
        #     ], columns = ["From-action", "To-action"]
        # sequences = read_sequences(
        #     StringIO("""
        #         current a
        #         a b
        #         b c""")
        # )

        # pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        # tipping_points = read_tipping_points(
        #     StringIO("""
        #         current 2030
        #         a 2040
        #         b 2050
        #         c 2060"""),
        #     pathway_map.actions(),
        # )

        # pathway_map.assign_tipping_points(tipping_points)
        # pathway_map.set_attribute("level", level_by_action)

        pass
        # TODO Open a table (*.txt (see networkx doc for format convention))
        # pathname = QFileDialog.get_open_file_name(
        #     self.ui, "Open File", "/home", "Images (*.png *.xpm *.jpg)"
        # )
        # print(pathname)

    @Slot()
    def show_about_dialog(self):
        dialog = loader.load(Path.ui("about_dialog.ui"), self.ui)
        dialog.setWindowTitle(f"About {self.name}")
        dialog.text.setText("*Meh*!")
        dialog.show()


def application():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Path.icon("icon.svg")))
    _ = MainUI()
    app.exec()

    return 0
