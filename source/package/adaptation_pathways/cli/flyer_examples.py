import os.path
import sys

import docopt
import matplotlib.pyplot as plt
import networkx as nx

import adaptation_pathways as ap

from .main import main_function


def condition_based_pathways() -> None:
    # Define actions
    current_situation = ap.Action("Current situation")
    small_ships = ap.Action("Small ships")
    medium_ships = ap.Action("Medium ships")
    small_dredging = ap.Action("Small dredging")
    large_dredging = ap.Action("Large dredging")

    # TODO How to model action combination possibilities?
    medium_ships_and_small_dredging = ap.CombinedAction([medium_ships, small_dredging])

    # Create actions graph
    sequence_graph = ap.graph.SequenceGraph()

    sequence_graph.add_sequence(current_situation, small_ships)
    sequence_graph.add_sequence(current_situation, medium_ships)
    sequence_graph.add_sequence(current_situation, small_dredging)
    sequence_graph.add_sequence(current_situation, large_dredging)
    sequence_graph.add_sequence(medium_ships, small_ships)
    sequence_graph.add_sequence(medium_ships, small_dredging)
    sequence_graph.add_sequence(medium_ships, large_dredging)
    sequence_graph.add_sequence(small_dredging, small_ships)
    sequence_graph.add_sequence(small_dredging, medium_ships_and_small_dredging)
    sequence_graph.add_sequence(small_dredging, large_dredging)

    # Create pathways graph
    pathway_graph = ap.graph.sequence_graph_to_pathway_graph(sequence_graph)

    # Define tipping points in terms of sedimentation rates

    # Define scenarios in terms of time relative to sedimentation rates
    # High sediment deposition
    # Low sediment deposition

    # Create some plot that contains all information we want to see in the pathway map

    plt.clf()
    axis = plt.subplot(211)
    axis.set_title("Actions graph")
    nx.draw_planar(sequence_graph.graph, with_labels=True, font_size="xx-small")
    axis = plt.subplot(212)
    axis.set_title("Pathways graph")
    nx.draw_planar(pathway_graph.graph, with_labels=True, font_size="xx-small")
    plt.savefig("condition_based_pathways.pdf", bbox_inches="tight")


def time_based_pathways() -> None:
    # Define actions
    current_situation = ap.Action("current situation")
    pump_capacity = ap.Action("pump capacity 500m³/s situation")
    discharge_capacity = ap.Action("discharge capacity doubling")
    increase_water_level_and_dikes1 = ap.Action(
        "increase water level 0.2m and dikes 0.5m"
    )
    increase_water_level_and_dikes2 = ap.Action(
        "increase water level 0.2m and dikes 1.0m"
    )

    pump_capacity_and_increase_water_level_and_dikes1 = ap.CombinedAction(
        [pump_capacity, increase_water_level_and_dikes1]
    )
    discharge_capacity_and_increase_water_level_and_dikes1 = ap.CombinedAction(
        [discharge_capacity, increase_water_level_and_dikes1]
    )
    increase_water_level_and_dikes1_and_pump_capacity = ap.CombinedAction(
        [increase_water_level_and_dikes1, pump_capacity]
    )
    increase_water_level_and_dikes1_and_discharge_capacity = ap.CombinedAction(
        [increase_water_level_and_dikes1, discharge_capacity]
    )

    # Create actions graph
    sequence_graph = ap.graph.SequenceGraph()

    sequence_graph.add_sequence(current_situation, pump_capacity)
    sequence_graph.add_sequence(current_situation, discharge_capacity)
    sequence_graph.add_sequence(current_situation, increase_water_level_and_dikes1)
    sequence_graph.add_sequence(current_situation, increase_water_level_and_dikes2)
    sequence_graph.add_sequence(pump_capacity, discharge_capacity)
    sequence_graph.add_sequence(
        pump_capacity, pump_capacity_and_increase_water_level_and_dikes1
    )
    sequence_graph.add_sequence(
        discharge_capacity, discharge_capacity_and_increase_water_level_and_dikes1
    )
    sequence_graph.add_sequence(
        increase_water_level_and_dikes1,
        increase_water_level_and_dikes1_and_pump_capacity,
    )
    sequence_graph.add_sequence(
        increase_water_level_and_dikes1,
        increase_water_level_and_dikes1_and_discharge_capacity,
    )

    # Create pathways graph
    pathway_graph = ap.graph.sequence_graph_to_pathway_graph(sequence_graph)

    plt.clf()
    axis = plt.subplot(211)
    axis.set_title("Actions graph")
    nx.draw_planar(sequence_graph.graph, with_labels=True, font_size="xx-small")
    axis = plt.subplot(212)
    axis.set_title("Pathways graph")
    nx.draw_planar(pathway_graph.graph, with_labels=True, font_size="xx-small")
    plt.savefig("time_based_pathways.pdf", bbox_inches="tight")


@main_function
def flyer_examples() -> int:
    condition_based_pathways()
    time_based_pathways()
    return 0


def main() -> int:
    command = os.path.basename(sys.argv[0])
    usage = f"""\
Replicate examples from flyer

Usage:
    {command}

Options:
    -h --help          Show this screen and exit
    --version          Show version and exit
"""

    arguments = sys.argv[1:]
    arguments = docopt.docopt(usage, arguments, version=ap.__version__)

    return flyer_examples()
