import flet as ft
import theme
from controls.actions_editor import ActionsEditor
from controls.graph_editor import GraphEditor
from controls.header import SectionHeader
from controls.metrics_editor import MetricsEditor
from controls.panel import Panel
from controls.pathways_editor import PathwaysPanel
from controls.scenarios_editor import ScenariosEditor
from controls.tabbed_panel import TabbedPanel

from adaptation_pathways.app.model.pathways_project import PathwaysProject


class EditorPage(ft.Row):
    def __init__(self, project: PathwaysProject):
        self.project = project
        self.expanded_editor: ft.Control | None = None

        self.metrics_editor = MetricsEditor(project)
        self.metrics_tab = (
            SectionHeader(theme.icons.metrics, size=20),
            self.metrics_editor,
        )

        self.actions_editor = ActionsEditor(project)
        self.actions_tab = (
            SectionHeader(theme.icons.actions, size=20),
            self.actions_editor,
        )

        self.scenarios_editor = ScenariosEditor(project)
        self.scenarios_tab = (
            SectionHeader(theme.icons.scenarios, size=20),
            self.scenarios_editor,
        )

        self.tabbed_panel = TabbedPanel(
            selected_index=0,
            tabs=[
                self.metrics_tab,
                self.actions_tab,
                self.scenarios_tab,
            ],
        )

        self.graph_editor = GraphEditor(project)
        self.graph_panel = Panel(self.graph_editor)

        self.pathways_editor = PathwaysPanel(project)
        self.pathways_panel = Panel(
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    self.pathways_editor,
                ],
            ),
            padding=theme.variables.panel_padding,
        )

        self.metrics_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.actions_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.scenarios_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.graph_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.graph_panel
        )
        self.pathways_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.pathways_panel
        )

        self.left_column = ft.Column(
            expand=2,
            spacing=theme.variables.panel_spacing,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self.tabbed_panel],
        )

        self.right_column = ft.Column(
            expand=3,
            spacing=theme.variables.panel_spacing,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self.graph_panel, self.pathways_panel],
        )

        super().__init__(
            expand=True,
            spacing=theme.variables.panel_spacing,
            controls=[self.left_column, self.right_column],
        )

        self.update_layout()

        project.on_conditions_changed.append(self.on_metrics_changed)
        project.on_criteria_changed.append(self.on_metrics_changed)
        project.on_scenarios_changed.append(self.on_scenarios_changed)
        project.on_actions_changed.append(self.on_actions_changed)
        project.on_action_color_changed.append(self.on_action_color_changed)
        project.on_pathways_changed.append(self.on_pathways_changed)

    def update_layout(self):
        if self.expanded_editor is None:
            self.left_column.visible = True
            self.right_column.visible = True
            self.graph_panel.visible = True
            self.pathways_panel.visible = True
        else:
            self.left_column.visible = self.expanded_editor == self.tabbed_panel
            self.pathways_panel.visible = self.expanded_editor == self.pathways_panel
            self.graph_panel.visible = self.expanded_editor == self.graph_panel
            self.right_column.visible = (
                self.pathways_panel.visible or self.graph_panel.visible
            )

        self.metrics_editor.header.set_expanded(
            self.expanded_editor == self.tabbed_panel
        )
        self.actions_editor.header.set_expanded(
            self.expanded_editor == self.tabbed_panel
        )
        self.scenarios_editor.header.set_expanded(
            self.expanded_editor == self.tabbed_panel
        )
        self.pathways_editor.header.set_expanded(
            self.expanded_editor == self.pathways_panel
        )
        self.graph_editor.header.set_expanded(self.expanded_editor == self.graph_panel)

    def on_editor_expanded(self, editor):
        if self.expanded_editor == editor:
            self.expanded_editor = None
        else:
            self.expanded_editor = editor

        self.update_layout()
        self.update()

    def on_metrics_changed(self):
        self.metrics_editor.redraw()
        self.scenarios_editor.redraw()
        self.actions_editor.redraw()
        self.pathways_editor.redraw()
        self.graph_editor.redraw()

    def on_scenarios_changed(self):
        self.scenarios_editor.redraw()
        self.graph_editor.redraw()

    def on_actions_changed(self):
        self.actions_editor.redraw()
        self.pathways_editor.redraw()
        self.graph_editor.redraw()

    def on_pathways_changed(self):
        self.pathways_editor.redraw()
        self.graph_editor.redraw()

    def on_action_color_changed(self):
        self.pathways_editor.redraw()
        self.graph_editor.redraw()
