import flet as ft
from pathways_app import theme

from adaptation_pathways.app.model.action import Action


class ActionIcon(ft.Container):
    def __init__(self, action: Action, display_tooltip=True, size=36):
        super().__init__(
            content=ft.Stack(
                controls=[
                    ft.Icon(action.icon, size=(size * 0.5), color=action.color),
                    ft.Icon(
                        ft.icons.CIRCLE_OUTLINED,
                        size=size,
                        color=action.color,
                        tooltip=(
                            ft.Tooltip(
                                action.name,
                                bgcolor=action.color,
                                text_style=theme.text.action_tooltip,
                                # vertical_offset=size * 0.75,
                            )
                            if display_tooltip
                            else None
                        ),
                    ),
                ],
                alignment=ft.alignment.center,
            ),
        )
