import flet as ft
from controls.tabbed_panel import TabbedPanel
from controls.panel import Panel
from controls.header import Header
import logging
import theme

def main(page: ft.Page):
    page.theme = theme.theme

    # bitdojo_window could make a custom title bar
    # page.window.frameless = True

    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True
    page.title = "Pathways Generator"
    page.fonts = {
        "Open Sans":"fonts/Open_Sans/static/OpenSans-Regular.ttf"
    }
    page.bgcolor = theme.colors.primary_darker
    page.padding = 1
    page.spacing = 0
    
    page.appbar = ft.Container(
        height = 50,
        padding = ft.padding.symmetric(4, 5),
        margin=0,
        content = ft.Stack(
            controls=[
                ft.Row([
                    ft.Image(theme.icon),
                    ft.Text("PATHWAYS\nGENERATOR", style=theme.text.logo),
                ]),
                ft.Row([
                    ft.Container(
                        bgcolor=theme.colors.primary_medium,
                        border_radius=theme.variables.small_radius,
                        alignment=ft.alignment.center,
                        padding=ft.padding.symmetric(0, 15),
                        width=300,
                        content=ft.Stack([
                            ft.Column(
                                controls=[
                                    ft.Text("Sea Level Rise Adaptation"),
                                    ft.Text("Cork City Council", text_align=ft.TextAlign.CENTER)
                                ],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ])
                    )],                
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        ),
        bgcolor = theme.colors.primary_dark,
        border_radius=ft.border_radius.only(top_left=0, top_right=0),
        border = ft.border.only(
            bottom = ft.border.BorderSide(1, theme.colors.primary_darker)
        ),
    )
    
    page.add(ft.Container(
        expand=True,
        padding=theme.variables.panel_spacing,
        content=ft.Row(
            expand=True,
            spacing=theme.variables.panel_spacing,
            controls=[
                ft.Column(
                    expand=2,
                    spacing=theme.variables.panel_spacing,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        TabbedPanel(
                            selected_index=0,
                            tabs=[
                                [
                                    Header(theme.icons.globe, "Metrics"), 
                                    ft.Column(expand=True,controls=[ft.Text("Metrics")])
                                ],
                                [
                                    Header(theme.icons.globe, "Actions"), 
                                    ft.Column(expand=True,controls=[ft.Text("Actions")])
                                ],
                                [
                                    Header(theme.icons.globe, "Pathways"), 
                                    ft.Column(expand=True,controls=[ft.Text("Pathways")])
                                ],
                            ]
                        )
                    ],
                ),
                ft.Column(
                    expand=3, 
                    spacing=theme.variables.panel_spacing,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        Panel(
                            ft.Row(

                            ),
                        ),
                        Panel(
                            ft.Column(
                                expand=True, 
                                controls=[
                                    Header(theme.icons.globe, "Scenarios")
                                ],
                            )
                        ),
                    ], 
                ),
            ],
        ),
        bgcolor=theme.colors.primary_lighter,
        border_radius=ft.border_radius.only(bottom_left=8,bottom_right=8),
    ))

logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=4001)
