# from PySide6.QtWidgets import QApplication, QMainWindow
#
# from main_window import Ui_MainWindow
#
#
# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self, *args, obj=None, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)
#         self.setupUi(self)
#
#
# def application():
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     app.exec()
#
#     return 0


import os
import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog

import adaptation_pathways as ap


loader = QUiLoader()
basedir = os.path.dirname(__file__)


class MainUI(QObject):  # Not a widget.
    def __init__(self):
        super().__init__()
        self.name = "Adaptation Pathway Generator"
        self.version = f"{ap.__version__}"

        self.ui = loader.load(os.path.join(basedir, "main_window.ui"), None)
        self.ui.setWindowTitle(f"{self.name} - {self.version}")
        self.ui.show()

        open_sequences_action = QAction(
            QIcon(os.path.join(basedir, "icon", "folder-open-table.png")),
            "&Open sequences table",
            self,
        )
        open_sequences_action.triggered.connect(self.open_sequences_table)
        quit_action = QAction(
            "Quit",
            self,
        )
        file_menu = self.ui.menubar.addMenu("&File")
        file_menu.addAction(open_sequences_action)
        file_menu.addAction(quit_action)

        about_action = QAction(
            "About",
            self,
        )
        about_action.triggered.connect(self.show_about_dialog)
        help_menu = self.ui.menubar.addMenu("&Help")
        help_menu.addAction(about_action)

        self.ui.toolBar.addAction(open_sequences_action)

    @Slot()
    def open_sequences_table(self):
        # TODO Open a table (*.txt (see networkx doc for format convention))
        pathname = QFileDialog.getOpenFileName(
            self.ui, "Open File", "/home", "Images (*.png *.xpm *.jpg)"
        )
        print(pathname)

    @Slot()
    def show_about_dialog(self):
        dialog = loader.load(os.path.join(basedir, "about_dialog.ui"), self.ui)
        dialog.setWindowTitle(f"About {self.name}")
        dialog.text.setText("*Meh*!")
        dialog.show()


def application():
    app = QApplication(sys.argv)
    MainUI()
    app.exec()

    return 0
