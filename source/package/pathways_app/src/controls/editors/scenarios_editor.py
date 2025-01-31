import datetime
from functools import partial

import flet as ft
from src.pathways_app import PathwaysApp
from src.utils import find_index

from adaptation_pathways.app.model.metric import Metric
from adaptation_pathways.app.model.scenario import YearDataPoint

from ..editable_cell import EditableIntCell, EditableTextCell
from ..header import SmallHeader
from ..metric_value import MetricValueCell
from ..styled_dropdown import StyledDropdown
from ..styled_table import StyledTable, TableColumn, TableRow


class ScenariosEditor(ft.Column):
    def __init__(self, app: PathwaysApp):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        self.app = app

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
            value=self.app.project.values_scenario_id or "none",
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
                    for scenario in self.app.project.all_scenarios
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
                for scenario in self.app.project.all_scenarios
            ]
        )

    def on_add_scenario(self):
        self.app.project.create_scenario("New Scenario")
        self.app.notify_scenarios_changed()

    def on_copy_scenarios(self, rows: list[TableRow]):
        for row in rows:
            self.app.project.copy_scenario(row.row_id)

        self.app.notify_scenarios_changed()

    def on_scenario_name_edited(self):
        self.app.notify_scenarios_changed()

    def on_delete_scenarios(self, rows: list[TableRow]):
        self.app.project.delete_scenarios(row.row_id for row in rows)
        self.app.notify_scenarios_changed()

    def update_values_table(self):
        self.update_values_headers()
        self.update_values_rows()

    def update_values_headers(self):
        self.scenario_values_table.set_columns(
            [
                TableColumn(label="Year", sortable=False),
                *(
                    TableColumn(label=metric.name, sortable=False)
                    for metric in self.app.project.all_conditions
                ),
            ]
        )

    def update_values_rows(self):
        if self.app.project.values_scenario is None:
            self.scenario_values_table.set_rows([])
            return

        self.scenario_values_table.set_rows(
            [
                self._get_year_row(point)
                for point in self.app.project.values_scenario.yearly_data
            ]
        )

    def _get_year_row(self, point: YearDataPoint):
        return TableRow(
            row_id=str(point.year),
            cells=[
                EditableIntCell(point, "year", self.on_year_edited),
                *(
                    self._get_metric_cell(metric, point)
                    for metric in self.app.project.all_conditions
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
        for metric in self.app.project.all_conditions:
            self.app.project.values_scenario.recalculate_values(metric.id)

        self.app.project.values_scenario.sort_yearly_data()
        self.app.notify_scenarios_changed()

    def on_metric_value_edited(self, cell: MetricValueCell):
        self.app.project.values_scenario.recalculate_values(cell.metric.id)
        self.app.notify_scenarios_changed()

    def on_scenario_changed(self, _):
        self.app.project.values_scenario_id = (
            self.scenario_dropdown.value
            if self.scenario_dropdown.value in self.app.project.scenarios_by_id
            else None
        )
        self.redraw()

    def on_add_year(self):
        if self.app.project.values_scenario is None:
            return

        scenario = self.app.project.values_scenario

        year = datetime.datetime.now().year
        year_count = len(scenario.yearly_data)

        if year_count > 0:
            year = scenario.yearly_data[year_count - 1].year + 1

        scenario.get_or_add_year(year)
        for metric in self.app.project.all_conditions:
            scenario.recalculate_values(metric.id)

        self.app.notify_scenarios_changed()

    def on_delete_years(self, rows: list[TableRow]):
        def is_year(data: YearDataPoint, year: int):
            return data.year == year

        for row in rows:
            row_year = int(row.row_id)

            data_index = find_index(
                self.app.project.values_scenario.yearly_data,
                partial(is_year, year=row_year),
            )
            if data_index is None:
                continue
            self.app.project.values_scenario.yearly_data.pop(data_index)

        self.app.notify_scenarios_changed()

    def redraw(self):
        self.update_scenario_table()
        self.update_dropdown()
        self.update_values_table()
        self.update()
