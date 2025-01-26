# pylint: disable=too-many-arguments,too-many-instance-attributes
import random

import flet as ft

from adaptation_pathways.app.model.action import Action
from adaptation_pathways.app.model.pathways_project import PathwaysProject

from .. import theme
from .action_icon import ActionIcon
from .editable_cell import EditableTextCell
from .metric_effect import MetricEffectCell
from .metric_value import MetricValueCell
from .panel_header import PanelHeader
from .styled_table import StyledTable, TableCell, TableColumn, TableRow


class ActionsEditor(ft.Column):
    def __init__(self, project: PathwaysProject):
        super().__init__(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=40,
        )

        self.project = project

        self.header = PanelHeader(title="Actions", icon=theme.icons.actions)

        self.action_table = StyledTable(
            columns=[],
            rows=[],
            row_height=42,
            on_add=self.on_new_action,
            on_delete=self.on_delete_actions,
        )
        self.update_table()

        self.controls = [
            ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.header,
                    self.action_table,
                ],
            ),
        ]

    def redraw(self):
        self.update_table()
        # self.update()

    def on_name_edited(self, _):
        self.project.notify_actions_changed()
        self.update()

    def on_cell_edited(self, cell: MetricValueCell):
        self.project.update_pathway_values(cell.metric.id)
        self.project.notify_actions_changed()
        self.update()

    def on_action_selected(self, action: Action):
        if action.id in self.project.selected_action_ids:
            self.project.selected_action_ids.remove(action.id)
        else:
            self.project.selected_action_ids.add(action.id)
        self.redraw()
        self.update()

    def on_delete_actions(self, rows: list[TableRow]):
        self.project.delete_actions(row.row_id for row in rows)
        self.project.notify_actions_changed()
        self.update()

    def on_new_action(self):
        self.project.create_action(
            random.choice(theme.action_colors),
            random.choice(theme.action_icons),
        )
        self.project.notify_actions_changed()
        self.update()

    def update_table(self):
        columns = [
            TableColumn(label="Icon", width=45, expand=False, sortable=False),
            TableColumn(
                label="Name",
            ),
            *(
                TableColumn(label=metric.name, key=metric.id)
                for metric in self.project.all_metrics()
            ),
        ]
        self.action_table.set_columns(columns)

        self.update_rows()

    def create_icon_editor(self, action: Action):
        def on_color_picked(color: str):
            action.color = color
            action_icon.update_action(action)
            self.project.notify_action_color_changed()

        def on_icon_picked(icon: str):
            action.icon = icon
            action_icon.update_action(action)
            self.project.notify_action_color_changed()

        def on_editor_closed(_):
            self.project.notify_actions_changed()

        def update_items():
            action_button.items = [
                ft.PopupMenuItem(
                    content=ft.GridView(
                        spacing=4,
                        width=200,
                        runs_count=4,
                        padding=ft.padding.symmetric(4, 6),
                        child_aspect_ratio=1.0,
                        controls=[
                            ft.Container(
                                bgcolor=color,
                                border=ft.border.all(
                                    2,
                                    (
                                        theme.colors.primary_medium
                                        if action.color == color
                                        else theme.colors.primary_lightest
                                    ),
                                ),
                                on_click=lambda e, c=color: on_color_picked(c),
                                width=10,
                                height=10,
                            )
                            for color in theme.action_colors
                        ],
                    )
                ),
                ft.PopupMenuItem(
                    content=ft.GridView(
                        expand=True,
                        runs_count=5,
                        padding=ft.padding.symmetric(12, 6),
                        controls=[
                            ft.Container(
                                ft.Icon(icon),
                                on_click=lambda e, i=icon: on_icon_picked(i),
                            )
                            for icon in theme.action_icons
                        ],
                        spacing=4,
                    )
                ),
            ]

        action_icon = ActionIcon(action)

        action_button = ft.PopupMenuButton(
            action_icon,
            items=[],
            bgcolor=theme.colors.off_white,
            menu_position=ft.PopupMenuPosition.UNDER,
            on_cancel=on_editor_closed,
        )
        update_items()
        return action_button

    def update_rows(self):
        rows = []

        for action in self.project.all_actions:
            if action.id == self.project.root_pathway.action_id:
                continue

            metric_cells = []
            for metric in self.project.all_metrics():
                effect = action.metric_data[metric.id]
                metric_cells.append(
                    MetricEffectCell(
                        metric, effect, on_finished_editing=self.on_cell_edited
                    )
                )

            rows.append(
                TableRow(
                    row_id=action.id,
                    cells=[
                        TableCell(self.create_icon_editor(action)),
                        EditableTextCell(action, "name", self.on_name_edited),
                        *metric_cells,
                    ],
                )
            )

        self.action_table.set_rows(rows)
