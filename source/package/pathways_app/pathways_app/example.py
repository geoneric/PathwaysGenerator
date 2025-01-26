import flet as ft

from adaptation_pathways.app.model.action import Action, MetricEffect
from adaptation_pathways.app.model.metric import Metric, MetricValue, MetricValueState
from adaptation_pathways.app.model.pathway import Pathway
from adaptation_pathways.app.model.pathways_project import PathwaysProject


metric_sea_level_rise = Metric(
    "sea-level-rise",
    name="Sea Level Rise",
    unit_or_default="cm",
)

metric_cost = Metric(
    "cost",
    name="Cost",
    unit_or_default="€",
)

metric_habitat_health = Metric(
    "habitat",
    name="Habitat Health",
    unit_or_default="Impact",
)

action_root = Action(
    "current-situation",
    name="Current",
    color="#999999",
    icon=ft.Icons.HOME,
    metric_data={
        metric_sea_level_rise.id: MetricEffect(0),
        metric_cost.id: MetricEffect(0),
        metric_habitat_health.id: MetricEffect(0),
    },
)

action_sea_wall = Action(
    "sea-wall",
    name="Sea Wall",
    color="#5A81DB",
    icon=ft.Icons.WATER,
    metric_data={
        metric_sea_level_rise.id: MetricEffect(10),
        metric_cost.id: MetricEffect(100000),
        metric_habitat_health.id: MetricEffect(-2),
    },
)

action_pump = Action(
    "pump",
    name="Pump",
    color="#44C1E1",
    icon=ft.Icons.WATER_DROP_SHARP,
    metric_data={
        metric_sea_level_rise.id: MetricEffect(5),
        metric_cost.id: MetricEffect(50000),
        metric_habitat_health.id: MetricEffect(-1),
    },
)

action_nature_based = Action(
    id="nature-based",
    name="Nature-Based",
    color="#E0C74B",
    icon=ft.Icons.PARK,
    metric_data={
        metric_sea_level_rise.id: MetricEffect(1),
        metric_cost.id: MetricEffect(5000),
        metric_habitat_health.id: MetricEffect(2),
    },
)

root_pathway = Pathway(action_root.id)
root_pathway.metric_data[metric_sea_level_rise.id] = MetricValue(0)
root_pathway.metric_data[metric_cost.id] = MetricValue(0)
root_pathway.metric_data[metric_habitat_health.id] = MetricValue(0)

project = PathwaysProject(
    project_id="test-id",
    name="Sea Level Rise Adaptation",
    organization="Cork City Council",
    start_year=2024,
    end_year=2054,
    conditions=[metric_sea_level_rise],
    criteria=[metric_cost],
    scenarios=[],
    actions=[action_pump, action_sea_wall, action_nature_based],
    pathways=[root_pathway],
    root_action=action_root,
    root_pathway_id=root_pathway.id,
)

project.create_pathway(action_pump.id, root_pathway.id)
project.create_pathway(action_sea_wall.id, root_pathway.id)
project.create_pathway(action_nature_based.id, root_pathway.id)

best_case_scenario = project.create_scenario("Best Case")
best_case_scenario.set_data(
    2025, metric_sea_level_rise.id, MetricValue(0, MetricValueState.OVERRIDE)
)
best_case_scenario.set_data(
    2050, metric_sea_level_rise.id, MetricValue(10, MetricValueState.OVERRIDE)
)
project.values_scenario_id = best_case_scenario.id
