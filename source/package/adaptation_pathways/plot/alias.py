from ..action import Action
from .colour import Colour, Colours  # pylint: disable=unused-import


ColourByAction = dict[Action, Colour]
ColourByActionName = dict[str, Colour]
