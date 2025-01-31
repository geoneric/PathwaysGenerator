import traceback
from typing import Callable

import flet as ft
import matplotlib.pyplot
from flet.matplotlib_chart import MatplotlibChart
from src import theme
from src.pathways_app import PathwaysApp

from adaptation_pathways.app.service.plotting_service import PlottingService

from ..header import SmallHeader
from ..styled_button import StyledButton
from ..styled_dropdown import StyledDropdown


class GraphHeader(ft.Row):
    def __init__(
        self,
        on_expand: Callable[[], None] | None = None,
        on_sidebar: Callable[[], None] | None = None,
    ):
        self.on_expand = on_expand
        self.on_sidebar = on_sidebar

        self.expand_icon = ft.Icon(
            ft.Icons.OPEN_IN_FULL,
            color=theme.colors.primary_dark,
            size=theme.variables.icon_button_size,
        )
        self.sidebar_icon = ft.Icon(
            ft.Icons.VIEW_SIDEBAR,
            color=theme.colors.primary_dark,
            size=theme.variables.icon_button_size,
        )

        super().__init__(
            expand=False,
            controls=[
                ft.Container(self.sidebar_icon, on_click=self.on_sidebar_clicked),
                ft.Container(expand=True),
                ft.Container(self.expand_icon, on_click=self.on_expand_clicked),
            ],
        )
        self.set_sidebar_open(True)
        self.set_expanded(False)

    def set_expanded(self, expanded: bool):
        self.expand_icon.name = (
            theme.icons.minimize if expanded else theme.icons.maximize
        )

    def on_expand_clicked(self, _):
        if self.on_expand is None:
            return
        self.on_expand()

    def set_sidebar_open(self, is_open: bool):
        self.sidebar_icon.name = (
            theme.icons.sidebar_open if is_open else theme.icons.sidebar_closed
        )

    def on_sidebar_clicked(self, _):
        if self.on_sidebar is None:
            return
        self.on_sidebar()


class GraphEditor(ft.Row):
    def __init__(self, app: PathwaysApp):
        super().__init__(expand=False, spacing=0)

        self.app = app

        self.header = GraphHeader(on_sidebar=self.on_sidebar_toggle)

        self.graph_container = ft.Container(
            expand=True, bgcolor=theme.colors.true_white
        )

        self.metric_dropdown = StyledDropdown(
            value="none",
            options=[],
            width=200,
            on_change=self.on_graph_metric_changed,
        )

        self.graph_options = ft.Column([], expand=False, spacing=3)
        self.time_metric_option = StyledDropdown(
            self.app.project.graph_metric_id or "none",
            options=[],
            on_change=self.on_time_metric_changed,
        )

        self.graph_scenario_option = StyledDropdown(
            self.app.project.graph_scenario_id or "none",
            options=[],
            on_change=self.on_graph_scenario_changed,
        )

        self.update_parameters()

        self.sidebar = ft.Container(
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
                        option_icons=[ft.Icons.ROUTE_OUTLINED, ft.Icons.BAR_CHART],
                        height=36,
                        text_style=theme.text.dropdown_large,
                    ),
                    self.graph_options,
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            StyledButton("Export", icon=ft.Icons.SAVE_SHARP),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
            ),
        )

        self.controls = [
            self.sidebar,
            ft.Container(
                expand=True,
                bgcolor=theme.colors.true_white,
                border_radius=ft.border_radius.only(
                    top_right=theme.variables.small_radius,
                    bottom_right=theme.variables.small_radius,
                ),
                padding=ft.padding.only(bottom=10),
                content=ft.Stack(
                    expand=True,
                    controls=[
                        ft.Column(
                            [
                                ft.Container(height=10),
                                self.graph_container,
                                self.metric_dropdown,
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.END,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            content=self.header,
                            padding=theme.variables.panel_padding,
                            alignment=ft.alignment.top_center,
                            height=36,
                        ),
                    ],
                    alignment=ft.alignment.top_center,
                ),
            ),
        ]

        self.update_graph()

    def on_sidebar_toggle(self):
        self.sidebar.visible = not self.sidebar.visible
        self.header.set_sidebar_open(self.sidebar.visible)
        self.update()

    def on_graph_metric_changed(self, _):
        self.app.project.graph_is_time = self.metric_dropdown.value == "time"
        if not self.app.project.graph_is_time:
            self.app.project.graph_metric_id = self.metric_dropdown.value
        self.redraw()

    def on_time_metric_changed(self, _):
        self.app.project.graph_metric_id = self.time_metric_option.value
        self.redraw()

    def on_graph_scenario_changed(self, _):
        self.app.project.graph_scenario_id = self.graph_scenario_option.value
        self.redraw()

    def redraw(self):
        self.update_parameters()
        self.update_graph()
        self.update()

    def update_parameters(self):
        if self.app.project.graph_is_time:
            self.time_metric_option.set_options(
                [
                    ft.dropdown.Option(
                        key="none", text="- Select a Condition -", disabled=True
                    ),
                    *(
                        ft.dropdown.Option(
                            key=metric.id,
                            text=f"{metric.name} ({metric.unit.symbol})",
                        )
                        for metric in self.app.project.all_conditions
                    ),
                ]
            )

            self.graph_scenario_option.set_options(
                [
                    ft.dropdown.Option(
                        key="none", text="- Select a Scenario -", disabled=True
                    ),
                    *(
                        ft.dropdown.Option(
                            key=scenario.id,
                            text=f"{scenario.name}",
                        )
                        for scenario in self.app.project.all_scenarios
                    ),
                ]
            )

            self.graph_options.controls = [
                ft.Container(height=0),
                SmallHeader("Condition"),
                self.time_metric_option,
                ft.Container(height=15),
                SmallHeader("Scenario"),
                self.graph_scenario_option,
            ]
        else:
            self.graph_options.controls = []

        self.metric_dropdown.value = (
            "time"
            if self.app.project.graph_is_time
            else self.app.project.graph_metric_id or "none"
        )
        self.metric_dropdown.set_options(
            [
                ft.dropdown.Option(
                    key="none",
                    text="- Choose X-Axis -",
                    disabled=True,
                ),
                ft.dropdown.Option(
                    key="time",
                    text="Time",
                    disabled=len(self.app.project.scenarios_by_id) == 0,
                ),
                *(
                    ft.dropdown.Option(
                        key=metric.id, text=f"{metric.name} ({metric.unit.symbol})"
                    )
                    for metric in self.app.project.all_conditions
                ),
            ]
        )

    def update_graph(self):
        if self.app.project.graph_metric is None:
            self.graph_container.visible = False
            return

        try:
            figure, _ = PlottingService.draw_metro_map(self.app.project)
            self.graph_container.visible = True
            self.graph_container.content = MatplotlibChart(figure)
            matplotlib.pyplot.close(figure)
        except Exception:
            print("Error when attempting to draw graph")
            print(traceback.format_exc())
            self.graph_container.visible = False
