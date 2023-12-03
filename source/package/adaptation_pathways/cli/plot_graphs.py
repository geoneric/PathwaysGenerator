import os.path
import sys

import docopt
import networkx as nx

import adaptation_pathways as ap

from ..graph import plot_actions_graph, plot_pathways_graph, plot_pathways_map
from .main import common_arguments, main_function


def read_pathways(pathways_pathname: str) -> ap.graph.ActionsGraph:
    graph = nx.read_edgelist(pathways_pathname, create_using=nx.DiGraph)
    actions_graph = ap.graph.ActionsGraph()
    actions = {action_label: ap.Action(action_label) for action_label in graph.nodes()}

    for from_action_label, to_action_label in graph.edges():
        actions_graph.add_sequence(actions[from_action_label], actions[to_action_label])

    return actions_graph


@main_function
def generate_graphs(pathways_pathname: str, plots_prefix_pathname: str) -> int:
    actions_graph = read_pathways(pathways_pathname)
    pathways_graph = ap.graph.actions_graph_to_pathways_graph(actions_graph)
    pathways_map = ap.graph.pathways_graph_to_pathways_map(pathways_graph)

    assert os.path.isdir(plots_prefix_pathname), plots_prefix_pathname

    basename = os.path.splitext(os.path.basename(pathways_pathname))[0]

    plot_pathname = os.path.join(plots_prefix_pathname, f"{basename}-actions_graph.svg")
    plot_actions_graph(actions_graph, plot_pathname)

    plot_pathname = os.path.join(
        plots_prefix_pathname, f"{basename}-pathways_graph.svg"
    )
    plot_pathways_graph(pathways_graph, plot_pathname)

    plot_pathname = os.path.join(plots_prefix_pathname, f"{basename}-pathways_map.svg")
    plot_pathways_map(pathways_map, plot_pathname)

    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Plot action and pathways graphs

Usage:
    {command} <pathways> <prefix>

Options:
    pathways       Name of file containing ѕequences of actions
    prefix         Name of directory to store plots in . The file name will be
                   based on the name of the pathways file passed in and the
                   kind of plot in the file.
{common_arguments()}

The format for storing sequences is simple: per line mention the names of
two actions that form a sequence. Information from multiple lines can result
in longer sequences. Example:

current a
current b
current c
b a
c a
b c
"""
    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)
    pathways_pathname = arguments["<pathways>"]  # type: ignore
    plots_prefix_pathname = arguments["<prefix>"]  # type: ignore

    return generate_graphs(pathways_pathname, plots_prefix_pathname)
