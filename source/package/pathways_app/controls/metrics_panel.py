import flet as ft
from pathways_app.controls.header import SmallHeader
from pathways_app.controls.styled_button import StyledButton
from pathways_app.controls.styled_table import StyledTable

from adaptation_pathways.app.model import Metric


class MetricsPanel(ft.Column):
    def __init__(self, conditions: list[Metric], criteria: list[Metric]):
        super().__init__()

        self.expand = False
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        self.spacing = 40

        self.controls = [
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=False,
                        controls=[
                            SmallHeader("Conditions"),
                            ft.Container(expand=True),
                            StyledButton("New", icon=ft.icons.ADD_CIRCLE_OUTLINE),
                        ],
                    ),
                    StyledTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("Name")),
                            ft.DataColumn(label=ft.Text("Unit")),
                            ft.DataColumn(label=ft.Text("Estimate")),
                        ],
                        rows=[
                            ft.DataRow(
                                [
                                    ft.DataCell(ft.Text(metric.name)),
                                    ft.DataCell(ft.Text(metric.unit.display_name)),
                                    ft.DataCell(ft.Text(repr(metric.estimate))),
                                ]
                            )
                            for metric in conditions
                        ],
                    ),
                ],
            ),
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=False,
                        controls=[
                            SmallHeader("Criteria"),
                            ft.Container(expand=True),
                            StyledButton(text="New", icon=ft.icons.ADD_CIRCLE_OUTLINE),
                        ],
                    ),
                    StyledTable(
                        columns=[
                            ft.DataColumn(label=ft.Text("Name", expand=True)),
                            ft.DataColumn(label=ft.Text("Unit", expand=True)),
                            ft.DataColumn(label=ft.Text("Estimate", expand=True)),
                        ],
                        rows=[
                            ft.DataRow(
                                [
                                    ft.DataCell(ft.Text(metric.name)),
                                    ft.DataCell(ft.Text(metric.unit.display_name)),
                                    ft.DataCell(ft.Text(repr(metric.estimate))),
                                ]
                            )
                            for metric in criteria
                        ],
                    ),
                ],
            ),
        ]
