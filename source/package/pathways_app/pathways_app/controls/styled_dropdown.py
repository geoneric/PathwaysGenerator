# pylint: disable=too-many-arguments
import flet as ft
import theme
from utils import find_index


class StyledDropdown(ft.Dropdown):
    def __init__(
        self,
        value: str,
        options: list[ft.dropdown.Option],
        option_icons: list[str] | None = None,
        width: ft.OptionalNumber = None,
        height: ft.OptionalNumber = 28,
        text_style: ft.TextStyle | None = None,
        on_change=None,
        on_blur=None,
    ):
        super().__init__(
            value=value,
            text_style=text_style,
            expand=False,
            options=[],
            width=width,
            bgcolor=theme.colors.true_white,
            content_padding=ft.padding.symmetric(4, 8),
            padding=0,
            height=height,
            border_color=theme.colors.primary_dark,
            icon_enabled_color=theme.colors.primary_dark,
            on_blur=on_blur,
        )

        self.prefix = ft.Row(
            spacing=5,
            controls=[],
        )
        self.text_style = text_style
        self.set_options(options, option_icons)
        self.change_callback = on_change
        self.on_change = self.on_value_changed

    def update_icon(self):
        if self.option_icons is None:
            return

        option_index = find_index(self.options, lambda el: el.key == self.value)
        if option_index is not None:
            self.prefix.visible = True
            self.prefix.controls = [
                ft.Icon(
                    self.option_icons[option_index],
                    color=theme.colors.primary_dark,
                    expand=False,
                ),
                ft.Text(self.value, style=self.text_style),
            ]
        else:
            self.prefix.visible = False

    def set_options(
        self, options: list[ft.dropdown.Option], icons: list[str] | None = None
    ):
        self.options = options
        self.option_icons = icons
        self.update_icon()

    def on_value_changed(self, e):
        self.update_icon()
        self.update()

        if self.change_callback is not None:
            self.change_callback(e)
