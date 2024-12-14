import flet as ft
from pathways_app import theme
from pathways_app.controls.action_icon import ActionIcon
from pathways_app.controls.styled_table import StyledTable

from adaptation_pathways.app.model import Action, Metric
from adaptation_pathways.app.model.pathway import Pathway


class PathwaysPanel(ft.Column):
    def __init__(self, root: Pathway, metrics: list[Metric], actions: list[Action]):

        self.root = root
        self.metrics = metrics
        self.actions = actions

        columns = [
            ft.DataColumn(ft.Text("Pathway")),
            *(ft.DataColumn(ft.Text(metric.name), numeric=True) for metric in metrics),
        ]

        self.rows_by_pathway: dict[Pathway, ft.DataRow] = {}

        self.pathway_table = StyledTable(columns=columns, rows=[], show_checkboxes=True)

        self.update_pathway_rows()

        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Column(
                    expand=False,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[self.pathway_table],
                )
            ],
        )

    def update_pathway_rows(self):
        current_row = ft.DataRow(
            [
                ft.DataCell(
                    ft.Row(
                        spacing=5,
                        controls=[
                            ActionIcon(self.root.last_action, size=26),
                            ft.Text("Current", color=self.root.last_action.color),
                        ],
                    )
                ),
                *(
                    ft.DataCell(
                        ft.Text(
                            value=self.root.get_formatted_value(metric),
                        ),
                    )
                    for metric in self.metrics
                ),
            ]
        )
        current_row.color = theme.colors.off_white

        rows = [
            current_row,
        ]

        self.rows_by_pathway = {}
        for pathway, path in self.root.all_child_paths():
            row = self.get_pathway_row(pathway, path)
            self.rows_by_pathway[pathway] = row
            rows.append(row)

        self.pathway_table.set_rows(rows)
        return rows

    def get_pathway_row(self, pathway: Pathway, ancestors: list[Pathway]):
        unused_actions = [
            a
            for a in self.actions
            if not any(node.last_action == a for node in ancestors)
            and (
                pathway.children is None
                or not any(child.last_action == a for child in pathway.children)
            )
        ]

        row_controls = [
            *(ActionIcon(node.last_action, size=26) for node in ancestors[1:-1]),
            ActionIcon(pathway.last_action, size=26),
        ]

        if len(unused_actions) > 0:
            row_controls.append(
                ft.PopupMenuButton(
                    ft.Icon(
                        ft.icons.ADD_CIRCLE_OUTLINE,
                        size=20,
                        color=theme.colors.primary_lightest,
                    ),
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                [
                                    ActionIcon(a, display_tooltip=False),
                                    ft.Text(
                                        a.name,
                                        style=theme.text.normal,
                                    ),
                                ]
                            ),
                            on_click=lambda e, new_action=a: self.extend_pathway(
                                pathway, new_action, ancestors
                            ),
                        )
                        for a in unused_actions
                    ],
                    tooltip=ft.Tooltip(
                        "Add",
                        bgcolor=theme.colors.primary_white,
                    ),
                    bgcolor=theme.colors.off_white,
                    menu_position=ft.PopupMenuPosition.UNDER,
                ),
            )

        row = ft.DataRow(
            [
                ft.DataCell(
                    ft.Container(
                        expand=True,
                        content=ft.Row(
                            spacing=0,
                            controls=row_controls,
                        ),
                    ),
                ),
                *(
                    ft.DataCell(
                        ft.Text(
                            value=pathway.get_formatted_value(metric),
                        )
                    )
                    for metric in self.metrics
                ),
            ],
        )

        def on_select_changed(e):
            row.selected = e.data
            row.update()

        row.on_select_changed = on_select_changed
        return row

    def extend_pathway(
        self, pathway: Pathway, action: Action, ancestors: list[Pathway]
    ):
        if pathway.children is None:
            pathway.children = []

        new_pathway = Pathway(Pathway.get_id(ancestors, action), action, {})
        pathway.children.append(new_pathway)

        self.update_pathway_rows()

        new_row = self.rows_by_pathway[new_pathway]
        new_row.selected = True

        self.update()
