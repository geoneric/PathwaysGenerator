import typing

import matplotlib as mpl
import matplotlib.lines as mlines

from ...action import Action
from ...graph import PathwayMap
from ...graph.node import ActionEnd
from .. import alias
from ..plot import configure_title


def _configure_x_axes(
    axes: mpl.axes.Axes,
    *,
    arguments: dict[str, typing.Any],
):

    # Top x-axis
    axes.spines.top.set_visible(False)

    # Bottom x-axis
    axes.spines.bottom.set_visible(True)
    axes.tick_params(bottom=True)
    axes.set_xlabel(arguments.get("x_label", ""))

    x_ticks = axes.get_xticks()

    if len(x_ticks) > 0:
        x_ticks = x_ticks[1:]

    x_labels = [f"{int(tick)}" for tick in x_ticks]
    axes.set_xticks(x_ticks, labels=x_labels)


def _configure_y_axes(
    axes: mpl.axes.Axes,
    paths: list[list[typing.Any]],
    *,
    arguments: dict[str, typing.Any],
):

    label_by_pathway: dict[Action, str] = arguments["label_by_pathway"]

    leaf_action_ends = [path[-1] for path in paths]
    assert all(isinstance(action_end, ActionEnd) for action_end in leaf_action_ends)
    leaf_actions = [action_end.action for action_end in leaf_action_ends]

    labels = [label_by_pathway[action] for action in leaf_actions]

    y_coordinates = list(range(len(paths)))

    axes.set_yticks(y_coordinates, labels=labels)
    axes.invert_yaxis()  # labels read top-to-bottom


def _configure_legend(
    axes, action_names: set[str], colour_by_action_name, *, arguments
):

    # Iterate over all actions that are shown on the y-axis. For each of these create a proxy artist. Then
    # create the legend, passing in the proxy artists.

    colours = [colour_by_action_name[name] for name in action_names]
    handles = []

    for label, colour in zip(action_names, colours):
        handles.append(mlines.Line2D([], [], color=colour, label=label))

    axes.legend(handles=handles, **arguments)


def _plot_annotations(
    axes,
    paths: list[list[typing.Any]],
    action_names: set[str],
    *,
    arguments: dict[str, typing.Any],
    legend_arguments: dict[str, typing.Any],
):
    configure_title(axes, arguments=arguments)
    _configure_y_axes(axes, paths, arguments=arguments)
    _configure_x_axes(axes, arguments=arguments)

    show_legend: bool = arguments.get("show_legend", False)

    if show_legend:
        colour_by_action_name: dict[Action, alias.Colour] = arguments[
            "colour_by_action_name"
        ]
        _configure_legend(
            axes, action_names, colour_by_action_name, arguments=legend_arguments
        )


def plot_bars(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    *,
    arguments: dict[str, typing.Any] | None = None,
    legend_arguments: dict[str, typing.Any] | None = None,
) -> None:
    """
    Plot a bar plot
    """
    if arguments is None:
        arguments = {}

    if legend_arguments is None:
        legend_arguments = {}

    colour_by_action_name: dict[Action, alias.Colour] = arguments[
        "colour_by_action_name"
    ]

    paths = pathway_map.all_paths()

    if "label_by_pathway" not in arguments:
        # Each pathway is uniquely identified by the action instance of its leaf node
        arguments["label_by_pathway"] = {
            leaf_node.action: f"{idx}"
            for idx, leaf_node in enumerate(pathway_map.leaf_nodes())
        }

    if "stack_bars" not in arguments:
        arguments["stack_bars"] = False

    stack_bars: bool = arguments["stack_bars"]

    bar_height = 0.8 if not stack_bars else 1.0

    # TODO Trying to get a fix bar height for multiple plots
    # max_nr_bars = 3
    # axes.set_ylim(-0.5 * bar_height, max_nr_bars - 0.5 * bar_height)

    min_tipping_point, max_tipping_point = pathway_map.tipping_point_range()
    tipping_point_range = max_tipping_point - min_tipping_point
    assert tipping_point_range >= 0

    for idx, path in enumerate(paths):
        y = idx
        action_ends = list(path[1::2])

        x = [action_end.tipping_point for action_end in action_ends]
        x = [x[0] - 0.1 * tipping_point_range] + x

        starts = x[:-1]
        widths = [end - start for start, end in zip(x, x[1:])]

        colours = [
            colour_by_action_name[action_end.action.name] for action_end in action_ends
        ]
        edge_colours = colours if stack_bars else "black"

        axes.barh(
            y,
            width=widths,
            height=bar_height,
            left=starts,
            align="center",
            color=colours,
            edgecolor=edge_colours,
        )

    action_names = {action.name for action in pathway_map.actions()}
    _plot_annotations(
        axes,
        paths,
        action_names,
        arguments=arguments,
        legend_arguments=legend_arguments,
    )

    axes.autoscale_view()
