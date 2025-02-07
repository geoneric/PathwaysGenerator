import typing


def configure_title(
    axes,
    *,
    arguments: dict[str, typing.Any],
) -> None:

    title: str = arguments.get("title", "")

    if len(title) > 0:
        axes.set_title(title)
