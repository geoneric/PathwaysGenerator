from abc import ABC
from typing import Callable

import flet as ft
from pyparsing import abstractmethod
from src import theme

from .input_filters import IntInputFilter
from .styled_table import TableCell


class EditableCell(TableCell, ABC):
    def __init__(
        self,
        display_control: ft.Control,
        edit_control: ft.Control,
        is_editing=False,
        is_calculated=False,
        can_reset=False,
        alignment: ft.Alignment | None = ft.alignment.center_left,
        padding: int | ft.Padding | None = theme.variables.table_cell_padding,
        sort_value: str | int | float | None = None,
        on_finished_editing: Callable[["EditableCell"], None] | None = None,
    ):
        self.display_content = display_control
        self.input_content = edit_control
        self.calculated_icon = ft.Container(
            ft.Icon(
                ft.Icons.CALCULATE,
                size=theme.variables.calculated_icon_size,
                color=theme.colors.calculated_icon,
            ),
            expand=True,
            alignment=ft.alignment.top_left,
        )
        self.reset_button = ft.Container(
            ft.Container(
                ft.Icon(
                    ft.Icons.RESTART_ALT,
                    size=theme.variables.calculated_icon_size,
                    color=theme.colors.calculated_icon,
                    tooltip=ft.Tooltip(
                        "Recalculate",
                        bgcolor=theme.colors.calculated_icon,
                        wait_duration=0,
                        vertical_offset=15,
                        text_style=theme.text.action_tooltip,
                    ),
                ),
                on_click=self.on_reset_to_calculated,
            ),
            expand=True,
            alignment=ft.alignment.top_left,
        )

        self.is_editing = is_editing
        self.is_calculated = is_calculated
        self.can_reset = can_reset
        self.on_finished_editing = on_finished_editing

        self.update_visibility()

        self.cell_content = ft.Container(
            expand=True,
            content=ft.Stack(
                [
                    self.display_content,
                    ft.Stack(
                        [
                            self.input_content,
                        ],
                        expand=True,
                    ),
                    self.calculated_icon,
                    self.reset_button,
                ],
                expand=True,
                alignment=alignment,
            ),
            padding=padding,
            bgcolor=theme.colors.calculated_bg if self.is_calculated else None,
            on_click=self.set_editing,
        )

        super().__init__(control=self.cell_content, sort_value=sort_value)

    def set_editing(self, _):
        self.is_editing = True
        self.update_controls()

    def set_not_editing(self, _):
        self.is_editing = False
        self.update_controls()

    def update_controls(self):
        if self.is_editing:
            self.update_input()
        else:
            self.update_display()

        self.update_visibility()
        self.control.update()

        if self.is_editing:
            self.input_content.focus()
        else:
            if self.on_finished_editing is not None:
                self.on_finished_editing(self)

    def update_visibility(self):
        self.display_content.visible = not self.is_editing
        self.input_content.visible = self.is_editing
        self.calculated_icon.visible = self.is_calculated and not self.is_editing
        self.reset_button.visible = self.can_reset and not self.is_editing

    def on_reset_to_calculated(self, _):
        pass

    @abstractmethod
    def update_display(self):
        pass

    @abstractmethod
    def update_input(self):
        pass


class EditableTextCell(EditableCell):
    def __init__(self, source: object, value_attribute: str, on_finished_editing=None):
        self.source = source
        self.value_attribute = value_attribute

        self.display_content = ft.Text(self.value, expand=True)
        self.input_content = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=self.value,
            keyboard_type=ft.KeyboardType.TEXT,
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            prefix_style=theme.text.textfield_symbol,
            suffix_style=theme.text.textfield_symbol,
            expand=True,
            content_padding=ft.padding.symmetric(4, 6),
            on_blur=self.set_not_editing,
        )

        def on_finished_editing_internal(_):
            self.value = self.input_content.value
            self.sort_value = self.value
            if on_finished_editing is not None:
                on_finished_editing(self)

        super().__init__(
            self.display_content,
            self.input_content,
            on_finished_editing=on_finished_editing_internal,
        )
        self.sort_value = self.value

    @property
    def value(self) -> str:
        return getattr(self.source, self.value_attribute)

    @value.setter
    def value(self, value: str):
        setattr(self.source, self.value_attribute, value)

    def update_input(self):
        self.input_content.value = self.display_content.value

    def update_display(self):
        self.display_content.value = self.input_content.value

    def on_reset_to_calculated(self, _):
        pass


class EditableIntCell(EditableCell):
    def __init__(self, source: object, value_attribute: str, on_finished_editing=None):
        self.source = source
        self.value_attribute = value_attribute

        self.display_content = ft.Text(self.value, expand=True)
        self.input_content = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=self.value,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=IntInputFilter(),
            bgcolor=theme.colors.true_white,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            prefix_style=theme.text.textfield_symbol,
            suffix_style=theme.text.textfield_symbol,
            expand=True,
            content_padding=ft.padding.symmetric(4, 6),
            on_blur=self.set_not_editing,
        )

        def on_finished_editing_internal(_):
            self.value = int(self.input_content.value)
            self.sort_value = self.value
            if on_finished_editing is not None:
                on_finished_editing(self)

        super().__init__(
            self.display_content,
            self.input_content,
            on_finished_editing=on_finished_editing_internal,
        )
        self.sort_value = self.value

    @property
    def value(self) -> int:
        return getattr(self.source, self.value_attribute)

    @value.setter
    def value(self, value: int):
        setattr(self.source, self.value_attribute, value)

    def update_input(self):
        self.input_content.value = self.display_content.value

    def update_display(self):
        self.display_content.value = self.input_content.value

    def on_reset_to_calculated(self, _):
        pass
