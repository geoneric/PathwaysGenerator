import flet as ft

from adaptation_pathways.app.model.action import Action
from adaptation_pathways.app.model.metric import Metric, MetricEstimate, MetricValue
from adaptation_pathways.app.model.pathway import Pathway
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.model.scenario import Scenario


metric_sea_level_rise = Metric(
    id="sea-level-rise",
    name="Sea Level Rise",
    unit_or_default="cm",
    current_value=10,
    estimate=MetricEstimate.MAXIMUM,
)

metric_cost = Metric(
    id="cost",
    name="Cost",
    unit_or_default="€",
    current_value=0,
    estimate=MetricEstimate.SUM,
)

metric_habitat_health = Metric(
    id="habitat",
    name="Habitat Health",
    unit_or_default="Impact",
    current_value=0,
    estimate=MetricEstimate.AVERAGE,
)

action_root = Action(
    id="current-situation",
    name="Current Situation",
    color="#999999",
    icon=ft.icons.HOME,
    metric_data={
        metric_sea_level_rise: MetricValue(0),
        metric_cost: MetricValue(0),
        metric_habitat_health: MetricValue(0),
    },
)

action_sea_wall = Action(
    id="sea-wall",
    name="Sea Wall",
    color="#5A81DB",
    icon=ft.icons.WATER,
    metric_data={
        metric_sea_level_rise: MetricValue(10),
        metric_cost: MetricValue(100000),
        metric_habitat_health: MetricValue(-2),
    },
)

action_pump = Action(
    id="pump",
    name="Pump",
    color="#44C1E1",
    icon=ft.icons.WATER_DROP_SHARP,
    metric_data={
        metric_sea_level_rise: MetricValue(5),
        metric_cost: MetricValue(50000),
        metric_habitat_health: MetricValue(-1),
    },
)

action_nature_based = Action(
    id="nature-based",
    name="Nature-Based",
    color="#E0C74B",
    icon=ft.icons.PARK,
    metric_data={
        metric_sea_level_rise: MetricValue(1),
        metric_cost: MetricValue(5000),
        metric_habitat_health: MetricValue(2),
    },
)

project = PathwaysProject(
    id="test-id",
    name="Sea Level Rise Adaptation",
    organization="Cork City Council",
    start_year=2024,
    end_year=2054,
    conditions=[metric_sea_level_rise],
    criteria=[metric_cost, metric_habitat_health],
    scenarios=[
        Scenario(
            id="scenario-1",
            name="Best Case",
            metric_data_over_time={
                2025: {metric_sea_level_rise: MetricValue(13)},
                2026: {metric_sea_level_rise: MetricValue(21)},
            },
        )
    ],
    actions=[action_pump, action_sea_wall, action_nature_based],
    root_pathway=Pathway(
        id=action_root.id,
        last_action=action_root,
        metric_data=action_root.metric_data,
        children=[
            Pathway(
                id=f"{action_root.id}->{action_pump.id}",
                last_action=action_pump,
                metric_data=action_pump.metric_data,
            ),
            Pathway(
                id=f"{action_root.id}->{action_sea_wall.id}",
                last_action=action_sea_wall,
                metric_data=action_sea_wall.metric_data,
            ),
            Pathway(
                id=f"{action_root.id}->{action_nature_based.id}",
                last_action=action_nature_based,
                metric_data=action_nature_based.metric_data,
            ),
        ],
    ),
)
