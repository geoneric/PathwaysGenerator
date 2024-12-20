import math
import typing

import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.markers as mmarkers
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import BboxImage
from matplotlib.legend_handler import HandlerBase
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.transforms import Bbox, TransformedBbox

from ...action import Action
from ...action_combination import ActionCombination
from ...graph import PathwayMap
from ...graph.node import ActionBegin, ActionEnd
from .. import alias
from ..util import add_position, distribute, group_overlapping_regions_with_payloads


def _plot_action_lines(
    axes,
    pathway_map,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    *,
    arguments: dict[str, typing.Any],
) -> mpl.collections.LineCollection:

    tipping_point_overshoot: float = arguments.get("tipping_point_overshoot", 0)
    colour_by_action_name: dict[Action, alias.Colour] = arguments[
        "colour_by_action_name"
    ]

    edge_nodes = list(pathway_map.graph.edges())
    edge_collection = mpl.collections.LineCollection([])

    if len(edge_nodes) > 0:
        edges = np.asarray([(layout[edge[0]], layout[edge[1]]) for edge in edge_nodes])

        # Each edge consists of a start and end point. In case the y-coordinate of both points is the same,
        # then the end point corresponds with a tipping point. The x-coordinate of this point must be tweaked,
        # given the tipping_point_overshoot passed in.

        for edge in edges:
            if edge[0][1] == edge[1][1]:
                edge[1][0] += tipping_point_overshoot

        colours = [colour_by_action_name[edge[0].action.name] for edge in edge_nodes]

        edge_collection = mpl.collections.LineCollection(
            edges,
            colors=colours,
        )
        axes.add_collection(edge_collection)

    return edge_collection


def _plot_action_starts(
    axes,
    pathway_map,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    *,
    arguments: dict[str, typing.Any],
) -> mpl.collections.PathCollection:

    start_action_marker: mmarkers.MarkerStyle = arguments.get(
        "start_action_marker", "o"
    )
    colour_by_action_name: dict[Action, alias.Colour] = arguments[
        "colour_by_action_name"
    ]

    nodes = pathway_map.all_action_begins()
    path_collection = mpl.collections.PathCollection(None)

    if len(nodes) > 0:
        node_pos = np.asarray([layout[node] for node in nodes])
        x, y = zip(*node_pos)
        colours = [colour_by_action_name[node.action.name] for node in nodes]
        path_collection = axes.scatter(
            x, y, marker=start_action_marker, c=colours
        )  # , c = node_colours) , s=100)

    return path_collection


def _plot_action_tipping_points(
    axes,
    pathway_map,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    *,
    arguments: dict[str, typing.Any],
) -> mpl.collections.PathCollection:

    tipping_point_overshoot: float = arguments.get("tipping_point_overshoot", 0)
    tipping_point_marker: mmarkers.MarkerStyle = arguments.get(
        "tipping_point_marker", "|" if tipping_point_overshoot > 0 else "o"
    )
    if isinstance(tipping_point_marker, str):
        tipping_point_marker = mmarkers.MarkerStyle(tipping_point_marker)
    tipping_point_face_colour = arguments.get("tipping_point_face_colour", "white")
    colour_by_action_name: dict[Action, alias.Colour] = arguments[
        "colour_by_action_name"
    ]

    nodes = pathway_map.all_action_ends()
    path_collection = mpl.collections.PathCollection(None)

    if len(nodes) > 0:
        # TODO Skip the tipping point at the end of each individual path way
        node_pos = np.asarray([layout[v] for v in nodes])
        x, y = zip(*node_pos)
        x = np.array(x) + tipping_point_overshoot
        colours = [colour_by_action_name[node.action.name] for node in nodes]

        if tipping_point_marker.is_filled():
            scatter_arguments = {
                "edgecolor": colours,
                "facecolor": tipping_point_face_colour,
            }
        else:
            scatter_arguments = {
                "facecolor": colours,
            }

        path_collection = axes.scatter(
            x, y, marker=tipping_point_marker, **scatter_arguments
        )

    return path_collection


