import os.path
import sys

import docopt
import matplotlib.pyplot as plt
import networkx as nx

import adaptation_pathways as ap

from .main import common_arguments, main_function


def pathways() -> None:
    current = ap.Action("current")
    action_a = ap.Action("a")
    action_b = ap.Action("b")
    action_c = ap.Action("c")

    actions_graph = ap.graph.ActionsGraph()

    actions_graph.add_sequence(current, action_a)
    actions_graph.add_sequence(current, action_b)
    actions_graph.add_sequence(current, action_c)
    actions_graph.add_sequence(action_b, action_a)
    actions_graph.add_sequence(action_b, action_c)
    actions_graph.add_sequence(action_c, action_a)

    pathways_graph = ap.graph.actions_graph_to_pathways_graph(actions_graph)
    pathways_map = ap.graph.pathways_graph_to_pathways_map(pathways_graph)

    plt.rc(
        "axes.spines", **{"bottom": False, "left": False, "right": False, "top": False}
    )

    draw_options = {
        "with_labels": True,
        "font_size": "xx-small",
    }
    plt_options = {
        "bbox_inches": "tight",
        "transparent": True,
    }

    plt.clf()

    _, axis = plt.subplots()
    axis.set_title("Actions graph")
    layout = ap.draw.actions_graph_layout(actions_graph)
    nx.draw_networkx(actions_graph.graph, pos=layout, **draw_options)
    plt.savefig("hello_world-actions_graph.pdf", **plt_options)

    plt.clf()
    _, axis = plt.subplots()
    axis.set_title("Pathways graph")
    layout = ap.draw.pathways_graph_layout(pathways_graph)
    nx.draw_networkx(pathways_graph.graph, pos=layout, **draw_options)
    plt.savefig("hello_world-pathways_graph.pdf", **plt_options)

    plt.clf()
    _, axis = plt.subplots()
    axis.set_title("Pathways map")
    layout = ap.draw.pathways_map_layout(pathways_map)
    # layout = nx.planar_layout(pathways_map.graph)
    nx.draw_networkx(pathways_map.graph, pos=layout, **draw_options)
    plt.savefig("hello_world-pathways_map.pdf", **plt_options)


@main_function
def hello_world() -> int:
    pathways()
    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
The simplest example possible

Usage:
    {command}

Options:
{common_arguments()}
"""

    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)

    return hello_world()
