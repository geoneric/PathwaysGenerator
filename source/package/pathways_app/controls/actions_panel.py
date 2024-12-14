# pylint: disable=too-many-arguments,too-many-instance-attributes
import flet as ft
from pathways_app import theme
from pathways_app.controls.action_icon import ActionIcon
from pathways_app.controls.metric_value import MetricValueCell
from pathways_app.controls.sortable_header import SortableHeader, SortMode
from pathways_app.controls.styled_button import StyledButton
from pathways_app.controls.styled_table import StyledTable

from adaptation_pathways.app.model import Action, Metric


class ActionsPanel(ft.Column):
    actions: list[Action]
    metrics: list[Metric]
    sorted_actions: list[Action]
    sortable_headers: list[SortableHeader]
    action_table: StyledTable
    sorting_criteria: str | None = None
    sort_mode: SortMode = SortMode.NONE

    def __init__(self, actions: list[Action], metrics: list[Metric]):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=40,
            scroll=ft.ScrollMode.AUTO,
        )

        self.actions = actions
        self.metrics = metrics
        self.sorted_actions = [*actions]

        def on_sort_actions(header: SortableHeader):
            self.sort_mode = header.sort_mode

            if self.sort_mode == SortMode.NONE:
                self.sorting_criteria = None
            else:
                self.sorting_criteria = header.sort_key

            self.update_headers()
            self.update_rows()
            self.update()

        self.sortable_headers = [
            SortableHeader(sort_key="name", name="Name", on_sort=on_sort_actions),
            *(
                SortableHeader(
                    sort_key=metric.id,
                    name=metric.name,
                    on_sort=on_sort_actions,
                )
                for metric in metrics
            ),
        ]

        self.action_table = StyledTable(
            columns=[
                ft.DataColumn(
                    label=ft.Text("Icon", expand=True),
                ),
                *(
                    ft.DataColumn(label=header, numeric=header.sort_key != "name")
                    for header in self.sortable_headers
                ),
            ],
            rows=[],
            row_height=42,
        )

        self.update_rows()

        self.controls = [
            ft.Column(
                expand=False,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Row(
                        expand=False,
                        controls=[
                            ft.Container(expand=True),
                            StyledButton("New", icon=ft.icons.ADD_CIRCLE_OUTLINE),
                        ],
                    ),
                    ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[self.action_table],
                    ),
                ],
            ),
        ]

    def update_headers(self):
        for header in self.sortable_headers:
            if header.sort_key is not self.sorting_criteria:
                header.set_sort_mode(SortMode.NONE)
                header.update()

    def on_cell_edited(self, _: MetricValueCell):
        self.update_headers()
        self.update_rows()
        self.update()

    def update_rows(self):
        if self.sorting_criteria is not None:
            sorting_metric = next(
                (m for m in self.metrics if m.id == self.sorting_criteria), None
            )

            if sorting_metric is not None:

                def sort_by_metric(action: Action):
                    data = action.get_data(sorting_metric)
                    return data.value if data is not None else 0

                self.sorted_actions.sort(
                    key=sort_by_metric, reverse=self.sort_mode == SortMode.DESCENDING
                )
            else:

                def sort_by_attr(action: Action):
                    if self.sorting_criteria is None:
                        return ""
                    return getattr(action, self.sorting_criteria, "")

                self.sorted_actions.sort(
                    key=sort_by_attr, reverse=self.sort_mode == SortMode.DESCENDING
                )
        else:
            self.sorted_actions = [*self.actions]

        self.action_table.set_rows(
            [
                ft.DataRow(
                    [
                        ft.DataCell(
                            ft.PopupMenuButton(
                                ActionIcon(action),
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            [
                                                ActionIcon(a, display_tooltip=False),
                                                ft.Text(
                                                    a.name, style=theme.text.normal
                                                ),
                                            ]
                                        )
                                    )
                                    for a in self.actions
                                    if a != action
                                ],
                                bgcolor=theme.colors.off_white,
                                menu_position=ft.PopupMenuPosition.UNDER,
                            )
                        ),
                        ft.DataCell(ft.Text(action.name)),
                        *(
                            MetricValueCell(
                                metric,
                                action.get_data(metric),
                                on_finished_editing=self.on_cell_edited,
                            )
                            for metric in self.metrics
                        ),
                    ]
                )
                for action in self.sorted_actions
            ]
        )
