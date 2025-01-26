# pylint: disable=too-many-instance-attributes
"""
The single class that stores all data needed to work on a project
"""
from typing import Callable, Iterable

from adaptation_pathways.app.model.sorting import SortingInfo

from .action import Action
from .metric import Metric, MetricEffect, MetricOperation, MetricValue, MetricValueState
from .pathway import Pathway
from .scenario import Scenario


class PathwaysProject:
    def __init__(
        self,
        project_id: str,
        name: str,
        organization: str,
        start_year: int,
        end_year: int,
        conditions: list[Metric],
        criteria: list[Metric],
        scenarios: list[Scenario],
        actions: list[Action],
        pathways: list[Pathway],
        root_action: Action,
        root_pathway_id: str,
    ):
        self.id = project_id
        self.name = name
        self.organization = organization
        self.start_year = start_year
        self.end_year = end_year
        self._current_id = 0

        self.conditions_by_id: dict[str, Metric] = {}
        for metric in conditions:
            self.conditions_by_id[metric.id] = metric

        self.criteria_by_id: dict[str, Metric] = {}
        for metric in criteria:
            self.criteria_by_id[metric.id] = metric

        self.scenarios_by_id: dict[str, Scenario] = {}
        for scenario in scenarios:
            self.scenarios_by_id[scenario.id] = scenario

        self.actions_by_id: dict[str, Action] = {}
        self.actions_by_id[root_action.id] = root_action
        for action in actions:
            self.actions_by_id[action.id] = action

        self.pathways_by_id: dict[str, Pathway] = {}
        for pathway in pathways:
            self.pathways_by_id[pathway.id] = pathway

        self.condition_sorting = SortingInfo()
        self.criteria_sorting = SortingInfo()
        self.scenario_sorting = SortingInfo()
        self.action_sorting = SortingInfo()
        self.pathway_sorting = SortingInfo()

        self.root_pathway_id = root_pathway_id
        self.selected_condition_ids: set[str] = set()
        self.selected_criteria_ids: set[str] = set()
        self.selected_action_ids: set[str] = set()
        self.selected_pathway_ids: set[str] = set()
        self.selected_scenario_ids: set[str] = set()

        self.values_scenario_id: str | None = (
            None if len(scenarios) == 0 else scenarios[0].id
        )

        self.graph_metric_id: str | None = (
            conditions[0].id if len(conditions) > 0 else None
        )
        self.graph_is_time: bool = self.graph_metric_id is not None
        self.graph_scenario_id: str | None = (
            scenarios[0].id if len(scenarios) > 0 else None
        )

        self.on_conditions_changed: list[Callable[[], None]] = []
        self.on_criteria_changed: list[Callable[[], None]] = []
        self.on_scenarios_changed: list[Callable[[], None]] = []
        self.on_actions_changed: list[Callable[[], None]] = []
        self.on_action_color_changed: list[Callable[[], None]] = []
        self.on_pathways_changed: list[Callable[[], None]] = []

        for metric in self.all_metrics():
            self.update_pathway_values(metric.id)

    def __hash__(self):
        return self.id.__hash__()

    def notify_conditions_changed(self):
        for listener in self.on_conditions_changed:
            listener()

    def notify_criteria_changed(self):
        for listener in self.on_criteria_changed:
            listener()

    def notify_scenarios_changed(self):
        for listener in self.on_scenarios_changed:
            listener()

    def notify_actions_changed(self):
        for listener in self.on_actions_changed:
            listener()

    def notify_action_color_changed(self):
        for listener in self.on_action_color_changed:
            listener()

    def notify_pathways_changed(self):
        for listener in self.on_pathways_changed:
            listener()

    @property
    def all_actions(self):
        return self.actions_by_id.values()

    @property
    def all_conditions(self):
        return self.conditions_by_id.values()

    @property
    def all_criteria(self):
        return self.criteria_by_id.values()

    @property
    def all_scenarios(self):
        return self.scenarios_by_id.values()

    @property
    def all_pathways(self):
        return self.pathways_by_id.values()

    @property
    def root_pathway(self):
        return self.get_pathway(self.root_pathway_id)

    @property
    def values_scenario(self):
        return self.get_scenario(self.values_scenario_id)

    @property
    def graph_metric(self):
        return self.get_metric(self.graph_metric_id)

    @property
    def graph_scenario(self):
        return self.get_scenario(self.graph_scenario_id)

    def _create_id(self) -> str:
        self._current_id += 1
        return str(self._current_id)

    def get_metric(self, metric_id: str) -> Metric | None:
        metric = self.conditions_by_id.get(metric_id, None)
        if metric is None:
            metric = self.criteria_by_id.get(metric_id, None)
        return metric

    def all_metrics(self):
        yield from self.all_conditions
        yield from self.all_criteria

    def _create_metric(self, name: str, metrics_by_id: dict[str, Metric]) -> Metric:
        metric_id = self._create_id()
        metric = Metric(metric_id, name, "")
        metrics_by_id[metric_id] = metric

        for action in self.all_actions:
            action.metric_data[metric_id] = MetricEffect(0, MetricOperation.ADD)

        self.update_pathway_values(metric.id)
        return metric

    def create_condition(self) -> Metric:
        metric = self._create_metric("New Condition", self.conditions_by_id)
        return metric

    def create_criteria(self) -> Metric:
        metric = self._create_metric("New Criteria", self.criteria_by_id)
        return metric

    def delete_condition(self, metric_id: str) -> Metric | None:
        metric = self.conditions_by_id.pop(metric_id)
        self.selected_condition_ids.remove(metric_id)
        return metric

    def delete_criteria(self, metric_id: str) -> Metric | None:
        metric = self.criteria_by_id.pop(metric_id)
        self.selected_criteria_ids.remove(metric_id)
        return metric

    def get_scenario(self, scenario_id: str) -> Scenario | None:
        return self.scenarios_by_id.get(scenario_id, None)

    def create_scenario(self, name: str) -> Scenario:
        scenario_id = self._create_id()
        scenario = Scenario(scenario_id, name)
        self.scenarios_by_id[scenario.id] = scenario
        if self.graph_scenario_id is None:
            self.graph_scenario_id = scenario_id
        return scenario

    def copy_scenario(self, scenario_id: str, suffix=" (Copy)") -> Scenario | None:
        to_copy = self.get_scenario(scenario_id)
        if to_copy is None:
            return None

        new_scenario = self.create_scenario(f"{to_copy.name}{suffix}")
        for year_data in to_copy.yearly_data:
            new_data = new_scenario.get_or_add_year(year_data.year)
            for metric_id, metric_data in year_data.metric_data.items():
                new_data.metric_data[metric_id] = MetricValue(
                    metric_data.value, metric_data.state
                )

        return new_scenario

    def delete_scenario(self, scenario_id: str) -> Scenario | None:
        scenario = self.scenarios_by_id.pop(scenario_id)
        if self.graph_scenario_id is scenario_id:
            self.graph_scenario_id = next(self.all_scenarios, None)
        return scenario

    def delete_scenarios(self, scenario_ids: Iterable[str]):
        for scenario_id in scenario_ids:
            self.delete_scenario(scenario_id)

    def update_scenario_values(self, metric_id: str):
        for scenario in self.all_scenarios:
            scenario.recalculate_values(metric_id)

    def get_action(self, action_id: str) -> Action:
        return self.actions_by_id[action_id]

    def create_action(self, color, icon) -> Action:
        action_id = self._create_id()
        action = Action(
            action_id,
            "New Action",
            color,
            icon,
            {
                metric.id: MetricEffect(0, MetricOperation.ADD)
                for metric in self.all_metrics()
            },
        )

        self.actions_by_id[action.id] = action
        return action

    def delete_action(self, action_id: str) -> Action | None:
        action = self.actions_by_id.pop(action_id)
        return action

    def delete_actions(self, action_ids: Iterable[str]):
        pathway_ids_to_delete: list[str] = []

        for action_id in action_ids:
            self.delete_action(action_id)
            for pathway in self.all_pathways:
                if pathway.action_id == action_id:
                    pathway_ids_to_delete.append(pathway.id)

        self.delete_pathways(pathway_ids_to_delete)

    def get_pathway(self, pathway_id: str) -> Pathway | None:
        if pathway_id is None:
            return None
        return self.pathways_by_id.get(pathway_id, None)

    def create_pathway(
        self, action_id: str, parent_pathway_id: str | None = None
    ) -> Pathway:
        pathway = Pathway(action_id, parent_pathway_id)
        self.pathways_by_id[pathway.id] = pathway
        for metric in self.all_metrics():
            self.update_pathway_values(metric.id)

        return pathway

    def update_pathway_values(self, metric_id: str):
        metric = self.get_metric(metric_id)
        if metric is None:
            return

        updated_pathways: set[str] = set()
        for pathway in self.all_pathways:
            self._update_pathway_value(pathway, metric, updated_pathways)

    def _update_pathway_value(
        self, pathway: Pathway, metric: Metric, updated_pathway_ids: set[str]
    ):
        pathway_action = self.get_action(pathway.action_id)
        parent = (
            None if pathway.parent_id is None else self.get_pathway(pathway.parent_id)
        )
        current_value = pathway.metric_data.get(metric.id, None)

        # Initialize the value if there was none
        if current_value is None:
            current_value = MetricValue(
                0,
                (
                    MetricValueState.ESTIMATE
                    if parent is not None
                    else MetricValueState.BASE
                ),
            )
            pathway.metric_data[metric.id] = current_value

        # If we have a non-estimate value, we don't need to update anything
        if current_value.state != MetricValueState.ESTIMATE:
            updated_pathway_ids.add(pathway.id)
            return

        base_value: float = 0
        if parent is not None:
            parent_value = parent.metric_data.get(metric.id, None)

            if (
                parent.id not in updated_pathway_ids
                and parent_value is not None
                and parent_value.is_estimate
            ):
                self._update_pathway_value(parent, metric, updated_pathway_ids)

            if parent_value is not None:
                base_value = parent_value.value

        current_value.value = pathway_action.apply_effect(metric.id, base_value)
        updated_pathway_ids.add(pathway.id)

    def delete_pathway(self, pathway_id: str) -> Pathway | None:
        pathway = self.pathways_by_id.pop(pathway_id, None)
        return pathway

    def delete_pathways(self, pathway_ids: Iterable[str]):
        ids_to_delete: set[str] = set()
        ids_to_delete.update(pathway_ids)
        print(ids_to_delete)

        # Delete any orphaned children
        for pathway in self.all_pathways:
            if pathway.id in ids_to_delete:
                continue

            for ancestor in self.get_ancestors(pathway):
                if ancestor.id in ids_to_delete:
                    ids_to_delete.add(pathway.id)

        for pathway_id in ids_to_delete:
            print(pathway_id)
            self.delete_pathway(pathway_id)

    def delete_selected_pathways(self):
        self.delete_pathways(self.selected_pathway_ids)
        self.selected_pathway_ids.clear()

    def get_children(self, pathway_id: str):
        return (
            pathway for pathway in self.all_pathways if pathway.parent_id == pathway_id
        )

    def get_ancestors(self, pathway: Pathway):
        if pathway.parent_id is None:
            return

        current_pathway = self.get_pathway(pathway.parent_id)
        while current_pathway is not None:
            yield current_pathway
            if current_pathway.parent_id is None:
                return
            current_pathway = self.get_pathway(current_pathway.parent_id)

    def get_ancestors_and_self(self, pathway: Pathway):
        current_pathway: Pathway | None = pathway
        while current_pathway is not None:
            yield current_pathway
            if current_pathway.parent_id is not None:
                current_pathway = self.get_pathway(current_pathway.parent_id)
            else:
                current_pathway = None
