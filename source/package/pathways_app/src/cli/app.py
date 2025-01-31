import locale

import flet as ft
from src import theme
from src.controls.menu_bar import MenuBar
from src.controls.pages.editor_page import EditorPage
from src.controls.pages.startup_page import StartupPage
from src.controls.pages.wizard_page import WizardPage
from src.pathways_app import PathwaysApp


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

    app = PathwaysApp(page)

    menu_bar = MenuBar(app)
    page.appbar = menu_bar

    app_container = ft.Container(
        expand=True,
        padding=theme.variables.panel_spacing,
        content=None,
        bgcolor=theme.colors.primary_lighter,
        border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
        alignment=ft.alignment.center,
    )

    page.add(app_container)

    def redraw():
        menu_bar.redraw()
        app_container.content.redraw()

    def rerender():
        troute = ft.TemplateRoute(page.route)

        if troute.match("/wizard"):
            app_container.content = WizardPage(app)
        elif troute.match("/project"):
            app_container.content = EditorPage(app)
        else:
            app_container.content = StartupPage(app)

        menu_bar.redraw()
        app_container.update()
        page.update()

    def render_route(_):
        rerender()

    app.on_conditions_changed.append(redraw)
    app.on_criteria_changed.append(redraw)
    app.on_scenarios_changed.append(redraw)
    app.on_actions_changed.append(redraw)
    app.on_action_color_changed.append(redraw)
    app.on_pathways_changed.append(redraw)
    app.on_project_info_changed.append(redraw)
    app.on_project_changed.append(rerender)

    page.on_route_change = render_route
    page.go("/project")
