import locale
import logging

import flet as ft
import theme
from controls.header import SectionHeader
from controls.menu_bar import MenuBar
from controls.metrics_panel import MetricsPanel
from controls.panel import Panel
from controls.tabbed_panel import TabbedPanel
from pathways_app import example
from pathways_app.controls.actions_panel import ActionsPanel
from pathways_app.controls.graph_panel import GraphPanel
from pathways_app.controls.pathways_panel import PathwaysPanel
from pathways_app.controls.scenarios_panel import ScenariosPanel


locale.setlocale(locale.LC_ALL, "")


def main(page: ft.Page):
    page.theme = theme.theme

    # bitdojo_window could make a custom title bar
    # page.window.frameless = True

    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True

    page.title = "Pathways Generator"
    page.fonts = theme.fonts
    page.bgcolor = theme.colors.primary_darker
    page.padding = 1
    page.spacing = 0

    project = example.project

    page.appbar = MenuBar(project)
    metrics_tab = (
        SectionHeader(ft.icons.TUNE, "Metrics"),
        MetricsPanel(project.conditions, project.criteria),
    )

    actions_tab = (
        SectionHeader(ft.icons.CONSTRUCTION_OUTLINED, "Actions"),
        ActionsPanel(project.actions, [*project.conditions, *project.criteria]),
    )

    scenarios_tab = (
        SectionHeader(ft.icons.PUBLIC, "Scenarios"),
        ScenariosPanel(
            project.scenarios, project.conditions, project.start_year, project.end_year
        ),
    )

    page.add(
        ft.Container(
            expand=True,
            padding=theme.variables.panel_spacing,
            content=ft.Row(
                expand=True,
                spacing=theme.variables.panel_spacing,
                controls=[
                    ft.Column(
                        expand=2,
                        spacing=theme.variables.panel_spacing,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            TabbedPanel(
                                selected_index=0,
                                tabs=[metrics_tab, actions_tab, scenarios_tab],
                            )
                        ],
                    ),
                    ft.Column(
                        expand=3,
                        spacing=theme.variables.panel_spacing,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            Panel(GraphPanel(project.conditions)),
                            Panel(
                                content=ft.Column(
                                    expand=False,
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=15,
                                    controls=[
                                        SectionHeader(
                                            ft.icons.ACCOUNT_TREE_OUTLINED, "Pathways"
                                        ),
                                        PathwaysPanel(
                                            root=project.root_pathway,
                                            metrics=project.conditions
                                            + project.criteria,
                                            actions=project.actions,
                                        ),
                                    ],
                                ),
                                padding=theme.variables.panel_padding,
                            ),
                        ],
                    ),
                ],
            ),
            bgcolor=theme.colors.primary_lighter,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )
    )


logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets")

print("Pathways App Started")
