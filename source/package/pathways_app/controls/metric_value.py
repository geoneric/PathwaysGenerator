import flet as ft
from pathways_app import theme

from adaptation_pathways.app.model.metric import Metric, MetricValue


class FloatInputFilter(ft.InputFilter):
    def __init__(self):
        super().__init__(
            regex_string=r"^$|^[-+]?\d*(\.\d*)?$", allow=True, replacement_string=""
        )


class MetricValueCell(ft.DataCell):
    def __init__(self, metric: Metric, value: MetricValue, on_finished_editing=None):
        self.metric = metric
        self.value = value
        self.is_editing = False

        def toggle_editing(_):
            self.is_editing = not self.is_editing

            self.update_display()
            self.update_input()
            self.update_bg()

            self.update()

            if self.is_editing:
                self.input_content.focus()
            else:
                if on_finished_editing is not None:
                    on_finished_editing(self)

        self.display_content = ft.Text("")
        self.update_display()

        def on_value_changed(_):
            self.value.value = float(self.input_content.value)

        self.input_content = ft.TextField(
            dense=True,
            enable_suggestions=False,
            value=value.value,
            input_filter=FloatInputFilter(),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=theme.colors.primary_medium,
            focused_border_color=theme.colors.primary_light,
            cursor_color=theme.colors.primary_medium,
            text_style=theme.text.textfield,
            prefix_style=theme.text.textfield_symbol,
            suffix_style=theme.text.textfield_symbol,
            expand=True,
            on_change=on_value_changed,
            on_blur=toggle_editing,
        )
        self.update_input()

        self.cell_content = ft.Container(
            expand=True,
            content=ft.Stack([self.display_content, self.input_content]),
            on_click=toggle_editing,
        )
        self.update_bg()

        super().__init__(content=self.cell_content)

    def update_bg(self):
        self.cell_content.bgcolor = (
            theme.colors.calculated_bg
            if self.value.is_estimate and not self.is_editing
            else theme.colors.true_white
        )

    def update_display(self):
        self.display_content.value = self.metric.unit.format(self.value.value)
        self.display_content.visible = not self.is_editing

    def update_input(self):
        symbol = self.metric.unit.get_symbol(self.value.value)

        if self.metric.unit.place_after_value:
            self.input_content.prefix_text = None
            self.input_content.suffix_text = symbol
        else:
            self.input_content.prefix_text = symbol
            self.input_content.suffix_text = None

        self.input_content.visible = self.is_editing
