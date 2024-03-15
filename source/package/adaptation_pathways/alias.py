from .action import Action
from .action_combination import ActionCombination
from .plot.alias import *  # pylint: disable=wildcard-import, unused-wildcard-import


Actions = list[Action | ActionCombination]
Sequences = list[tuple[Action, Action]]
TippingPointByAction = dict[Action, int]
