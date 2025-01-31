# from typing import Callable

import flet as ft
from src.pathways_app import PathwaysApp

from ..editors.conditions_editor import ConditionsEditor
from ..editors.criteria_editor import CriteriaEditor
from ..header import SmallHeader


class MetricsEditor(ft.Column):
    def __init__(self, app: PathwaysApp):
        super().__init__()

        self.app = app
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        self.spacing = 40

        self.conditions_editor = ConditionsEditor(
            app,
            pre_operation_content=ft.Row(
                [
                    SmallHeader("Conditions"),
                    ft.Container(expand=True),
                ],
                expand=True,
            ),
        )

        self.criteria_editor = CriteriaEditor(
            app,
            pre_operation_content=ft.Row(
                [
                    SmallHeader("Criteria"),
                    ft.Container(expand=True),
                ],
                expand=True,
            ),
        )

        self.controls = [
            ft.Column(
                expand=1,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.conditions_editor,
                ],
            ),
            ft.Column(
                expand=3,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.criteria_editor,
                ],
            ),
        ]

    def redraw(self):
        self.update_metrics()
        self.update()

    def update_metrics(self):
        self.conditions_editor.update_metrics()
        self.criteria_editor.update_metrics()
