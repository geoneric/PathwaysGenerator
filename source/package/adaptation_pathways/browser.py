import webbrowser

from . import dashboard


def view_in_browser(port_nr: int) -> int:
    dashboard.serve_dashboard(port_nr)

    # TODO title
    webbrowser.open(f"http:/127.0.0.1:{port_nr}")

    return 0
