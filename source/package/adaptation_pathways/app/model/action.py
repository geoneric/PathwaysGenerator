import dataclasses

from .comparisons import SequenceComparison
from .metric import Metric, MetricValue


@dataclasses.dataclass
class Action:
    id: str
    name: str
    color: str
    icon: str
    metric_data: dict[Metric, MetricValue | None]

    def get_data(self, metric) -> MetricValue | None:
        if metric not in self.metric_data:
            return None

        return self.metric_data[metric]


@dataclasses.dataclass
class ActionDependency:
    id: str
    action: Action
    relation: SequenceComparison
    other_actions: list[Action]
    actions_in_order: bool
