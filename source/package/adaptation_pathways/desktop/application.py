import sys
from io import StringIO

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QObject, Slot
from PySide6.QtUiTools import QUiLoader

import adaptation_pathways as ap

from ..action import Action

# action_level_by_first_occurrence
# read_tipping_points
# sequence_graph_to_pathway_map
# sequences_to_sequence_graph
from ..graph import read_actions, read_sequences
from ..plot.colour import Colour, default_action_colours, default_nominal_palette
from .model.action import ActionModel
from .model.sequence import SequenceModel
from .path import Path
from .widget.pathway_map import PathwayMapWidget
from .widget.sequence_graph import SequenceGraphWidget


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

        self.ui.action_open.setIcon(QtGui.QIcon(Path.icon("folder-open-table.png")))
        self.ui.action_save.setIcon(QtGui.QIcon(Path.icon("disk.png")))

        self.ui.action_open.triggered.connect(self.open_dataset)
        self.ui.action_about.triggered.connect(self.show_about_dialog)

        self.ui.table_actions.customContextMenuRequested.connect(
            self.on_actions_table_context_menu
        )
        self.ui.table_actions.doubleClicked.connect(
            lambda idx: self.edit_action(idx.row())
        )

        self.actions: list[tuple[Action, Colour, int]] = []
        self.action_model = ActionModel(self.actions)
        self.ui.table_actions.setModel(self.action_model)

        self.sequences: list[tuple[Action, Action]] = []
        self.sequence_model = SequenceModel(self.sequences)
        self.ui.table_sequences.setModel(self.sequence_model)

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

        self.ui.editor_tab_widget.setCurrentIndex(0)
        self.ui.plot_tab_widget.setCurrentIndex(0)
        self.ui.splitter.setSizes((100, 100))

    @Slot()
    def open_dataset(self):
        actions = read_actions(
            StringIO(
                """
                current
                a
                b
                c"""
            )
        )
        colours = default_action_colours(len(actions))
        tipping_points = [0] * len(actions)

        sequences = read_sequences(
            StringIO(
                """
                current a
                a b
                b c"""
            )
        )
        # level_by_action = action_level_by_first_occurrence(sequences)
        # sequence_graph = sequences_to_sequence_graph(sequences)
        # pathway_map = sequence_graph_to_pathway_map(sequence_graph)
        # tipping_points = read_tipping_points(
        #     StringIO(
        #         """
        #         current 2030
        #         a 2040
        #         b 2050
        #         c 2060"""
        #     ),
        #     pathway_map.actions(),
        # )

        # pathway_map.assign_tipping_points(tipping_points)
        # pathway_map.set_attribute("level", level_by_action)

        self.actions.clear()
        self.actions.extend(zip(actions, colours, tipping_points))
        self.ui.table_actions.model().layoutChanged.emit()

        self.sequences.clear()
        self.sequences.extend(sequences)
        self.ui.table_sequences.model().layoutChanged.emit()

        # TODO Open a dataset
        # pathname = QFileDialog.get_open_file_name(
        #     self.ui, "Open File", "/home", "Images (*.png *.xpm *.jpg)"
        # )

    def on_actions_table_context_menu(self, pos):
        context = QtWidgets.QMenu(self.ui.table_actions)

        action_idx = self.ui.table_actions.rowAt(pos.y())

        if action_idx != -1:
            edit_action_action = QtGui.QAction("Edit action...", self.ui.table_actions)
            edit_action_action.triggered.connect(lambda: self.edit_action(action_idx))
            context.addAction(edit_action_action)

            remove_action_action = QtGui.QAction("Remove action", self.ui.table_actions)
            remove_action_action.triggered.connect(
                lambda: self.remove_action(action_idx)
            )
            context.addAction(remove_action_action)

        add_action_action = QtGui.QAction("Add action...", self.ui.table_actions)
        add_action_action.triggered.connect(self.add_action)
        context.addAction(add_action_action)

        clear_actions_action = QtGui.QAction("Clear actions", self.ui.table_actions)
        clear_actions_action.triggered.connect(self.clear_actions)
        context.addAction(clear_actions_action)

        context.exec(self.ui.table_actions.viewport().mapToGlobal(pos))

    def add_action(self):
        name = "Name"
        colour = default_nominal_palette()[0]
        tipping_point = 0

        self.actions.append((Action(name), colour, tipping_point))
        self.ui.table_actions.model().layoutChanged.emit()
        self.edit_action(len(self.actions) - 1)

    def edit_action(self, idx):
        action_tuple = self.actions[idx]
        action, colour, tipping_point = action_tuple

        dialog = loader.load(Path.ui("edit_action_dialog.ui"), self.ui)
        dialog.name_edit.setText(action.name)

        palette = dialog.select_colour_button.palette()
        role = dialog.select_colour_button.backgroundRole()
        colour = QtGui.QColor.fromRgbF(*colour)
        palette.setColor(role, colour)
        dialog.select_colour_button.setPalette(palette)
        dialog.select_colour_button.setAutoFillBackground(True)

        new_colour = colour

        def select_colour():
            """
            Allow the user to select a colour
            """
            nonlocal new_colour
            new_colour = QtWidgets.QColorDialog.getColor(initial=colour)
            palette.setColor(role, new_colour)
            dialog.select_colour_button.setPalette(palette)
            # dialog.select_colour_button.setAutoFillBackground(True)

        dialog.select_colour_button.clicked.connect(select_colour)

        dialog.tipping_point_spin_box.setValue(tipping_point)

        if dialog.exec():
            new_name = dialog.name_edit.text()
            new_tipping_point = dialog.tipping_point_spin_box.value()

            something_changed = (
                new_name != action.name
                or new_colour != colour
                or new_tipping_point != tipping_point
            )

            if something_changed:
                new_action_tuple = (
                    Action(new_name),
                    new_colour.getRgbF(),
                    new_tipping_point,
                )
                self.actions[idx] = new_action_tuple
                self.ui.table_actions.model().layoutChanged.emit()

    def remove_action(self, idx):
        del self.actions[idx]
        self.ui.table_actions.model().layoutChanged.emit()

    def clear_actions(self):
        self.actions.clear()
        self.ui.table_actions.model().layoutChanged.emit()

    @Slot()
    def show_about_dialog(self):
        dialog = loader.load(Path.ui("about_dialog.ui"), self.ui)
        dialog.setWindowTitle(f"About {self.name}")
        dialog.text.setText("*Meh*!")
        dialog.show()


def application():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(Path.icon("icon.svg")))
    _ = MainUI()
    app.exec()

    return 0
