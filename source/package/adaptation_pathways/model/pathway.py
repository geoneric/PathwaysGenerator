from metric import Metric, MetricValue
from action import Action

class Pathway:
    id: str
    actions: list[Action]
    metric_data: dict[Metric, MetricValue | None]