def _configure_title(
    axes,
    *,
    arguments: dict[str, typing.Any],
) -> None:

    title: str = arguments.get("title", "")

    if len(title) > 0:
        axes.set_title(title)


# pylint: disable-next=too-many-locals
def _configure_y_axes(
    axes,
    y_coordinate_by_action_name: dict[str, float],
    *,
    icon_pathnames,
    arguments: dict[str, typing.Any],
):

    # Left y-axis
    axes.spines.left.set_visible(False)
    axes.tick_params(left=False)

    y_coordinates = list(y_coordinate_by_action_name.values())
    y_labels = list(y_coordinate_by_action_name.keys())
    colour_by_action_name: dict[str, alias.Colour] = arguments["colour_by_action_name"]
    label_colours = [colour_by_action_name[label] for label in y_labels]

    show_icons = len(icon_pathnames) > 0

    if not show_icons:
        axes.set_yticks(y_coordinates, labels=y_labels)

        for colour, tick, label in zip(
            label_colours, axes.yaxis.get_major_ticks(), y_labels
        ):
            tick.label1.set_color(colour)
    else:
        axes.set_yticks(y_coordinates, labels="")
        ytick_labels = axes.get_yticklabels()

        for idx, y_tick in enumerate(ytick_labels):
            x_coordinate, y_coordinate = y_tick.get_position()
            array = plt.imread(icon_pathnames[idx])
            _, nr_cols, _ = array.shape
            zoom = nr_cols * 3e-5
            image = OffsetImage(array, zoom=zoom)
            image.image.axes = axes
            annotation = AnnotationBbox(
                offsetbox=image,
                xycoords=("axes fraction", "data"),
                xy=(x_coordinate, y_coordinate),
                boxcoords="offset points",
                xybox=(-0.5 * zoom * nr_cols, 0),
                frameon=False,
            )
            axes.add_artist(annotation)

    # Right y-axis
    axes.spines.right.set_visible(False)

    return y_labels, label_colours


def _configure_x_axes(
    axes,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    *,
    arguments: dict[str, typing.Any],
):

    # Top x-axis
    axes.spines.top.set_visible(False)

    # Bottom x-axis
    axes.spines.bottom.set_visible(True)
    axes.tick_params(bottom=True)
    axes.set_xlabel(arguments.get("x_label", ""))

    if len(layout) > 0:
        # TODO Still needed?
        # coordinates = np.concatenate(list(layout.values())).reshape(len(layout), 2)
        # _update_data_limits(axes, coordinates)

        x_ticks = axes.get_xticks()

        if len(x_ticks) > 0:
            x_ticks = x_ticks[1:]

        x_labels = [f"{int(tick)}" for tick in x_ticks]
        axes.set_xticks(x_ticks, labels=x_labels)


class IconHandler(HandlerBase):

    def __init__(self, *, pathname=""):
        self.image_data = plt.imread(pathname)
        self.space = 0  # 15
        self.offset = 10

        super().__init__()

    # pylint: disable-next=too-many-arguments, too-many-positional-arguments
    def create_artists(
        self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
    ):
        bb = Bbox.from_bounds(
            xdescent + (width + self.space) / 3.0 + self.offset,
            ydescent,
            height * self.image_data.shape[1] / self.image_data.shape[0],
            height,
        )

        tbb = TransformedBbox(bb, trans)
        image = BboxImage(tbb)
        image.set_data(self.image_data)

        self.update_prop(image, orig_handle, legend)

        return [image]


