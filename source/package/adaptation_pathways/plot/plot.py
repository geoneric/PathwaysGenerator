import typing

import matplotlib as mpl


def configure_title(
    axes: mpl.axes.Axes,
    *,
    arguments: dict[str, typing.Any],
) -> None:

    title: str = arguments.get("title", "")

    if len(title) > 0:
        axes.set_title(title)
