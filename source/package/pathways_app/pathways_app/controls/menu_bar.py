import flet as ft

from .. import theme
from ..config import Config
from ..pathways_app import PathwaysApp


class MenuBar(ft.Container):
    def __init__(self, app: PathwaysApp):
        self.app = app

        super().__init__(
            content=ft.Stack(
                [
                    ft.Row(
                        [
                            ft.Image(theme.icon, height=36, width=36),
                            ft.Text("PATHWAYS\nGENERATOR", style=theme.text.logo),
                            ft.Container(width=15),
                            ft.SubmenuButton(
                                ft.Text("Project", style=theme.text.menu_button),
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text("New"),
                                        on_click=self.on_new_project,
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text("Open..."),
                                        on_click=self.on_open_project,
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text("Save As..."),
                                        on_click=self.on_save_project,
                                    ),
                                ],
                                # style=theme.buttons.menu_bar_button,
                            ),
                            ft.SubmenuButton(
                                ft.Text("Help", style=theme.text.menu_button),
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text("About Pathways"),
                                        on_click=lambda e: app.open_link(
                                            Config.about_url
                                        ),
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text("GitHub Repository"),
                                        on_click=lambda e: app.open_link(
                                            Config.github_url
                                        ),
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "version 1.0.0",
                                            color=theme.colors.primary_light,
                                        ),
                                        padding=ft.padding.symmetric(5, 10),
                                    ),
                                ],
                                # style=theme.buttons.menu_bar_button,
                                menu_style=theme.buttons.submenu,
                            ),
                        ],
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                bgcolor=theme.colors.primary_medium,
                                border_radius=theme.variables.small_radius,
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(0, 15),
                                width=300,
                                content=ft.Stack(
                                    [
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    app.project.name,
                                                    color=theme.colors.true_white,
                                                ),
                                                ft.Text(
                                                    app.project.organization,
                                                    text_align=ft.TextAlign.CENTER,
                                                    color=theme.colors.true_white,
                                                ),
                                            ],
                                            spacing=0,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        )
                                    ]
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            ),
            height=50,
            padding=ft.padding.symmetric(4, 5),
            margin=0,
            bgcolor=theme.colors.primary_dark,
            border_radius=ft.border_radius.only(top_left=0, top_right=0),
            border=ft.border.only(
                bottom=ft.border.BorderSide(1, theme.colors.primary_darker)
            ),
        )

    def on_new_project(self):
        pass

    def on_open_project(self, _):
        self.app.open_project()

    def on_save_project(self):
        pass
