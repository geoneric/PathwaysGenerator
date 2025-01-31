# pylint: disable=too-many-arguments
import flet as ft
from src import theme
from src.utils import find_index


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
            text_style=text_style or theme.text.dropdown_normal,
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

        self.option_icons = option_icons

        self.internal_icon = ft.Icon(
            "",
            color=theme.colors.primary_dark,
            expand=False,
        )
        self.internal_text = ft.Text("", style=self.text_style)
        # self.suffix = ft.Container(

        #     width=18,
        #     height=18,
        #     alignment=ft.alignment.center,
        #     bgcolor="#000000",
        # )
        self.suffix_icon = ft.Icon(
            ft.Icons.ARROW_DROP_DOWN, color=theme.colors.primary_medium
        )
        self.prefix = ft.Row(
            spacing=5,
            controls=[self.internal_icon, self.internal_text],
        )
        self.set_options(options, option_icons)
        self.change_callback = on_change
        self.on_change = self.on_value_changed

    def update_icon(self):
        option_index = find_index(self.options, lambda el: el.key == self.value)
        if option_index is None:
            return

        option = self.options[option_index]
        if self.option_icons is not None:
            self.internal_icon.visible = True
            self.internal_icon.name = self.option_icons[option_index]
        else:
            self.internal_icon.visible = False
        self.internal_text.value = option.text or option.key

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
