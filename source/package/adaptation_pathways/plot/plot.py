def configure_title(
    axes,
    *,
    title: str,
) -> None:

    if len(title) > 0:
        axes.set_title(title)


def y_axis_blended_to_data(axes, point):
    blended_to_display = axes.get_yaxis_transform()
    display_to_data = axes.transData.inverted()

    return display_to_data.transform(blended_to_display.transform(point))
