import dataclasses

from metric import Metric, MetricValue


@dataclasses.dataclass
class TimeSeriesPoint:
    time: float
    data: MetricValue | None


@dataclasses.dataclass
class Scenario:
    id: str
    name: str
    metric_data_over_time: dict[Metric, list[TimeSeriesPoint]]