def _configure_legend(axes, *, labels, colours, icon_pathnames: list[str], arguments):

    # TODO Document this:
    # - Use rcParams["legend.*"] to tweak the default appearance of the legend
    # - Use kwargs to override the default appearance of the legend
    # See also:
    # - https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html#matplotlib.axes.Axes.legend

    # Iterate over all actions that are shown on the y-axis. For each of these create a proxy artist. Then
    # create the legend, passing in the proxy artists.

    # TODO Maybe we need to do something about the ordering(?)

    show_icons = len(icon_pathnames) > 0
    handles = []
    handler_map = {}

    for colour in colours:
        handles.append(mlines.Line2D([], [], color=colour))

    if show_icons:
        # Install a custom handler that will draw an icon instead of the line just created
        for idx, handle in enumerate(handles):
            handler = IconHandler(pathname=icon_pathnames[idx])
            handler_map[handle] = handler

    axes.legend(handles=handles, labels=labels, handler_map=handler_map, **arguments)


def _plot_annotations(
    axes,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    y_coordinate_by_action_name: dict[str, float],
    *,
    arguments: dict[str, typing.Any],
    legend_arguments: dict[str, typing.Any],
) -> None:
    icon_pathnames = arguments.get("icon_pathnames", [])

    _configure_title(axes, arguments=arguments)
    y_labels, label_colours = _configure_y_axes(
        axes,
        y_coordinate_by_action_name,
        icon_pathnames=icon_pathnames,
        arguments=arguments,
    )
    _configure_x_axes(axes, layout, arguments=arguments)

    show_legend: bool = arguments.get("show_legend", False)

    if show_legend:
        _configure_legend(
            axes,
            labels=y_labels,
            colours=label_colours,
            icon_pathnames=icon_pathnames,
            arguments=legend_arguments,
        )


# pylint: disable-next=too-many-arguments
def classic_pathway_map_plotter(
    axes,
    pathway_map,
    layout: dict[ActionBegin | ActionEnd, np.ndarray],
    y_coordinate_by_action_name: dict[str, float],
    *,
    arguments: dict[str, typing.Any],
    legend_arguments: dict[str, typing.Any],
) -> None:

    # Components of a metro map, drawn in increasing z-order:
    # - Action lines
    # - Action start points
    # - Action tipping points
    # - Title, axes and legend

    edge_collection = _plot_action_lines(axes, pathway_map, layout, arguments=arguments)
    edge_collection.set_zorder(0)

    node_collection = _plot_action_starts(
        axes, pathway_map, layout, arguments=arguments
    )
    node_collection.set_zorder(1)

    node_collection = _plot_action_tipping_points(
        axes, pathway_map, layout, arguments=arguments
    )
    node_collection.set_zorder(1)

    _plot_annotations(
        axes,
        layout,
        y_coordinate_by_action_name,
        arguments=arguments,
        legend_arguments=legend_arguments,
    )

    axes.autoscale_view()


def _group_overlapping_regions(
    regions: list[tuple[alias.Region, typing.Any]]
) -> list[list[tuple[alias.Region, typing.Any]]]:

    # Given a list of tuples of regions and their payload (additional information not relevant here):
    # - Group the regions into overlapping regions
    # - Return a list of overlapping regions, along with their payload

    # Split list of tuple[Region, Payload] into list[Region] and list[Payload]
    # Group the regions
    # Re-associate each region with its payload again

    grouped_regions, grouped_payloads = group_overlapping_regions_with_payloads(
        *(list(tuples) for tuples in zip(*regions))
    )
    result: list[list[tuple[alias.Region, typing.Any]]] = []

    for region_group, payload_group in zip(grouped_regions, grouped_payloads):
        result.append(list(zip(region_group, payload_group)))

    return result


