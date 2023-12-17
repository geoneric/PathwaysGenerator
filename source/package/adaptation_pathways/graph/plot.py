import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from ..action import Action
from .layout import pathway_graph_layout, pathway_map_layout, sequence_graph_layout
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
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
        "Sequence graph",
        sequence_graph.graph,
        sequence_graph_layout(sequence_graph),
    )


def plot_and_save_sequence_graph(sequence_graph: SequenceGraph, pathname: str) -> None:
    plot_sequence_graph(sequence_graph)
    save_plot(pathname)


def plot_pathway_graph(pathway_graph: PathwayGraph) -> None:
    init_plot(
        "Pathway graph",
        pathway_graph.graph,
        pathway_graph_layout(pathway_graph),
    )


def plot_and_save_pathway_graph(pathway_graph: PathwayGraph, pathname: str) -> None:
    plot_pathway_graph(pathway_graph)
    save_plot(pathname)


def plot_pathway_map(pathway_map: PathwayMap) -> None:
    init_plot("Pathway map", pathway_map.graph, pathway_map_layout(pathway_map))


def plot_and_save_pathway_map(pathway_map: PathwayMap, pathname: str) -> None:
    plot_pathway_map(pathway_map)
    save_plot(pathname)
