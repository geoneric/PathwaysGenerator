import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..action import Action
from .layout import pathways_graph_layout, pathways_map_layout, sequence_graph_layout
from .pathways_graph import PathwaysGraph
from .pathways_map import PathwaysMap
from .sequence_graph import SequenceGraph


def init_plot(title: str, graph: nx.DiGraph, layout: dict[Action, np.ndarray]) -> None:
    plt.rc(
        "axes.spines", **{"bottom": False, "left": False, "right": False, "top": False}
    )
    # plt.clf()

    draw_options = {
        "with_labels": True,
        "font_size": "small",
        "font_weight": "bold",
    }

    _, axis = plt.subplots()

    axis.set_title(title)
    nx.draw_networkx(graph, pos=layout, **draw_options)


def save_plot(pathname: str) -> None:
    plt_options = {
        "bbox_inches": "tight",
        "transparent": True,
    }
    plt.savefig(pathname, **plt_options)


def plot_sequence_graph(sequence_graph: SequenceGraph) -> None:
    init_plot(
        "Sequences graph",
        sequence_graph.graph,
        sequence_graph_layout(sequence_graph),
    )


def plot_and_save_sequence_graph(sequence_graph: SequenceGraph, pathname: str) -> None:
    plot_sequence_graph(sequence_graph)
    save_plot(pathname)


def plot_pathways_graph(pathways_graph: PathwaysGraph, pathname: str) -> None:
    init_plot(
        "Pathways graph",
        pathways_graph.graph,
        pathways_graph_layout(pathways_graph),
    )
    save_plot(pathname)


def plot_pathways_map(pathways_map: PathwaysMap, pathname: str) -> None:
    init_plot("Pathways map", pathways_map.graph, pathways_map_layout(pathways_map))
    save_plot(pathname)