# pylint: disable-next=too-many-locals
def _spread_vertically(
    pathway_map: PathwayMap,
    position_by_node: dict[ActionBegin | ActionEnd, np.ndarray],
    overlapping_lines_spread: float,
) -> None:

    # - Assign all action_begin / action_end combinations to bins, by y-coordinate
    # - For those bins that contain more than one element, tweak the y-coordinates
    # - When tweaking y-coordinates take non-overlapping regions into account

    # Per y-coordinate a list of regions (x-coordinates), action begin/end tuples
    nodes_by_y: dict[
        float, list[tuple[alias.Region, tuple[ActionBegin, ActionEnd]]]
    ] = {}

    for action_begin in pathway_map.all_action_begins():
        action_end = pathway_map.action_end(action_begin)

        x_begin, y_begin = position_by_node[action_begin]
        x_end, y_end = position_by_node[action_end]
        assert x_end >= x_begin
        assert y_end == y_begin
        region = x_begin, x_end

        if y_begin not in nodes_by_y:
            nodes_by_y[y_begin] = []

        nodes_by_y[y_begin].append((region, (action_begin, action_end)))

    min_y = min(nodes_by_y.keys())
    max_y = max(nodes_by_y.keys())
    range_y = max_y - min_y

    for y_coordinate, regions in nodes_by_y.items():
        grouped_regions = _group_overlapping_regions(regions)

        for regions in grouped_regions:
            nr_regions = len(regions)

            if nr_regions > 1:
                y_coordinates = distribute(
                    nr_regions * [y_coordinate], overlapping_lines_spread * range_y
                )

                for idx in range(nr_regions):
                    action_begin, action_end = regions[idx][1]
                    position_by_node[action_begin][1] = y_coordinates[idx]
                    position_by_node[action_end][1] = y_coordinates[idx]


def _distribute_horizontally(
    pathway_map: PathwayMap,
    action_begin: ActionBegin,
    position_by_node: dict[ActionBegin | ActionEnd, np.ndarray],
) -> None:
    assert isinstance(action_begin, ActionBegin)

    action_end = pathway_map.action_end(action_begin)
    end_x = action_end.tipping_point

    add_position(position_by_node, action_end, (end_x, np.nan))

    for action_begin_new in pathway_map.action_begins(
        pathway_map.action_end(action_begin)
    ):
        begin_x = end_x

        add_position(position_by_node, action_begin_new, (begin_x, np.nan))
        _distribute_horizontally(pathway_map, action_begin_new, position_by_node)


# pylint: disable-next=too-many-locals
def _spread_horizontally(
    pathway_map: PathwayMap,
    position_by_node: dict[ActionBegin | ActionEnd, np.ndarray],
    overlapping_lines_spread: float,
) -> None:

    # - Assign all action_end / action_begin combinations to bins, by x-coordinate
    # - For those bins that contain more than one element, tweak the x-coordinates
    # - When tweaking x-coordinates take non-overlapping regions into account

    # Per x-coordinate a list of regions (y-coordinates), action end/begin tuples
    nodes_by_x: dict[
        float, list[tuple[alias.Region, tuple[ActionEnd, ActionBegin]]]
    ] = {}

    for action_end in pathway_map.all_action_ends():
        action_begins = pathway_map.action_begins(action_end)

        if action_begins:
            x_end, y_end = position_by_node[action_end]

            if x_end not in nodes_by_x:
                nodes_by_x[x_end] = []

            for action_begin in action_begins:
                x_begin, y_begin = position_by_node[action_begin]
                assert x_end == x_begin
                region = tuple(sorted([y_end, y_begin]))

                nodes_by_x[x_end].append((region, (action_end, action_begin)))

    min_x = min(nodes_by_x.keys())
    max_x = max(nodes_by_x.keys())
    range_x = max_x - min_x

    # Root action end. This x coordinate needs no tweaking.
    del nodes_by_x[min_x]

    for x_coordinate, regions in nodes_by_x.items():
        grouped_regions = _group_overlapping_regions(regions)

        for regions in grouped_regions:
            nr_regions = len(regions)

            if nr_regions > 1:
                x_coordinates = distribute(
                    nr_regions * [x_coordinate], overlapping_lines_spread * range_x
                )

                for idx in range(nr_regions):
                    action_end, action_begin = regions[idx][1]
                    position_by_node[action_end][0] = x_coordinates[idx]
                    position_by_node[action_begin][0] = x_coordinates[idx]


