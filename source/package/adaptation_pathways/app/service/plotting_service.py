# pylint: disable=too-few-public-methods,unused-argument
"""
Methods for drawing charts and graphs
"""
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from adaptation_pathways.action import Action
from adaptation_pathways.alias import Sequence, TippingPointByAction
from adaptation_pathways.app.model.pathway import Pathway
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.model.scenario import Scenario
from adaptation_pathways.graph import (
    SequenceGraph,
    sequence_graph_to_pathway_map,
    verify_tipping_points,
)
from adaptation_pathways.graph.node.action import Action as ActionNode
from adaptation_pathways.plot import init_axes, plot_classic_pathway_map
from adaptation_pathways.plot.util import action_level_by_first_occurrence


matplotlib.use("svg")


class PlottingService:
    @staticmethod
    def draw_metro_map(
        project: PathwaysProject, for_export=False
    ) -> tuple[Figure, Axes]:

        action_nodes: dict[str, ActionNode] = {}
        tipping_points: TippingPointByAction = {}
        action_colors: dict[str, str] = {}
        root_pathway = project.root_pathway
        metric = project.graph_metric
        scenario: Scenario | None = (
            None if not project.graph_is_time else project.graph_scenario
        )

        def get_tipping_point(pathway: Pathway) -> float:
            metric_value = pathway.metric_data.get(metric.id, None)
            if metric_value is None:
                metric_value = root_pathway.metric_data.get(metric.id, None)

            if metric_value is None:
                return 0

            if scenario is not None:
                return scenario.estimate_tipping_point(metric.id, metric_value.value)

            return metric_value.value

        # Create action node for each pathway
        for pathway in project.all_pathways:
            pathway_action = project.get_action(pathway.action_id)
            action = Action(pathway_action.name)
            action_node = ActionNode(action)
            action_nodes[pathway.id] = action_node
            action_colors[action.name] = pathway_action.color
            tipping_points[action] = get_tipping_point(pathway)

        # Populate sequences
        sequence_graph = SequenceGraph()
        sequences: list[Sequence] = []

        for pathway in project.all_pathways:
            if pathway.parent_id is None:
                continue

            action_node = action_nodes[pathway.id]
            parent_action_node = action_nodes[pathway.parent_id]
            sequence_graph.add_sequence(parent_action_node, action_node)
            sequences.append((parent_action_node.action, action_node.action))

        # Mostly copied from plot_pathway_map.py
        level_by_action = action_level_by_first_occurrence(sequences)
        pathway_map = sequence_graph_to_pathway_map(sequence_graph)

        verify_tipping_points(pathway_map, tipping_points)

        figure, axes = plt.subplots(layout="constrained")
        init_axes(axes)

        arguments: dict[str, Any] = {
            "colour_by_action_name": action_colors,
            "level_by_action": level_by_action,
            "overlapping_lines_spread": 0.02,
            "tipping_points": tipping_points,
            "tipping_point_overshoot": 0.2,
        }

        if for_export:
            arguments["x_label"] = f"{metric.name} ({metric.unit.symbol})"
            arguments["show_legend"] = True

        plot_classic_pathway_map(axes, pathway_map, arguments=arguments)

        return (figure, axes)
