from model.filter import ActionFilter, MetricFilter
from model.pathway import Pathway
from model.action import Action
from model.metric import Metric, MetricEstimate

class PathwayService:
    @staticmethod
    def filter_pathways(
            all_pathways: list[Pathway], 
            action_filters: list[ActionFilter], 
            metric_filters: list[MetricFilter]
    ) -> list[Pathway]:
        # Replace with actual filtering code
        return all_pathways
    
    @staticmethod
    def generate_pathways(
            all_actions: list[Action],
            all_metrics: list[Metric],
            action_constraints: list[ActionFilter],
            metric_constraints: list[MetricFilter],
            max_sequence_length: int | None = None
    ) -> list[Pathway]:
        # Generate all pathways that don't violate the provided constraints
        # Estimate a value for each metric based on its Metric.estimate method
        return []
    
    @staticmethod
    def estimate_metric(
            pathway: Pathway,
            metric: Metric,
            all_actions: list[Action],
            all_pathways: list[Pathway]
    ) -> float:        
        # For manual estimate, just use the existing data (if there is any)
        if metric.estimate is MetricEstimate.MANUAL:
            current_data = pathway.metric_data.get(metric)
            if (current_data is None or current_data.is_estimate):
                return 0
            else:
                return current_data.value

        # Do the proper estimate respecting the Metric.estimate method
        return 0
