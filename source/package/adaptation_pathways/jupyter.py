from . import dashboard


def view_in_jupyter(*, mode: str = "", server_url: str = "") -> int:
    kwargs = {}

    if mode:
        kwargs["jupyter_mode"] = mode

    if server_url:
        kwargs["jupyter_server_url"] = server_url

    app = dashboard.application()
    app.run(**kwargs)

    return 0
