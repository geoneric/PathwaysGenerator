import flet as ft
from pathways_app import theme
from pathways_app.controls.styled_button import StyledButton
from pathways_app.controls.styled_dropdown import StyledDropdown

from adaptation_pathways.app.model.metric import Metric


class GraphPanel(ft.Row):
    def __init__(self, conditions: list[Metric]):
        super().__init__(expand=False, spacing=0)
        self.controls = [
            ft.Container(
                expand=False,
                padding=theme.variables.panel_padding,
                content=ft.Column(
                    expand=False,
                    width=200,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        StyledDropdown(
                            "Metro Map",
                            options=[
                                ft.dropdown.Option("Metro Map"),
                                ft.dropdown.Option("Bar Chart"),
                            ],
                            option_icons=[ft.icons.ROUTE_OUTLINED, ft.icons.BAR_CHART],
                            height=36,
                            text_style=theme.text.dropdown_large,
                        ),
                        ft.Container(expand=True),
                        ft.Row(
                            [
                                StyledButton("Export", icon=ft.icons.SAVE_SHARP),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor=theme.colors.true_white,
                border_radius=ft.border_radius.only(
                    top_right=theme.variables.small_radius,
                    bottom_right=theme.variables.small_radius,
                ),
                padding=ft.padding.only(bottom=10),
                content=ft.Column(
                    [
                        ft.Container(expand=True, bgcolor=theme.colors.off_white),
                        StyledDropdown(
                            value="Time",
                            options=[
                                ft.dropdown.Option("Time"),
                                *(
                                    ft.dropdown.Option(metric.name)
                                    for metric in conditions
                                ),
                            ],
                            width=200,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ]
