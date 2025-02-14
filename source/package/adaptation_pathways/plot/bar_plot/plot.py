import typing

import matplotlib.lines as mlines

from ...alias import TippingPointByAction
from ...graph import PathwayMap, tipping_point_range
from ...graph.node import ActionEnd
from ..alias import ColourByActionName, LevelByAction
from ..colour import default_nominal_palette
from ..pathway_map.colour import colour_by_action_name_pathway_map
from ..plot import configure_title


def _configure_x_axes(
    axes,
    *,
    x_label,
):
    # Top x-axis
    axes.spines.top.set_visible(False)

    # Bottom x-axis
    axes.spines.bottom.set_visible(True)
    axes.tick_params(bottom=True)
    axes.set_xlabel(x_label)

    x_ticks = axes.get_xticks()

    if len(x_ticks) > 0:
        x_ticks = x_ticks[1:]

    x_labels = [f"{int(tick)}" for tick in x_ticks]
    axes.set_xticks(x_ticks, labels=x_labels)


def _configure_y_axes(
    axes,
    paths: list[list[typing.Any]],
    *,
    label_by_pathway,
):
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
    colour_by_action_name,
    label_by_pathway,
    legend_arguments: dict[str, typing.Any],
    show_legend,
    title,
    x_label,
):
    configure_title(axes, title=title)
    _configure_y_axes(axes, paths, label_by_pathway=label_by_pathway)
    _configure_x_axes(axes, x_label=x_label)

    if show_legend:
        _configure_legend(
            axes, action_names, colour_by_action_name, arguments=legend_arguments
        )


def plot_bars(
    axes,
    pathway_map: PathwayMap,
    *,
    colour_by_action_name: ColourByActionName | None = None,
    label_by_pathway: dict[ActionEnd, str] | None = None,
    legend_arguments: dict[str, typing.Any] | None = None,
    level_by_action: LevelByAction | None = None,  # pylint: disable=unused-argument
    show_legend: bool = False,
    stack_bars: bool = False,
    tipping_point_by_action: TippingPointByAction,
    title: str = "",
    x_label: str = "",
) -> None:
    """
    Plot a bar plot
    """

    if colour_by_action_name is None:
        colour_by_action_name = colour_by_action_name_pathway_map(
            pathway_map, default_nominal_palette()
        )

    if label_by_pathway is None:
        # Each pathway is uniquely identified by the action instance of its leaf node
        label_by_pathway = {
            leaf_node.action: "" for leaf_node in pathway_map.leaf_nodes()
        }

    if legend_arguments is None:
        legend_arguments = {}

    paths = pathway_map.all_paths()

    bar_height = 0.8 if not stack_bars else 1.0

    # TODO Trying to get a fix bar height for multiple plots
    # max_nr_bars = 3
    # axes.set_ylim(-0.5 * bar_height, max_nr_bars - 0.5 * bar_height)

    min_tipping_point, max_tipping_point = tipping_point_range(
        pathway_map, tipping_point_by_action
    )
    tipping_point_range_ = max_tipping_point - min_tipping_point
    assert tipping_point_range_ >= 0

    for idx, path in enumerate(paths):
        y = idx
        action_ends = list(path[1::2])

        x = [tipping_point_by_action[action_end.action] for action_end in action_ends]
        x = [x[0] - 0.1 * tipping_point_range_] + x

        starts = x[:-1]
        widths = [end - start for start, end in zip(x, x[1:])]

        colours = [
            colour_by_action_name[action_end.action.name] for action_end in action_ends
        ]
        # edge_colours = colours if stack_bars else "black"
        edge_colours = None

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
        colour_by_action_name=colour_by_action_name,
        label_by_pathway=label_by_pathway,
        legend_arguments=legend_arguments,
        show_legend=show_legend,
        title=title,
        x_label=x_label,
    )

    axes.autoscale_view()
