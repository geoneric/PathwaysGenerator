from . import dashboard, viewer


def view_in_window(port_nr: int) -> int:
    dashboard.serve_dashboard(port_nr)

    # TODO When the window closes, the service should stop as well
    return viewer.view(f"http:/127.0.0.1:{port_nr}")
