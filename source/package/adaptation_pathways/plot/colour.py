from dataclasses import dataclass

from ..graph.pathway_graph import PathwayGraph
from ..graph.pathway_map import PathwayMap
from ..graph.sequence_graph import SequenceGraph


Colour = tuple[float, float, float, float]
Colours = list[Colour]


@dataclass
class PlotColours:
    node_colours: Colours | None = None
    edge_colours: Colours | None = None
    node_edge_colours: Colours | None = None
    label_colour: Colour | None = None


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


def default_transparency():
    return 1.0  # 0.75


def default_nominal_palette() -> Colours:
    palette = [colour + (default_transparency(),) for colour in nord_palette_nominal]
    palette.append(nord_palette_blue[0] + (default_transparency(),))

    return palette


def default_edge_colours(
    graph: SequenceGraph | PathwayGraph,
) -> Colours:
    colour = nord_palette_dark[3] + (default_transparency(),)
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_node_edge_colours(
    graph: SequenceGraph | PathwayGraph | PathwayMap,
) -> Colours:
    colour = nord_palette_dark[3] + (default_transparency(),)
    colours = [colour] * len(list(graph.graph.edges))

    return colours


def default_label_colour() -> Colour:
    return nord_palette_dark[0] + (default_transparency(),)
