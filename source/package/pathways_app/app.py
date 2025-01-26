import flet as ft
from pathways_app import example
from pathways_app.config import Config


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.project = example.project
        self.file_picker = ft.FilePicker(on_result=self.on_file_opened)

    def open_link(self, url: str):
        self.page.launch_url(url)

    def open_project(self):
        print("Open")
        self.file_picker.pick_files(
            "Choose a Project File",
            file_type=ft.FilePickerFileType.ANY,
            allowed_extensions=[Config.project_extension],
            allow_multiple=False,
        )

    def on_file_opened(self, event: ft.FilePickerResultEvent):
        for file in event.files:
            print(file)
