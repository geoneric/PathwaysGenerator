"""
This module contains aliases to be used as type hints.
"""

from typing import Any, TypeAlias

import numpy as np

from ..action import Action
from ..graph.node import Node


Colour = tuple[float, float, float, float]
"""
A colour is represented by four floating point values [0, 1], representing RGBA values respectively
"""

Colours = list[Colour]
Style = str | tuple[int, tuple[int, int]]
Styles = list[Style]
FillStyle = str
FillStyles = list[Style]

ColourByActionName = dict[str, Colour]
"""
Per action name a colour
"""

LabelByPathway = dict[Action, str]
"""
Per pathway, identified by its leaf Action instance, a label
"""

LevelByActionName = dict[str, float]
"""
Per Action name a level
"""

LevelByPathway = dict[Action, float]
"""
Per pathway, identified by its leaf Action instance, a level
"""

MarkerByActionName = dict[str, Any]

MarkerStyle = dict


Region = tuple[float, float]

Position: TypeAlias = np.ndarray
PositionByNode = dict[Node, Position]
