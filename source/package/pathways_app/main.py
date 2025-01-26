import logging

import flet as ft
from pathways_app.cli.app import main
import theme
from controls.editor_page import EditorPage
from controls.menu_bar import MenuBar
from pathways_app.app import App


locale.setlocale(locale.LC_ALL, "")


def main(page: ft.Page):
    # bitdojo_window could make a custom title bar
    # page.window.frameless = True
    # page.window.width = 1200
    # page.window.height = 800
    page.theme = theme.theme
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.resizable = True
    page.window.alignment = ft.alignment.center
    page.window.maximized = True

    page.title = "Pathways Generator"
    page.fonts = theme.fonts
    page.bgcolor = theme.colors.primary_darker
    page.padding = 1
    page.spacing = 0

    app = App(page)
    page.appbar = MenuBar(app)
    page.overlay.append(app.file_picker)

    page.add(
        ft.Container(
            expand=True,
            padding=theme.variables.panel_spacing,
            content=EditorPage(app.project),
            bgcolor=theme.colors.primary_lighter,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        )
    )


logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)

print("Pathways App Started")
