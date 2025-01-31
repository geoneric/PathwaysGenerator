import flet as ft
from src import theme


class StyledButton(ft.FilledButton):
    def __init__(
        self,
        text: str | None = None,
        icon: str | None = None,
        size=14,
        on_click=None,
    ):
        super().__init__(
            style=theme.buttons.primary,
            height=size * 2,
            on_click=on_click,
        )

        row = ft.Row(
            controls=[], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        if icon is not None:
            row.controls.append(ft.Icon(icon, color=theme.colors.true_white, size=size))

        if text is not None:
            row.controls.append(ft.Text(text, style=theme.buttons.primary, size=size))

        self.content = ft.Container(
            content=row, padding=ft.padding.symmetric(size * 0.25, size * 0.5)
        )
