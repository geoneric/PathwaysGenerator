from typing import Callable

import flet as ft
from src import theme

from .header import SectionHeader


class PanelHeader(ft.Container):
    def __init__(
        self,
        title: str,
        icon: str | None = None,
        on_expand: Callable[[], None] | None = None,
    ):
        self.on_expand = on_expand
        self.icon = ft.Icon(ft.Icons.EXPAND, color=theme.colors.primary_dark, size=16)
        self.set_expanded(False)

        super().__init__(
            content=ft.Row(
                [
                    SectionHeader(icon, title),
                    ft.Container(expand=True),
                    ft.Container(
                        self.icon,
                        padding=0,
                        on_click=self.on_expand_clicked,
                    ),
                ]
            ),
            padding=ft.padding.only(bottom=8),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.colors.primary_dark)),
        )

    def set_expanded(self, expanded: bool):
        self.icon.name = theme.icons.minimize if expanded else theme.icons.maximize

    def on_expand_clicked(self, _):
        if self.on_expand is None:
            return

        self.on_expand()
