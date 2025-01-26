import datetime
from functools import partial

import flet as ft
from controls.styled_dropdown import StyledDropdown
from controls.styled_table import StyledTable, TableColumn, TableRow
from pathways_app import theme
from pathways_app.controls.editable_cell import EditableIntCell, EditableTextCell
from pathways_app.controls.header import SmallHeader
from pathways_app.controls.metric_value import MetricValueCell
from pathways_app.controls.panel_header import PanelHeader
from pathways_app.utils import find_index

from adaptation_pathways.app.model.metric import Metric
from adaptation_pathways.app.model.pathways_project import PathwaysProject
from adaptation_pathways.app.model.scenario import YearDataPoint


class ScenariosEditor(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self.project = project

        self.header = PanelHeader("Scenarios", theme.icons.scenarios)

        self.scenario_table = StyledTable(
            columns=[TableColumn("Name", key="name")],
            rows=[],
            expand=1,
            on_add=self.on_add_scenario,
            on_delete=self.on_delete_scenarios,
            on_copy=self.on_copy_scenarios,
        )
        self.update_scenario_table()

        self.no_scenario_option = ft.dropdown.Option(
            key="none", text="- Choose a Scenario -", disabled=True
        )
        self.scenario_dropdown = StyledDropdown(
            value=(
                "none"
                if self.project.values_scenario_id is None
                else self.project.values_scenario_id
            ),
            options=[],
            on_change=self.on_scenario_changed,
        )

        self.scenario_values_table = StyledTable(
            columns=[],
            rows=[],
            expand=3,
            on_add=self.on_add_year,
            add_label="Add Year",
            on_delete=self.on_delete_years,
            pre_operation_content=ft.Row(
                [self.scenario_dropdown, ft.Container(expand=True)], expand=True
            ),
        )

        self.controls = [
            self.header,
            self.scenario_table,
            ft.Container(height=20),
            SmallHeader("Scenario Data"),
            self.scenario_values_table,
        ]

        self.update_dropdown()
        self.update_values_table()

    def update_dropdown(self):
        self.scenario_dropdown.set_options(
            [
                self.no_scenario_option,
                *(
                    ft.dropdown.Option(key=scenario.id, text=scenario.name)
                    for scenario in self.project.all_scenarios
                ),
            ]
        )

    def update_scenario_table(self):
        self.scenario_table.set_rows(
            [
                TableRow(
                    scenario.id,
                    [EditableTextCell(scenario, "name", self.on_scenario_name_edited)],
                )
                for scenario in self.project.all_scenarios
            ]
        )

    def on_add_scenario(self):
        self.project.create_scenario("New Scenario")
        self.project.notify_scenarios_changed()

    def on_copy_scenarios(self, rows: list[TableRow]):
        for row in rows:
            self.project.copy_scenario(row.row_id)

        self.project.notify_scenarios_changed()

    def on_scenario_name_edited(self):
        self.project.notify_scenarios_changed()

    def on_delete_scenarios(self, rows: list[TableRow]):
        self.project.delete_scenarios(row.row_id for row in rows)
        self.project.notify_scenarios_changed()

    def update_values_table(self):
        self.update_values_headers()
        self.update_values_rows()

    def update_values_headers(self):
        self.scenario_values_table.set_columns(
            [
                TableColumn(label="Year", sortable=False),
                *(
                    TableColumn(label=metric.name, sortable=False)
                    for metric in self.project.all_conditions
                ),
            ]
        )

    def update_values_rows(self):
        if self.project.values_scenario is None:
            self.scenario_values_table.set_rows([])
            return

        self.scenario_values_table.set_rows(
            [
                self._get_year_row(point)
                for point in self.project.values_scenario.yearly_data
            ]
        )

    def _get_year_row(self, point: YearDataPoint):
        return TableRow(
            row_id=point.year,
            cells=[
                EditableIntCell(point, "year", self.on_year_edited),
                *(
                    self._get_metric_cell(metric, point)
                    for metric in self.project.all_conditions
                ),
            ],
        )

    def _get_metric_cell(self, metric: Metric, point: YearDataPoint):
        return MetricValueCell(
            metric,
            point.get_or_add_data(metric.id),
            on_finished_editing=self.on_metric_value_edited,
        )

    def on_year_edited(self, _):
        for metric in self.project.all_conditions:
            self.project.values_scenario.recalculate_values(metric.id)

        self.project.values_scenario.sort_yearly_data()
        self.project.notify_scenarios_changed()

    def on_metric_value_edited(self, cell: MetricValueCell):
        self.project.values_scenario.recalculate_values(cell.metric.id)
        self.project.notify_scenarios_changed()

    def on_scenario_changed(self, _):
        self.project.values_scenario_id = (
            self.scenario_dropdown.value
            if self.scenario_dropdown.value in self.project.scenarios_by_id
            else None
        )
        self.redraw()

    def on_add_year(self):
        if self.project.values_scenario is None:
            return

        scenario = self.project.values_scenario

        year = datetime.datetime.now().year
        year_count = len(scenario.yearly_data)

        if year_count > 0:
            year = scenario.yearly_data[year_count - 1].year + 1

        scenario.get_or_add_year(year)
        for metric in self.project.all_conditions:
            scenario.recalculate_values(metric.id)

        self.project.notify_scenarios_changed()

    def on_delete_years(self, rows: list[TableRow]):
        def is_year(data: YearDataPoint, year: int):
            return data.year == year

        for row in rows:
            row_year = int(row.row_id)

            data_index = find_index(
                self.project.values_scenario.yearly_data,
                partial(is_year, year=row_year),
            )
            if data_index is None:
                continue
            self.project.values_scenario.yearly_data.pop(data_index)

        self.project.notify_scenarios_changed()

    def redraw(self):
        self.update_scenario_table()
        self.update_dropdown()
        self.update_values_table()
        self.update()
