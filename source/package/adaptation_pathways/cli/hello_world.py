import os.path
import sys

import docopt
import matplotlib.pyplot as plt
import networkx as nx

import adaptation_pathways as ap

from ..draw import actions_graph_layout, pathways_graph_layout  # , pathways_map_layout
from .main import common_arguments, main_function


def pathways() -> None:
    # Define actions
    # current_situation = ap.Action("current situation")
    action_a = ap.Action("a")
    action_b = ap.Action("b")
    action_c = ap.Action("c")
    action_d = ap.Action("d")

    # Create actions graph
    actions_graph = ap.ActionsGraph()

    # # actions_graph.add_action(current_situation)
    # actions_graph.add_action(action_a)
    # actions_graph.add_action(action_b)
    # actions_graph.add_action(action_c)
    # actions_graph.add_action(action_d)

    # actions_graph.add_sequence(current_situation, action_a)
    # actions_graph.add_sequence(current_situation, action_b)
    actions_graph.add_sequence(action_a, action_b)
    actions_graph.add_sequence(action_b, action_d)
    actions_graph.add_sequence(action_a, action_c)
    # actions_graph.add_sequence(current_situation, action_d)
    # actions_graph.add_sequence(action_b, action_a)
    # actions_graph.add_sequence(action_b, action_c)
    # actions_graph.add_sequence(action_b, action_d)
    # actions_graph.add_sequence(action_c, action_a)
    # actions_graph.add_sequence(action_c, action_d)

    # Create pathways graph
    pathways_graph = ap.actions_graph_to_pathways_graph(actions_graph)
    # pathways_map = ap.pathways_graph_to_pathways_map(pathways_graph)

    # Define tipping points in terms of sedimentation rates

    # Define scenarios in terms of time relative to sedimentation rates
    # High sediment deposition
    # Low sediment deposition

    # Create some plot that contains all information we want to see in the pathway map

    plt.clf()
    _, axis = plt.subplots()
    axis.set_title("Actions graph")
    layout = actions_graph_layout(actions_graph)
    nx.draw_networkx(
        actions_graph.graph, pos=layout, with_labels=True, font_size="xx-small"
    )
    plt.savefig("hello_world-actions_graph.pdf", bbox_inches="tight")

    plt.clf()
    _, axis = plt.subplots()
    axis.set_title("Pathways graph")
    layout = pathways_graph_layout(pathways_graph)
    nx.draw_networkx(
        pathways_graph.graph, pos=layout, with_labels=True, font_size="xx-small"
    )
    plt.savefig("hello_world-pathways_graph.pdf", bbox_inches="tight")

    # plt.clf()
    # _, axis = plt.subplots()
    # axis.set_title("Pathways map")
    # layout = pathways_map_layout(pathways_map)
    # nx.draw_networkx(
    #     pathways_map.graph, pos=layout, with_labels=True, font_size="xx-small"
    # )
    # plt.savefig("hello_world-pathways_map.pdf", bbox_inches="tight")


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
