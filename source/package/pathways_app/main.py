import logging

import flet as ft
from pathways_app.cli.app import main


logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)

print("Pathways App Started")
