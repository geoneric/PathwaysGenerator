# from typing import Callable

import flet as ft

from adaptation_pathways.app.model.metric import Metric
from adaptation_pathways.app.model.pathways_project import PathwaysProject

from .. import theme
from .editable_cell import EditableTextCell
from .header import SmallHeader
from .panel_header import PanelHeader
from .styled_table import StyledTable, TableColumn, TableRow
from .unit_cell import MetricUnitCell


class MetricsEditor(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__()

        self.project = project
        self.header = PanelHeader("Metrics", theme.icons.metrics)
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        self.spacing = 40

        self.conditions_table = StyledTable(
            columns=[
                TableColumn(label="Name"),
                TableColumn(label="Unit"),
            ],
            rows=[],
            show_checkboxes=True,
            on_add=self.on_new_condition,
            on_delete=self.on_delete_conditions,
            pre_operation_content=ft.Row(
                [
                    SmallHeader("Conditions"),
                    ft.Container(expand=True),
                ],
                expand=True,
            ),
        )

        self.criteria_table = StyledTable(
            columns=[
                TableColumn(label="Name"),
                TableColumn(label="Unit"),
            ],
            rows=[],
            show_checkboxes=True,
            on_add=self.on_new_criteria,
            on_delete=self.on_delete_criteria,
            pre_operation_content=ft.Row(
                [
                    SmallHeader("Criteria"),
                    ft.Container(expand=True),
                ],
                expand=True,
            ),
        )

        self.update_metrics()

        self.controls = [
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.header,
                    self.conditions_table,
                ],
            ),
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.criteria_table,
                ],
            ),
        ]

    def redraw(self):
        self.update_metrics()
        self.update()

    def on_metric_updated(self, _):
        self.project.notify_conditions_changed()

    def on_condition_selected(self, metric: Metric):
        if metric.id in self.project.selected_condition_ids:
            self.project.selected_condition_ids.remove(metric.id)
        else:
            self.project.selected_condition_ids.add(metric.id)

        self.redraw()

    def on_criteria_selected(self, metric: Metric):
        if metric.id in self.project.selected_criteria_ids:
            self.project.selected_criteria_ids.remove(metric.id)
        else:
            self.project.selected_criteria_ids.add(metric.id)

        self.redraw()

    def on_new_condition(self):
        metric = self.project.create_condition()
        self.project.update_pathway_values(metric.id)
        self.project.notify_conditions_changed()

    def on_delete_conditions(self, rows: list[TableRow]):
        for row in rows:
            self.project.delete_condition(row.row_id)
        self.project.notify_conditions_changed()

    def on_new_criteria(self):
        metric = self.project.create_criteria()
        self.project.update_pathway_values(metric.id)
        self.project.notify_criteria_changed()

    def on_delete_criteria(self, rows: list[TableRow]):
        for row in rows:
            self.project.delete_criteria(row.row_id)
        self.project.notify_criteria_changed()

    def get_metric_row(
        self,
        metric: Metric,
        # selected_ids: set[str],
        # on_metric_selected: Callable[[Metric], None],
    ) -> TableRow:
        row = TableRow(
            row_id=metric.id,
            cells=[
                EditableTextCell(metric, "name", self.on_metric_updated),
                MetricUnitCell(metric, self.on_metric_updated),
            ],
        )
        return row

    def update_metrics(self):
        self.conditions_table.set_rows(
            self.get_metric_row(metric) for metric in self.project.all_conditions
        )

        self.criteria_table.set_rows(
            [
                self.get_metric_row(
                    metric,
                    # self.project.selected_criteria_ids,
                    # self.on_criteria_selected,
                )
                for metric in self.project.all_criteria
            ]
        )
