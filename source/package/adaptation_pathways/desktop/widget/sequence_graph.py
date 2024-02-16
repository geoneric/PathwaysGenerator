from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from ...plot import init_axes


class SequenceGraphWidget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super().__init__(Figure(figsize=(width, height), dpi=dpi, layout="constrained"))

        if parent is not None:
            self.setParent(parent)

        self.axes = self.figure.add_subplot()
        init_axes(self.axes)
