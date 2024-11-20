import flet as ft
import theme
import logging
from controls.header import Header

class TabbedPanel(ft.Column):
    selected_index: int = 0
    tab_buttons: list[ft.TextButton]
    content: ft.Container

    def __init__(self, tabs: list[tuple[Header,ft.Control]], selected_index: int):
        def get_tab_bgcolor(index: int):
            return theme.colors.primary_white if self.selected_index == index else theme.colors.primary_lighter

        def on_click(e):
            self.selected_index=self.tab_buttons.index(e.control)
            for [index, tab] in enumerate(self.tab_buttons):
                tab.content.bgcolor=get_tab_bgcolor(index)
                tab.content.update()
            self.content.content=tabs[self.selected_index][1]
            self.content.content.update()      

        super().__init__(
            expand=True,
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )

        self.selected_index=selected_index

        self.tab_buttons=[
            ft.TextButton(
                expand=True,
                content=ft.Container(
                    expand=True,
                    content=tab[0],
                    padding=10,
                    bgcolor=get_tab_bgcolor(index),
                    border_radius=ft.border_radius.only(
                        top_left=theme.variables.small_radius, 
                        top_right=theme.variables.small_radius,
                    ),
                    border = ft.border.only(
                        left=ft.BorderSide(1, theme.colors.primary_light),
                        right=ft.BorderSide(1, theme.colors.primary_light),
                        top=ft.BorderSide(1, theme.colors.primary_light),
                    ),
                ),
                style=ft.ButtonStyle(
                    padding=0, 
                    shape=ft.RoundedRectangleBorder(0),
                ),
                on_click=on_click,
            ) for [index, tab] in enumerate(tabs)
        ]

        self.content = ft.Container(
            expand=True,
            content=tabs[selected_index][1],
            margin=0,
            bgcolor=theme.colors.primary_white,
            border=ft.border.only(
                left=ft.BorderSide(1, theme.colors.primary_light),
                right=ft.BorderSide(1, theme.colors.primary_light),
                bottom=ft.BorderSide(1, theme.colors.primary_light),
            ),
            border_radius=ft.border_radius.only(
                bottom_left=theme.variables.small_radius,
                bottom_right=theme.variables.small_radius
            ),
        )

        self.controls = [
            ft.Row(
                controls=self.tab_buttons,
                spacing=3,
            ),
            self.content,
        ]

