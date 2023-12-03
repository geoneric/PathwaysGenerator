import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..action import Action
from .actions_graph import ActionsGraph
from .layout import actions_graph_layout, pathways_graph_layout, pathways_map_layout
from .pathways_graph import PathwaysGraph
from .pathways_map import PathwaysMap


def init_plot(
    title: str, graph: nx.DiGraph, layout: dict[Action, np.ndarray], pathname: str
) -> None:
    plt.rc(
        "axes.spines", **{"bottom": False, "left": False, "right": False, "top": False}
    )
    plt.clf()

    draw_options = {
        "with_labels": True,
        "font_size": "small",
        "font_weight": "bold",
    }
    plt_options = {
        "bbox_inches": "tight",
        "transparent": True,
    }

    _, axis = plt.subplots()

    axis.set_title(title)
    nx.draw_networkx(graph, pos=layout, **draw_options)
    plt.savefig(pathname, **plt_options)


def plot_actions_graph(actions_graph: ActionsGraph, pathname: str) -> None:
    init_plot(
        "Actions graph",
        actions_graph.graph,
        actions_graph_layout(actions_graph),
        pathname,
    )


def plot_pathways_graph(pathways_graph: PathwaysGraph, pathname: str) -> None:
    init_plot(
        "Pathways graph",
        pathways_graph.graph,
        pathways_graph_layout(pathways_graph),
        pathname,
    )


def plot_pathways_map(pathways_map: PathwaysMap, pathname: str) -> None:
    init_plot(
        "Pathways map", pathways_map.graph, pathways_map_layout(pathways_map), pathname
    )
