"""
This module contains aliases to be used as type hints.
"""

from typing import TypeAlias

import numpy as np

from ..action import Action
from ..graph.node import Node


# from .colour import Colour, Colours  # pylint: disable=unused-import

Colour = tuple[float, float, float, float]
"""
A colour is represented by four floating point values [0, 1], representing RGBA values respectively
"""

Colours = list[Colour]
Style = str | tuple[int, tuple[int, int]]
Styles = list[Style]
FillStyle = str
FillStyles = list[Style]

ColourByAction = dict[Action, Colour]
ColourByActionName = dict[str, Colour]
LevelByAction = dict[Action, float]

Region = tuple[float, float]

Position: TypeAlias = np.ndarray
PositionByNode = dict[Node, Position]
