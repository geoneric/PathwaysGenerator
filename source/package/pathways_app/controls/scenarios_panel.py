import flet as ft
from pathways_app.controls.styled_button import StyledButton
from pathways_app.controls.styled_dropdown import StyledDropdown
from pathways_app.controls.styled_table import StyledTable

from adaptation_pathways.app.model import Metric
from adaptation_pathways.app.model.scenario import Scenario


class ScenariosPanel(ft.Column):
    def __init__(
        self,
        scenarios: list[Scenario],
        conditions: list[Metric],
        start_year: int,
        end_year: int,
    ):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            scroll=ft.ScrollMode.AUTO,
        )

        current_scenario = scenarios[0]
        year_range = range(start_year, end_year)

        self.controls = [
            ft.Row(
                expand=False,
                controls=[
                    StyledDropdown(
                        value=current_scenario.name,
                        options=[
                            ft.dropdown.Option(scenario.name) for scenario in scenarios
                        ],
                    ),
                    ft.Container(expand=True),
                    StyledButton("New", icon=ft.icons.ADD_CIRCLE_OUTLINE),
                ],
            ),
            StyledTable(
                columns=[
                    ft.DataColumn(label=ft.Text("Year")),
                    *(
                        ft.DataColumn(label=ft.Text(metric.name))
                        for metric in conditions
                    ),
                ],
                rows=[
                    ft.DataRow(
                        [
                            ft.DataCell(ft.Text(year)),
                            *(
                                ft.DataCell(
                                    ft.Text(
                                        current_scenario.get_data(year, metric)
                                        or "None"
                                    )
                                )
                                for metric in conditions
                            ),
                        ]
                    )
                    for year in year_range
                ],
            ),
        ]
