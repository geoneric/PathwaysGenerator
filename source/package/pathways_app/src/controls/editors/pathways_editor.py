import flet as ft
from src import theme
from src.pathways_app import PathwaysApp

from adaptation_pathways.app.model.pathway import Pathway

from ..action_icon import ActionIcon
from ..metric_value import MetricValueCell
from ..styled_table import StyledTable, TableCell, TableColumn, TableRow


class PathwaysEditor(ft.Container):
    def __init__(self, app: PathwaysApp):
        self.app = app

        self.rows_by_pathway: dict[Pathway, ft.DataRow] = {}

        self.pathway_table = StyledTable(
            columns=[], rows=[], show_checkboxes=True, on_delete=self.on_delete_pathways
        )
        self.update_table()

        super().__init__(
            expand=True,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.pathway_table,
                ],
            ),
        )

    def redraw(self):
        self.update_table()
        self.update()

    def on_delete_pathways(self, rows: list[TableRow]):
        self.app.project.delete_pathways(row.row_id for row in rows)
        self.app.notify_pathways_changed()

    def update_table(self):
        self.pathway_table.set_columns(
            [
                TableColumn(
                    label="Pathway",
                    expand=2,
                ),
                *(
                    TableColumn(
                        label=metric.name,
                        key=metric.id,
                        alignment=ft.alignment.center_right,
                    )
                    for metric in self.app.project.all_metrics()
                ),
            ]
        )

        rows = []

        self.rows_by_pathway = {}
        for pathway in self.app.project.all_pathways:
            ancestors = self.app.project.get_ancestors_and_self(pathway)
            path = [*reversed([*ancestors])]
            row = self.get_pathway_row(pathway, path)
            self.rows_by_pathway[pathway] = row
            rows.append(row)

        self.pathway_table.set_rows(rows)
        return rows

    def on_metric_value_edited(self, cell: MetricValueCell):
        self.app.project.update_pathway_values(cell.metric.id)
        self.app.notify_pathways_changed()

    def get_pathway_row(self, pathway: Pathway, ancestors: list[Pathway]):
        children = [*self.app.project.get_children(pathway.id)]
        pathway_action = self.app.project.get_action(pathway.action_id)

        unused_action_ids = [
            action.id
            for action in self.app.project.all_actions
            if not any(ancestor.action_id == action.id for ancestor in ancestors)
            and not any(child.action_id == action.id for child in children)
        ]

        row_controls = [
            ActionIcon(self.app.project.get_action(ancestor.action_id), size=26)
            for ancestor in ancestors
        ]

        if pathway.parent_id is None:
            row_controls.append(ft.Text("  Current  ", color=pathway_action.color))

        if len(unused_action_ids) > 0:
            row_controls.append(
                ft.PopupMenuButton(
                    ft.Icon(
                        ft.Icons.ADD_CIRCLE_OUTLINE,
                        size=20,
                        color=theme.colors.primary_lightest,
                    ),
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ActionIcon(
                                        action,
                                        display_tooltip=False,
                                    ),
                                    ft.Text(
                                        action.name,
                                        style=theme.text.normal,
                                    ),
                                ]
                            ),
                            on_click=lambda e, action_id=action_id: self.extend_pathway(
                                pathway, action_id
                            ),
                        )
                        for action_id in unused_action_ids
                        for action in [self.app.project.get_action(action_id)]
                    ],
                    tooltip=ft.Tooltip(
                        "Add",
                        bgcolor=theme.colors.primary_white,
                    ),
                    bgcolor=theme.colors.off_white,
                    menu_position=ft.PopupMenuPosition.UNDER,
                ),
            )

        row = TableRow(
            row_id=pathway.id,
            cells=[
                TableCell(
                    ft.Container(
                        expand=True,
                        content=ft.Row(
                            spacing=0,
                            controls=row_controls,
                        ),
                    ),
                    sort_value=pathway.id,
                ),
                *(
                    MetricValueCell(
                        metric,
                        pathway.metric_data[metric.id],
                        on_finished_editing=self.on_metric_value_edited,
                    )
                    for metric in self.app.project.all_metrics()
                ),
            ],
            can_be_deleted=pathway.id != self.app.project.root_pathway_id,
        )

        return row

    def extend_pathway(self, pathway: Pathway, action_id: str):
        self.app.project.create_pathway(action_id, pathway.id)
        self.app.notify_pathways_changed()
