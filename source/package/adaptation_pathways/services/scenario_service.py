from model.scenario import Scenario
from model.metric import Metric

class ScenarioService:
    def estimate_metric_at_time(
            scenario: Scenario,
            metric: Metric,
            time: float
    ) -> float:
        # Replace with a linear interpolation/extrapolation using the nearest points
        return metric.current_value
