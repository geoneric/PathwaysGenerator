import logging

import flet as ft
from src.cli.app import main


logging.basicConfig(level=logging.CRITICAL)
ft.app(
    target=main,
    assets_dir="assets",
    view=ft.AppView.FLET_APP,
    route_url_strategy="hash",
)

print("Pathways App Started")
