from .action import Action
from .metric import Metric, MetricValue


class Pathway:
    id: str
    parent_id: str | None = None
    last_action: Action
    metric_data: dict[str, MetricValue]

    def __init__(
        self, pathway_id: str, last_action: Action, parent_id: str | None = None
    ):
        self.id = pathway_id
        self.parent_id = parent_id
        self.last_action = last_action
        self.metric_data = {}

    def get_formatted_value(self, metric: Metric) -> str:
        data = self.metric_data.get(metric.id, None)
        if data is None:
            return ""

        return metric.unit.format(data.value)
