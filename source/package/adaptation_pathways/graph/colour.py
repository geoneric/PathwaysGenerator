from .node import Action, ActionBegin, ActionConversion, ActionEnd
from .pathway_graph import PathwayGraph
from .pathway_map import PathwayMap
from .sequence_graph import SequenceGraph


nord_palette_nominal = [
    (191 / 255, 97 / 255, 106 / 255),  # Redish
    (208 / 255, 135 / 255, 112 / 255),  # Orange
    (235 / 255, 203 / 255, 139 / 255),  # Dark yellow
    (163 / 255, 190 / 255, 140 / 255),  # Green
    (180 / 255, 142 / 255, 173 / 255),  # Purple
]

nord_palette_dark = [
    (46 / 255, 52 / 255, 64 / 255),  # Dark
    (59 / 255, 66 / 255, 82 / 255),  # Lighter than nord0
    (67 / 255, 76 / 255, 94 / 255),  # Lighter than nord1
    (76 / 255, 86 / 255, 106 / 255),  # Lighter than nord2
]

nord_palette_light = [
    (216 / 255, 222 / 255, 233 / 255),  # Bright
    (229 / 255, 233 / 255, 240 / 255),  # Lighter than nord4
    (236 / 255, 239 / 255, 244 / 255),  # Lighter than nord5
]

nord_palette_blue = [
    (143 / 255, 188 / 255, 187 / 255),  # Calm, frozen polar water
    (136 / 255, 192 / 255, 208 / 255),  # Bright, shiny, pure and clear ice
    (129 / 255, 161 / 255, 193 / 255),  # Darkened, arctic waters
    (94 / 255, 129 / 255, 172 / 255),  # Dark, deep arctic ocean
]


def default_node_colours_sequence_graph(
    graph: SequenceGraph,
) -> list[tuple[float, float, float, float]]:
    transparency = 0.75
    palette = [colour + (transparency,) for colour in nord_palette_nominal]
    palette.append(nord_palette_blue[0] + (transparency,))

    palette_size = len(palette)
    colour_by_action = {}
    colours = []

    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        assert isinstance(node, Action)
        if node not in colour_by_action:
            colour_by_action[node] = palette[idx % palette_size]
            idx += 1
        colours.append(colour_by_action[node])

    return colours


def default_node_colours_pathway_graph(
    graph: PathwayGraph,
) -> list[tuple[float, float, float, float]]:
    transparency = 0.75
    palette = [colour + (transparency,) for colour in nord_palette_nominal]
    palette.append(nord_palette_blue[0] + (transparency,))

    palette_size = len(palette)
    conversion_colour = nord_palette_light[0] + (transparency,)

    colour_by_action = {}
    colours = []

    # Use the same colour for conversions
    # Colour each unique action unique
    idx = 0

    for node in graph._graph.nodes:
        assert type(node) in [Action, ActionConversion]
        if isinstance(node, Action):
            if node not in colour_by_action:
                colour_by_action[node] = palette[idx % palette_size]
                idx += 1
            colours.append(colour_by_action[node])
        elif isinstance(node, ActionConversion):
            colours.append(conversion_colour)

    return colours


def default_node_colours_pathway_map(
    graph: PathwayMap,
) -> list[tuple[float, float, float, float]]:
    transparency = 0.75
    palette = [colour + (transparency,) for colour in nord_palette_nominal]
    palette.append(nord_palette_blue[0] + (transparency,))

    palette_size = len(palette)

    colour_by_action = {}
    colours = []

    # Colour each action begin / end combo unique
    idx = 0

    for node in graph._graph.nodes:
        assert type(node) in [ActionBegin, ActionEnd]

        if node.action not in colour_by_action:
            colour_by_action[node.action] = palette[idx % palette_size]
            idx += 1
        colours.append(colour_by_action[node.action])

    return colours


def default_edge_colours(
    graph: SequenceGraph | PathwayGraph | PathwayMap,
) -> list[tuple[float, float, float, float]]:
    transparency = 0.75
    edge_colour = nord_palette_dark[3] + (transparency,)
    edge_colours = [edge_colour] * len(list(graph.graph.edges))

    return edge_colours
