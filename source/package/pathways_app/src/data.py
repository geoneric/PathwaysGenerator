import datetime
from uuid import uuid4

import flet as ft

from adaptation_pathways.app.model.metric import (
    MetricEffect,
    MetricValue,
    MetricValueState,
)
from adaptation_pathways.app.model.pathways_project import PathwaysProject


def create_empty_project(name: str, project_id: str | None = None) -> PathwaysProject:
    start_year = datetime.datetime.now().year

    project = PathwaysProject(
        project_id=project_id or str(uuid4()),
        name=name,
        organization="",
        start_year=start_year,
        end_year=start_year + 100,
    )

    root_action = project.create_action("#999999", ft.Icons.HOME, name="Current")
    project.root_action_id = root_action.id

    root_pathway = project.create_pathway(root_action.id)
    project.root_pathway_id = root_pathway.id

    return project


def create_example_project() -> PathwaysProject:
    project = PathwaysProject(
        project_id="test-id",
        name="Sea Level Rise Adaptation",
        organization="Cork City Council",
        start_year=2024,
        end_year=2054,
        graph_is_time=False,
    )

    metric_sea_level_rise = project.create_condition()
    metric_sea_level_rise.name = "Sea Level Rise"
    metric_sea_level_rise.unit_or_default = "cm"

    metric_cost = project.create_criteria()
    metric_cost.name = "Cost"
    metric_cost.unit_or_default = "€"

    metric_habitat_health = project.create_criteria()
    metric_habitat_health.name = "Habitat Health"
    metric_habitat_health.unit_or_default = "Impact"

    action_root = project.create_action("#999999", ft.Icons.HOME)
    action_root.name = "Current"
    action_root.metric_data = {
        metric_sea_level_rise.id: MetricEffect(0),
        metric_cost.id: MetricEffect(0),
        metric_habitat_health.id: MetricEffect(0),
    }
    project.root_action_id = action_root.id

    action_sea_wall = project.create_action("#5A81DB", ft.Icons.WATER)
    action_sea_wall.name = "Sea Wall"
    action_sea_wall.metric_data = {
        metric_sea_level_rise.id: MetricEffect(10),
        metric_cost.id: MetricEffect(100000),
        metric_habitat_health.id: MetricEffect(-2),
    }

    action_pump = project.create_action("#44C1E1", ft.Icons.WATER_DROP_SHARP)
    action_pump.name = "Pump"
    action_pump.metric_data = {
        metric_sea_level_rise.id: MetricEffect(5),
        metric_cost.id: MetricEffect(50000),
        metric_habitat_health.id: MetricEffect(-1),
    }

    action_nature_based = project.create_action("#E0C74B", ft.Icons.PARK)
    action_nature_based.name = "Nature-Based"
    action_nature_based.metric_data = {
        metric_sea_level_rise.id: MetricEffect(1),
        metric_cost.id: MetricEffect(5000),
        metric_habitat_health.id: MetricEffect(2),
    }

    root_pathway = project.create_pathway(action_root.id, None)
    root_pathway.metric_data[metric_sea_level_rise.id] = MetricValue(0)
    root_pathway.metric_data[metric_cost.id] = MetricValue(0)
    root_pathway.metric_data[metric_habitat_health.id] = MetricValue(0)
    project.root_pathway_id = root_pathway.id

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
    return project
