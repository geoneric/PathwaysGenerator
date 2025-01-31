from enum import Enum
from typing import Callable

import flet as ft
from src import theme
from src.pathways_app import PathwaysApp

from ..editors.actions_editor import ActionsEditor
from ..editors.conditions_editor import ConditionsEditor
from ..editors.pathways_editor import PathwaysEditor
from ..editors.project_info_editor import ProjectInfoEditor
from ..header import SectionHeader
from ..panel import Panel
from ..styled_button import StyledButton


class WizardStepState(Enum):
    INACTIVE = 0
    ACTIVE = 1
    COMPLETE = 2


class WizardStepTab(ft.Container):
    def __init__(
        self,
        name: str,
        index: int,
        total: int,
        state=WizardStepState.INACTIVE,
        on_click: Callable[["WizardStepTab"], None] | None = None,
    ):
        self.icon = ft.Icon()
        self.index = index
        self.total = total
        self.state = state
        self.click_handler = on_click

        super().__init__(
            ft.Column(
                [self.icon, ft.Text(name)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            padding=ft.padding.symmetric(10, 16),
            on_click=self.on_click_event,
            expand=True,
        )
        self.set_state(state)

    def on_click_event(self, _):
        if self.click_handler is None:
            return

        self.click_handler(self)

    def set_state(self, state: WizardStepState):
        self.icon.name = (
            ft.Icons.CHECK_CIRCLE_OUTLINE
            if state is WizardStepState.COMPLETE
            else ft.Icons.CIRCLE_OUTLINED
        )
        self.icon.color = (
            theme.colors.completed
            if state is WizardStepState.COMPLETE
            else theme.colors.primary_dark
        )

        self.border = ft.border.only(
            bottom=(
                None
                if state is WizardStepState.ACTIVE
                else ft.BorderSide(1, theme.colors.primary_medium)
            ),
            left=(
                None
                if state is not WizardStepState.ACTIVE or self.index == 0
                else ft.BorderSide(1, theme.colors.primary_medium)
            ),
            right=(
                None
                if state is not WizardStepState.ACTIVE or self.index == self.total - 1
                else ft.BorderSide(1, theme.colors.primary_medium)
            ),
        )

        self.bgcolor = (
            theme.colors.primary_lightest
            if state is not WizardStepState.ACTIVE
            else theme.colors.primary_white
        )


class WizardPage(ft.Row):
    def __init__(self, app: PathwaysApp):
        self.app = app
        self.explainer_text = ft.Text("This is some sort of explanation")
        self.finish_button = StyledButton("Finish", on_click=self.on_finish)
        self.next_button = StyledButton("Next", on_click=self.on_next)
        self.back_button = StyledButton("Back", on_click=self.on_back)
        self.buttons = ft.Row(
            [
                ft.Container(expand=True),
                self.back_button,
                self.next_button,
                self.finish_button,
            ]
        )
        self.step_content = ft.Container(expand=True)

        tab_names = ["Project", "Conditions", "Actions", "Pathways"]
        tab_count = len(tab_names)
        self.step_tabs = [
            WizardStepTab(name, index, tab_count, on_click=self.on_tab_clicked)
            for index, name in enumerate(tab_names)
        ]

        self.step_explanations = [
            "To create a project, you'll need to fill in some critical info.",
            "Conditions are the metrics you want to analyze the tipping points of.",
            "Actions are the steps you can take to adapt to the conditions you defined earlier.",
            "Pathways are ordered sequences of actions that adapt to a condition, up to a tipping point.",
        ]

        self.selected_tab_index = 0

        self.header = ft.Container(
            ft.Row(
                [
                    SectionHeader(
                        ft.Icons.EDIT_DOCUMENT,
                        "New Project Wizard",
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        ft.Icon(ft.Icons.CLOSE),
                        on_click=self.on_close,
                    ),
                ],
                expand=True,
            ),
            bgcolor=theme.colors.primary_lightest,
            padding=ft.padding.symmetric(10, 16),
            border=ft.border.only(bottom=ft.BorderSide(1, theme.colors.primary_medium)),
        )

        self.body = ft.Container(
            ft.Column(
                [
                    self.explainer_text,
                    self.step_content,
                    self.buttons,
                ]
            ),
            padding=theme.variables.panel_padding,
            expand=True,
        )

        super().__init__(
            controls=[
                ft.Column(
                    [
                        Panel(
                            ft.Column(
                                [
                                    self.header,
                                    ft.Row(self.step_tabs, spacing=0, expand=False),
                                    self.body,
                                ],
                                expand=True,
                                spacing=0,
                            ),
                            expand=False,
                            width=600,
                            height=600,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.set_selected_tab(self.selected_tab_index)

    def set_selected_tab(self, index: int):
        self.selected_tab_index = index

        for i, tab in enumerate(self.step_tabs):
            tab.set_state(
                WizardStepState.ACTIVE
                if i == self.selected_tab_index
                else (
                    WizardStepState.COMPLETE
                    if i < self.selected_tab_index
                    else WizardStepState.INACTIVE
                )
            )

        match self.selected_tab_index:
            case 0:
                # self.step_content.content = ft.Container(expand=True, bgcolor="#333020")
                self.step_content.content = ProjectInfoEditor(self.app)
            case 1:
                self.step_content.content = ConditionsEditor(self.app)
            case 2:
                self.step_content.content = ActionsEditor(self.app)
            case 3:
                self.step_content.content = PathwaysEditor(self.app)

        self.explainer_text.value = self.step_explanations[self.selected_tab_index]
        self.next_button.visible = self.selected_tab_index < (len(self.step_tabs) - 1)
        self.finish_button.visible = not self.next_button.visible

    def redraw(self):
        for tab in self.step_tabs:
            tab.update()

        self.step_content.update()
        self.step_content.content.redraw()
        self.buttons.update()
        self.next_button.update()
        self.finish_button.update()
        self.update()

    def on_tab_clicked(self, tab: WizardStepTab):
        self.set_selected_tab(tab.index)
        self.redraw()

    def on_back(self, _):
        if self.selected_tab_index == 0:
            self.app.page.go("/")
        else:
            self.set_selected_tab(self.selected_tab_index - 1)
            self.redraw()

    def on_next(self, _):
        self.set_selected_tab(self.selected_tab_index + 1)
        self.redraw()

    def on_close(self, _):
        self.app.page.go("/")

    def on_finish(self, _):
        self.app.page.go("/project")
