from comparisons import SequenceComparison, NumberComparison
from metric import Metric
from action import Action

class ActionFilter:
    relation: SequenceComparison
    actions: list[Action]
    actions_in_order: bool

class MetricFilter:
    metric: Metric
    relation: NumberComparison
    value: float
