from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PathwayMapWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(Figure(figsize=(width, height), dpi=dpi))

        if parent is not None:
            self.setParent(parent)

        self.axes = self.figure.add_subplot()
