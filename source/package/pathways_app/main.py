import logging

import flet as ft
from pathways_app.cli.app import main


logging.basicConfig(level=logging.CRITICAL)
ft.app(target=main, assets_dir="assets")

print("Pathways App Started")
