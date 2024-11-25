import dataclasses

from comparisons import SequenceComparison
from metric import Metric, MetricValue


@dataclasses.dataclass
class Action:
    id: str
    name: str
    color: str
    icon: str
    metric_data: dict[Metric, MetricValue | None]


@dataclasses.dataclass
class ActionDependency:
    id: str
    action: Action
    relation: SequenceComparison
    other_actions: list[Action]
    actions_in_order: bool
