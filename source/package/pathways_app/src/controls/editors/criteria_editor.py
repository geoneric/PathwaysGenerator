# from typing import Callable

import flet as ft
from src.pathways_app import PathwaysApp

from adaptation_pathways.app.model.metric import Metric

from ..editable_cell import EditableTextCell
from ..styled_table import StyledTable, TableColumn, TableRow
from ..unit_cell import MetricUnitCell


class CriteriaEditor(ft.Column):
    def __init__(
        self, app: PathwaysApp, pre_operation_content: ft.Control | None = None
    ):
        super().__init__()

        self.app = app
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.criteria_table = StyledTable(
            columns=[
                TableColumn(label="Name"),
                TableColumn(label="Unit"),
            ],
            rows=[],
            pre_operation_content=pre_operation_content,
            on_add=self.on_new_criteria,
            on_delete=self.on_delete_criteria,
        )

        self.update_metrics()

        self.controls = [
            self.criteria_table,
        ]

    def redraw(self):
        self.update_metrics()
        self.update()

    def on_metric_updated(self, _):
        self.app.notify_conditions_changed()

    def on_new_criteria(self):
        metric = self.app.project.create_criteria()
        self.app.project.update_pathway_values(metric.id)
        self.app.notify_criteria_changed()

    def on_delete_criteria(self, rows: list[TableRow]):
        for row in rows:
            self.app.project.delete_criteria(row.row_id)
        self.app.notify_criteria_changed()

    def get_metric_row(
        self,
        metric: Metric,
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
        self.criteria_table.set_rows(
            [
                self.get_metric_row(
                    metric,
                )
                for metric in self.app.project.all_criteria
            ]
        )
