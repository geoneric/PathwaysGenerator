import base64
import json
from typing import Callable

import flet as ft
import jsonpickle
from pyodide.code import run_js
from src.config import Config
from src.data import create_empty_project

from adaptation_pathways.app.model.pathways_project import PathwaysProject


is_web = True
try:
    import flet_js
except ModuleNotFoundError:
    is_web = False


class PathwaysApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.project = create_empty_project("Blank Project")
        self.project.organization = "Deltares"
        self.file_opener = ft.FilePicker(on_result=self.on_file_opened)
        self.file_saver = ft.FilePicker(on_result=self.on_file_saved)
        self.page.overlay.append(self.file_opener)
        self.page.overlay.append(self.file_saver)

        self.on_conditions_changed: list[Callable[[], None]] = []
        self.on_criteria_changed: list[Callable[[], None]] = []
        self.on_scenarios_changed: list[Callable[[], None]] = []
        self.on_actions_changed: list[Callable[[], None]] = []
        self.on_action_color_changed: list[Callable[[], None]] = []
        self.on_pathways_changed: list[Callable[[], None]] = []
        self.on_project_info_changed: list[Callable[[], None]] = []
        self.on_project_changed: list[Callable[[], None]] = []

        if is_web:
            old_send = flet_js.send

            def new_send(data: str):
                message = json.loads(data)
                action = message.get("action", None)
                if action == "open_project_result":
                    self.on_project_text_received(message.payload)
                else:
                    old_send(data)

            flet_js.send = new_send

    def notify_conditions_changed(self):
        for listener in self.on_conditions_changed:
            listener()

    def notify_criteria_changed(self):
        for listener in self.on_criteria_changed:
            listener()

    def notify_scenarios_changed(self):
        for listener in self.on_scenarios_changed:
            listener()

    def notify_actions_changed(self):
        for listener in self.on_actions_changed:
            listener()

    def notify_action_color_changed(self):
        for listener in self.on_action_color_changed:
            listener()

    def notify_pathways_changed(self):
        for listener in self.on_pathways_changed:
            listener()

    def notify_project_changed(self):
        for listener in self.on_project_changed:
            listener()

    def notify_project_info_changed(self):
        for listener in self.on_project_info_changed:
            listener()

    def on_event(self, event):
        print(event)

    def open_link(self, url: str):
        self.page.launch_url(url)

    def new_project(self):
        self.project = create_empty_project("New Project")
        self.page.go("/wizard")
        self.notify_project_changed()

    def open_project(self):
        if is_web:
            run_js(
                """
                self.postMessage('open_project');
            """
            )
        else:
            self.file_opener.pick_files(
                "Choose a Project File",
                file_type=ft.FilePickerFileType.ANY,
                allowed_extensions=[Config.project_extension],
                allow_multiple=False,
            )

    def on_file_opened(self, event: ft.FilePickerResultEvent):
        if len(event.files) == 0:
            return

        print(event.files[0].path)
        with open(event.files[0].path, encoding="utf-8") as file:
            text = file.read()
            file.close()

            self.project = jsonpickle.decode(text)
            self.page.go("/project")
            self.notify_project_changed()

    def on_project_text_received(self, content: str):
        project_dict = json.loads(content)
        self.project = PathwaysProject(**project_dict)
        self.page.go("/project")
        self.notify_project_changed()

    def save_project(self):
        if is_web:
            text: str = jsonpickle.encode(self.project)
            text_bytes = text.encode("uft-8")
            text_64_bytes = base64.b64encode(text_bytes)
            text_64_text = text_64_bytes.decode("utf-8")
            self.open_link(f"data:text/plain;base64,{text_64_text}")
        else:
            print("Saving on desktop")
            self.file_saver.save_file(
                "Save Pathways Project",
                f"{self.project.name}.{Config.project_extension}",
            )

    def on_file_saved(self, event: ft.FilePickerResultEvent):
        if event.path is None:
            print("NO PATH")
            return

        try:
            with open(event.path, "w", encoding="utf-8") as file:
                text = jsonpickle.encode(self.project)
                file.write(text)
                file.close()
        except Exception as error:
            print(error)
