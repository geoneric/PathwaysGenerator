from typing import Callable

import flet as ft
from src import theme

from .header import SectionHeader


class TabbedPanel(ft.Container):

    def __init__(
        self,
        tabs: list[tuple[SectionHeader, ft.Control]],
        selected_index: int,
        on_tab_changed: Callable[[], None] | None = None,
    ):
        super().__init__(
            expand=True,
            bgcolor=theme.colors.primary_light,
            border=ft.border.all(1, theme.colors.primary_light),
            border_radius=ft.border_radius.all(theme.variables.small_radius),
        )

        self.selected_index = selected_index
        self.tabs = tabs
        self.on_tab_changed = on_tab_changed

        self.tab_buttons = [
            ft.Container(
                content=tab[0],
                padding=0,
                opacity=self.get_opacity(index),
                bgcolor=self.get_tab_bgcolor(index),
                on_click=self.on_tab_clicked,
            )
            for index, tab in enumerate(tabs)
        ]

        self.tab_content = ft.Container(
            expand=True,
            content=tabs[selected_index][1],
            margin=0,
            padding=theme.variables.panel_padding,
            bgcolor=theme.colors.primary_white,
        )

        self.content = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    expand=False,
                    bgcolor=theme.colors.primary_lightest,
                    content=ft.Column(
                        expand=True,
                        controls=self.tab_buttons,
                        spacing=0,
                    ),
                    padding=0,
                    border=ft.border.only(
                        right=ft.BorderSide(1, theme.colors.primary_lighter)
                    ),
                ),
                self.tab_content,
            ],
            spacing=0,
        )

    def get_tab_bgcolor(self, index: int):
        if self.selected_index == index:
            return theme.colors.primary_white
        return None

    def get_opacity(self, index: int):
        return 1 if self.selected_index == index else 0.5

    def on_tab_clicked(self, e):
        self.selected_index = self.tab_buttons.index(e.control)

        for [index, tab] in enumerate(self.tab_buttons):
            tab.bgcolor = self.get_tab_bgcolor(index)
            tab.opacity = self.get_opacity(index)

        self.tab_content.content = self.tabs[self.selected_index][1]
        self.update()

        if self.on_tab_changed is not None:
            self.on_tab_changed()
