# pylint: disable=too-few-public-methods,unused-argument
"""
Methods for drawing charts and graphs
"""
from app.model.action import Action
from app.model.pathway import Pathway
from matplotlib.figure import Figure


class PlottingService:
    @staticmethod
    def draw_metro_map(pathways: list[Pathway], all_actions: list[Action]) -> Figure:
        return None
