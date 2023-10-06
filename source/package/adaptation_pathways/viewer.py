import sys

from PySide6 import QtWebEngineWidgets
from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtWidgets import QApplication


# pylint: disable=import-error, unused-import
from __feature__ import snake_case, true_property  # noqa: F401, isort:skip


class Viewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, url):
        super().__init__()
        self.window_title = "Adaption Pathways"
        self.load(url)


def view(url: str):
    QCoreApplication.organization_name = "Deltares"
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)

    viewer = Viewer(QUrl(url))
    viewer.show()

    return app.exec()
