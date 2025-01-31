import flet as ft
from src import theme
from src.pathways_app import PathwaysApp

from ..styled_button import StyledButton


class StartupPage(ft.Row):
    def __init__(self, app: PathwaysApp):
        self.app = app

        super().__init__(
            expand=False,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.panel = ft.Container(
            ft.Column(
                [
                    ft.Text(
                        "Welcome to the Pathways Generator!",
                        text_align=ft.TextAlign.CENTER,
                        size=48,
                        expand=True,
                    ),
                    ft.Text(
                        "Use this tool to generate and analyze pathways.",
                        text_align=ft.TextAlign.CENTER,
                        size=18,
                        expand=True,
                    ),
                    ft.Row(
                        [
                            StyledButton(
                                "Start a New Project",
                                ft.Icons.NOTE_ADD_OUTLINED,
                                size=20,
                                on_click=self.on_new_project,
                            ),
                            ft.Column(
                                [
                                    ft.Container(
                                        height=16,
                                        width=1,
                                        bgcolor=theme.colors.primary_dark,
                                    ),
                                    ft.Text("or", size=16),
                                    ft.Container(
                                        height=16,
                                        width=1,
                                        bgcolor=theme.colors.primary_dark,
                                    ),
                                ],
                                spacing=10,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            StyledButton(
                                "Open an Existing Project",
                                ft.Icons.FILE_OPEN_OUTLINED,
                                size=20,
                                on_click=self.on_open_project,
                            ),
                        ],
                        expand=False,
                        spacing=20,
                    ),
                ],
                expand=False,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=False,
            padding=40,
            bgcolor=theme.colors.primary_white,
            border_radius=theme.variables.large_radius,
            border=ft.border.all(1, theme.colors.primary_dark),
        )

        self.controls = [
            ft.Column(
                [self.panel],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]

    def redraw(self):
        pass

    def on_new_project(self, _):
        self.app.new_project()

    def on_open_project(self, _):
        self.app.open_project()
