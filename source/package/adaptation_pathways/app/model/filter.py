import dataclasses

from action import Action
from comparisons import NumberComparison, SequenceComparison
from metric import Metric


@dataclasses.dataclass
class ActionFilter:
    relation: SequenceComparison
    actions: list[Action]
    actions_in_order: bool


@dataclasses.dataclass
class MetricFilter:
    metric: Metric
    relation: NumberComparison
    value: float


@dataclasses.dataclass
class GenerationConstraints:
    action_constraints: list[ActionFilter]
    metric_constraints: list[MetricFilter]
    max_sequence_length: int | None = None