# pylint: disable-next=too-many-locals, too-many-branches
def _distribute_vertically(
    pathway_map: PathwayMap,
    root_action_begin: ActionBegin,
    position_by_node: dict[ActionBegin | ActionEnd, np.ndarray],
) -> dict[str, float]:

    action_end = pathway_map.action_end(root_action_begin)
    position_by_node[action_end][1] = position_by_node[root_action_begin][1]

    # min_distance = 1.0

    # All unique action instances in the graph
    actions = pathway_map.actions()

    # Sieve out combined actions that combine a single *existing* action with a *new* one. These
    # must be positioned at the same y-coordinate as the existing action. These combined actions
    # must not interfere with the distribution of y-coordinates.

    # Sieve out actions that only differ with respect to the edition. These must be positioned
    # at the same y-coordinate and must not interfere with the distribution of y-coordinates.

    action_combinations_sieved: dict[ActionCombination, Action] = {}
    action_combinations_continuations: dict[ActionCombination, list[Action]] = {}
    names_of_actions_to_distribute: list[str] = []

    for action in actions:
        if not isinstance(action, ActionCombination):
            if action.name not in names_of_actions_to_distribute:
                names_of_actions_to_distribute.append(action.name)
        else:
            continued_actions = pathway_map.continued_actions(action)

            if len(continued_actions) == 1:
                # Action is a combination of a single existing action with a new one
                action_combinations_sieved[action] = continued_actions[0]
            else:
                if len(continued_actions) > 1:
                    action_combinations_continuations[action] = continued_actions

                if action.name not in names_of_actions_to_distribute:
                    names_of_actions_to_distribute.append(action.name)

    # We now have the names of the actions to distribute. What is important here is that the
    # number of actions is correct.
    y_coordinates: list[float] = list(
        range(
            math.floor(len(names_of_actions_to_distribute) / 2),
            -math.floor((len(names_of_actions_to_distribute) - 1) / 2) - 1,
            -1,
        )
    )

    # Nodes related to the root action are already positioned
    # Delete the y-coordinate of the root action
    assert y_coordinates[math.floor(len(names_of_actions_to_distribute) / 2)] == 0.0
    del y_coordinates[math.floor(len(names_of_actions_to_distribute) / 2)]

    # Delete the name of the root action
    assert (
        names_of_actions_to_distribute[0] == root_action_begin.action.name
    ), names_of_actions_to_distribute[0]
    del names_of_actions_to_distribute[0]

    # Now it is time to re-order the actions to distribute, based on their level, if any was set
    level_by_action = (
        pathway_map.graph.graph["level_by_action"]
        if "level_by_action" in pathway_map.graph.graph
        else {}
    )

    # Update the levels of action combinations that continue multiple existing actions. These
    # must end up somewhere in between the continued actions.
    if level_by_action:
        for action, continued_actions in action_combinations_continuations.items():
            assert action in level_by_action
            level_by_action[action] = sum(
                level_by_action[action] for action in continued_actions
            ) / len(continued_actions)

    levels_of_actions_to_distribute = []

    for action_name in names_of_actions_to_distribute:
        level = next(
            (
                level_by_action[action]
                for action in actions
                if action.name == action_name and action in level_by_action
            ),
            0,
        )
        levels_of_actions_to_distribute.append(level)

    # Sort action names based on their individual level. Actions with lower levels must end up
    # higher in the pathway map.
    levels_of_actions_to_distribute, names_of_actions_to_distribute = (
        list(t)
        for t in zip(
            *sorted(
                zip(levels_of_actions_to_distribute, names_of_actions_to_distribute)
            )
        )
    )

    y_coordinate_by_action_name = dict(
        zip(names_of_actions_to_distribute, y_coordinates)
    )

    for action_begin in pathway_map.all_action_begins()[1:]:  # Skip root node
        action = action_begin.action

        if (
            isinstance(action, ActionCombination)
            and action in action_combinations_sieved
        ):
            # In this case we want the combination to end up at the same y-coordinate as the
            # one action that is being continued
            action = action_combinations_sieved[action]

        y_coordinate = y_coordinate_by_action_name[action.name]

        assert np.isnan(position_by_node[action_begin][1])
        position_by_node[action_begin][1] = y_coordinate
        action_end = pathway_map.action_end(action_begin)

        assert np.isnan(position_by_node[action_end][1])
        position_by_node[action_end][1] = y_coordinate

    y_coordinate_by_action_name[root_action_begin.action.name] = 0

    return y_coordinate_by_action_name


