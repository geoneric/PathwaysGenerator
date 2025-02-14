def configure_title(
    axes,
    *,
    title: str,
) -> None:

    if len(title) > 0:
        axes.set_title(title)
