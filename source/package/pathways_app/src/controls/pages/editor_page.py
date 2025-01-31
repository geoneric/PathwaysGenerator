import flet as ft
from src import theme
from src.pathways_app import PathwaysApp

from ..editors.actions_editor import ActionsEditor
from ..editors.graph_editor import GraphEditor
from ..editors.metrics_editor import MetricsEditor
from ..editors.pathways_editor import PathwaysEditor
from ..editors.project_info_editor import ProjectInfoEditor
from ..editors.scenarios_editor import ScenariosEditor
from ..panel import Panel
from ..panel_header import PanelHeader
from ..tabbed_panel import TabbedPanel


class EditorPage(ft.Row):
    def __init__(self, app: PathwaysApp):
        self.app = app
        self.expanded_editor: ft.Control | None = None

        self.metrics_editor = MetricsEditor(app)
        self.metrics_header = PanelHeader("Metrics", theme.icons.metrics)
        self.metrics_tab = (
            self.get_tab_button(theme.icons.metrics, "Metrics"),
            ft.Column([self.metrics_header, self.metrics_editor]),
        )

        self.actions_editor = ActionsEditor(app)
        self.actions_header = PanelHeader(title="Actions", icon=theme.icons.actions)
        self.actions_tab = (
            self.get_tab_button(theme.icons.actions, "Actions"),
            ft.Column([self.actions_header, self.actions_editor], expand=True),
        )

        self.scenarios_editor = ScenariosEditor(app)
        self.scenarios_header = PanelHeader("Scenarios", theme.icons.scenarios)
        self.scenarios_tab = (
            self.get_tab_button(theme.icons.scenarios, "Scenarios"),
            ft.Column([self.scenarios_header, self.scenarios_editor], expand=True),
        )

        self.project_info_editor = ProjectInfoEditor(app)
        self.project_info_header = PanelHeader("Project Info", theme.icons.project_info)
        self.project_info_tab = (
            self.get_tab_button(theme.icons.project_info, "Project Info"),
            ft.Column(
                [self.project_info_header, self.project_info_editor], expand=True
            ),
        )

        self.tabbed_panel = TabbedPanel(
            selected_index=0,
            tabs=[
                self.metrics_tab,
                self.actions_tab,
                self.scenarios_tab,
                self.project_info_tab,
            ],
            on_tab_changed=self.redraw,
        )

        self.graph_editor = GraphEditor(app)
        self.graph_panel = Panel(self.graph_editor)

        self.pathways_editor = PathwaysEditor(app)
        self.pathways_header = PanelHeader("Pathways", ft.Icons.ACCOUNT_TREE_OUTLINED)
        self.pathways_panel = Panel(
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    self.pathways_header,
                    self.pathways_editor,
                ],
            ),
            padding=theme.variables.panel_padding,
        )

        self.metrics_header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.actions_header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.scenarios_header.on_expand = lambda: self.on_editor_expanded(
            self.tabbed_panel
        )
        self.graph_editor.header.on_expand = lambda: self.on_editor_expanded(
            self.graph_panel
        )
        self.pathways_header.on_expand = lambda: self.on_editor_expanded(
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

    def get_tab_button(self, icon: str, tooltip: str):
        return ft.Container(
            ft.Icon(
                icon,
                size=20,
                color=theme.colors.primary_dark,
            ),
            width=50,
            height=50,
            tooltip=ft.Tooltip(
                tooltip,
                wait_duration=0,
                bgcolor=theme.colors.primary_medium,
            ),
        )

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

        self.metrics_header.set_expanded(self.expanded_editor == self.tabbed_panel)
        self.actions_header.set_expanded(self.expanded_editor == self.tabbed_panel)
        self.scenarios_header.set_expanded(self.expanded_editor == self.tabbed_panel)
        self.pathways_header.set_expanded(self.expanded_editor == self.pathways_panel)
        self.graph_editor.header.set_expanded(self.expanded_editor == self.graph_panel)

    def on_editor_expanded(self, editor):
        if self.expanded_editor == editor:
            self.expanded_editor = None
        else:
            self.expanded_editor = editor

        self.update_layout()
        self.update()

    def redraw(self):
        if self.metrics_editor.page:
            self.metrics_editor.redraw()
        if self.scenarios_editor.page:
            self.scenarios_editor.redraw()
        if self.actions_editor.page:
            self.actions_editor.redraw()
        if self.project_info_editor.page:
            self.project_info_editor.redraw()
        self.pathways_editor.redraw()
        self.graph_editor.redraw()
        self.update()
