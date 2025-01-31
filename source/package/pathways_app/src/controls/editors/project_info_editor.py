import flet as ft
from src import theme
from src.pathways_app import PathwaysApp

from ..header import SmallHeader


class ProjectInfoEditor(ft.Container):
    def __init__(self, app: PathwaysApp):
        self.app = app

        self.project_name_input = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=self.app.project.name,
            keyboard_type=ft.KeyboardType.TEXT,
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            expand=False,
            content_padding=ft.padding.symmetric(12, 8),
            on_blur=self.on_name_edited,
            width=400,
        )

        self.project_org_input = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=self.app.project.organization,
            keyboard_type=ft.KeyboardType.TEXT,
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            expand=False,
            content_padding=ft.padding.symmetric(12, 8),
            on_blur=self.on_organization_edited,
            width=400,
        )

        super().__init__(
            ft.Column(
                controls=[
                    SmallHeader("Project Name"),
                    self.project_name_input,
                    SmallHeader("Organization"),
                    self.project_org_input,
                ],
                expand=False,
            ),
            expand=False,
        )

    def redraw(self):
        pass

    def on_name_edited(self, _):
        self.app.project.name = self.project_name_input.value
        self.app.notify_project_info_changed()

    def on_organization_edited(self, _):
        self.app.project.organization = self.project_org_input.value
        self.app.notify_project_info_changed()
