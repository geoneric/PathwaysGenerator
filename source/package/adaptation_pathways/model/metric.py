from enum import Enum

class MetricEstimate(Enum):
    MANUAL = 1
    SUM = 2
    AVERAGE = 3
    MINIMUM = 4
    MAXIMUM = 5
    LAST = 6

class MetricUnit:
    symbol: str
    place_after_value: bool
    value_format: str

class Metric:
    id: str
    name: str
    unit: MetricUnit
    current_value: float
    estimate: MetricEstimate

class MetricValue:
    value: float
    is_estimate: bool