def _layout(
    pathway_map: PathwayMap,
    *,
    overlapping_lines_spread: float | tuple[float, float],
) -> tuple[dict[ActionBegin | ActionEnd, np.ndarray], dict[str, float]]:
    """
    Layout that replicates the pathway map layout of the original (pre-2024) pathway generator

    :param pathway_map: Pathway map
    :return: Node positions

    The layout has the following characteristics:

    - A pathway map is a stack of horizontal lines representing actions
    - Each action ends up at its own level in the stack
    - Pathways jump from horizontal line to horizontal line, depending on the sequences of
      actions that make up each pathway

    The pathway map passed in must contain sane tipping points. When in doubt, call
    ``verify_tipping_points()`` before calling this function.

    The graph in the pathway map passed in must contain an attribute called "level_by_action",
    with a numeric value per action, which corresponds with the position in the above mentioned
    stack. Low numbers correspond with a high position in the stack (large y-coordinate). Such
    actions will be positioned at the top of the pathway map.
    """
    position_by_node: dict[ActionBegin | ActionEnd, np.ndarray] = {}
    y_coordinate_by_action_name: dict[str, float] = {}

    if pathway_map.nr_edges() > 0:
        root_action_begin = pathway_map.root_node
        root_action_end = pathway_map.action_end(root_action_begin)
        tipping_point = root_action_end.tipping_point

        min_tipping_point, max_tipping_point = pathway_map.tipping_point_range()
        tipping_point_range = max_tipping_point - min_tipping_point
        assert tipping_point_range >= 0
        x_coordinate = tipping_point - 0.1 * tipping_point_range

        add_position(position_by_node, root_action_begin, (x_coordinate, 0))

        _distribute_horizontally(pathway_map, root_action_begin, position_by_node)
        y_coordinate_by_action_name = _distribute_vertically(
            pathway_map, root_action_begin, position_by_node
        )

        if not isinstance(overlapping_lines_spread, tuple):
            overlapping_lines_spread = (
                overlapping_lines_spread,
                overlapping_lines_spread,
            )

        horizontal_spread, vertical_spread = overlapping_lines_spread

        if horizontal_spread > 0:
            _spread_horizontally(pathway_map, position_by_node, horizontal_spread)
        if vertical_spread > 0:
            _spread_vertically(pathway_map, position_by_node, vertical_spread)

    return position_by_node, y_coordinate_by_action_name


def plot(
    axes: mpl.axes.Axes,
    pathway_map: PathwayMap,
    *,
    arguments: dict[str, typing.Any] | None = None,
    legend_arguments: dict[str, typing.Any] | None = None,
) -> None:

    if arguments is None:
        arguments = {}

    if legend_arguments is None:
        legend_arguments = {}

    overlapping_lines_spread: tuple[float, float] = arguments.get(
        "overlapping_lines_spread", (0, 0)
    )

    layout, y_coordinate_by_action_name = _layout(
        pathway_map, overlapping_lines_spread=overlapping_lines_spread
    )

    classic_pathway_map_plotter(
        axes,
        pathway_map,
        layout,
        y_coordinate_by_action_name,
        arguments=arguments,
        legend_arguments=legend_arguments,
    )
