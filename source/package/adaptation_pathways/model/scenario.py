from metric import Metric, MetricValue

class TimeSeriesPoint:
    time: float
    data: MetricValue | None

class Scenario:
    id: str
    name: str
    metric_data_over_time: dict[Metric, list[TimeSeriesPoint]]
