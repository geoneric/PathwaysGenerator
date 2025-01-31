import flet as ft


class DefaultThemeColors:
    true_white = "#FFFFFF"
    off_white = "#EFF3FC"
    primary_white = "#DAE6FF"
    primary_lightest = "#C1D0FB"
    primary_lighter = "#92B0EF"
    primary_light = "#768ED5"
    primary_medium = "#6172B7"
    primary_dark = "#3A4192"
    primary_darker = "#160E59"
    secondary_light = "#91E0EC"
    secondary_medium = "#48BDCF"
    calculated_bg = "#60CCCCEE"
    calculated_icon = "#8888AA"
    row_selected = "#D5F9FF"
    completed = "#1BAC46"


colors = DefaultThemeColors()

action_colors = [
    "#DF2935",
    "#FCA858",
    "#EDE053",
    "#9FD154",
    "#3DAD79",
    "#68DED2",
    "#64C0E8",
    "#6691ED",
    "#AF97F0",
    "#C274C2",
    "#E887B2",
    "#F7687B",
]

action_icons = [
    ft.Icons.ACCESS_TIME_FILLED,
    ft.Icons.AC_UNIT,
    ft.Icons.ACCOUNT_BALANCE,
    ft.Icons.AIRPLANEMODE_ACTIVE,
    ft.Icons.BATTERY_FULL,
    ft.Icons.BRIGHTNESS_HIGH_SHARP,
    ft.Icons.BUILD_SHARP,
    ft.Icons.CALCULATE,
    ft.Icons.CAMERA_ALT,
    ft.Icons.CELL_TOWER,
    ft.Icons.CLOUD_SHARP,
    ft.Icons.CORONAVIRUS,
    ft.Icons.DEVICE_THERMOSTAT,
    ft.Icons.DIRECTIONS_BIKE,
    ft.Icons.DIRECTIONS_BOAT,
    ft.Icons.DIRECTIONS_CAR,
    ft.Icons.DIRECTIONS_BUS,
    ft.Icons.DIRECTIONS_TRAIN,
    ft.Icons.DIRECTIONS_WALK,
    ft.Icons.DISCOUNT_SHARP,
    ft.Icons.DIVERSITY_3_SHARP,
    ft.Icons.EMERGENCY_SHARP,
    ft.Icons.FAMILY_RESTROOM_SHARP,
    ft.Icons.FASTFOOD_SHARP,
    ft.Icons.FAVORITE,
    ft.Icons.FILTER_VINTAGE_OUTLINED,
    ft.Icons.FLASH_ON,
    ft.Icons.FLOOD_SHARP,
    ft.Icons.FOREST_SHARP,
]


class DefaultThemeVariables:
    small_radius = 3
    large_radius = 6
    panel_spacing = 6
    panel_padding = 10
    table_cell_padding = ft.padding.symmetric(4, 8)
    calculated_icon_size = 16
    icon_button_size = 16


variables = DefaultThemeVariables()


font_family = "Open Sans"
font_family_bold = "Open Sans - Bold"
font_family_semibold = "Open Sans - SemiBold"

fonts = {
    font_family: "fonts/Open_Sans/static/OpenSans-Regular.ttf",
    font_family_bold: "fonts/Open_Sans/static/OpenSans-Bold.ttf",
    font_family_semibold: "fonts/Open_Sans/static/OpenSans-SemiBold.ttf",
}


class DefaultThemeTextStyles:
    normal = ft.TextStyle(font_family=font_family, size=12, color=colors.primary_dark)

    logo = ft.TextStyle(
        size=16, height=1.1, color=colors.true_white, font_family=font_family
    )

    dropdown_large = ft.TextStyle(
        font_family=font_family_semibold,
        size=14,
        color=colors.primary_dark,
    )

    dropdown_normal = ft.TextStyle(
        font_family=font_family,
        size=12,
        color=colors.primary_dark,
    )

    textfield = ft.TextStyle(
        font_family=font_family, size=12, color=colors.primary_dark
    )

    textfield_symbol = ft.TextStyle(
        font_family=font_family, size=12, color=colors.primary_lighter
    )

    menu_button = ft.TextStyle(
        font_family=font_family,
        size=14,
        color=colors.true_white,
        overflow=ft.TextOverflow.VISIBLE,
    )

    button = ft.TextStyle(
        font_family=font_family_semibold,
        size=12,
        color=colors.true_white,
    )

    table_header = ft.TextStyle(
        font_family=font_family_semibold,
        size=12,
        color=colors.primary_dark,
    )

    action_tooltip = ft.TextStyle(
        font_family=font_family, size=10, color=colors.true_white
    )

    submenu_header = ft.TextStyle(
        font_family=font_family_semibold, size=10, color=colors.primary_dark
    )


text = DefaultThemeTextStyles()


class DefaultThemeIcons:
    globe = "icons/icon_globe.svg"
    actions = ft.Icons.CONSTRUCTION_OUTLINED
    metrics = ft.Icons.TUNE
    scenarios = ft.Icons.PUBLIC
    project_info = ft.Icons.INFO_OUTLINE
    maximize = ft.Icons.OPEN_IN_FULL
    minimize = ft.Icons.CLOSE_FULLSCREEN
    sidebar_open = ft.Icons.VIEW_SIDEBAR_OUTLINED
    sidebar_closed = ft.Icons.VIEW_SIDEBAR_OUTLINED


icon = "images/deltares-logo-white.png"
icons = DefaultThemeIcons()


class DefaultThemeButtons:
    primary = ft.ButtonStyle(
        color=colors.true_white,
        bgcolor=colors.primary_medium,
        padding=ft.padding.symmetric(0, 0),
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
    )

    menu_bar_button = ft.ButtonStyle(
        bgcolor=colors.primary_dark,
        color=colors.true_white,
        padding=ft.padding.symmetric(0, 20),
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        mouse_cursor=ft.MouseCursor.CLICK,
    )

    menu_button = ft.MenuStyle(
        alignment=ft.alignment.center_left,
        bgcolor=colors.true_white,
        shadow_color=colors.true_white,
        surface_tint_color=colors.true_white,
        padding=ft.padding.symmetric(0, 0),
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        side=ft.BorderSide(1, color=colors.primary_medium),
        mouse_cursor=ft.MouseCursor.CELL,
    )

    menu_bar = ft.MenuStyle(
        alignment=ft.alignment.center_left,
        bgcolor="#00000000",
        padding=ft.padding.symmetric(0, 0),
        shape=ft.RoundedRectangleBorder(radius=0),
        shadow_color="#00000000",
        side=None,
        mouse_cursor=ft.MouseCursor.CLICK,
    )

    submenu = ft.MenuStyle(
        alignment=ft.alignment.bottom_left,
        bgcolor=colors.true_white,
        shadow_color=colors.true_white,
        surface_tint_color=colors.true_white,
        padding=ft.padding.symmetric(0, 0),
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        # side=ft.BorderSide(1, color=colors.primary_medium),
        mouse_cursor=ft.MouseCursor.CELL,
        # alignment=ft.alignment.center_left,
        # bgcolor=colors.true_white,
        # shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        # side=ft.BorderSide(1, color=colors.primary_medium),
    )

    submenu_button = ft.ButtonStyle(
        color=colors.primary_dark,
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        padding=ft.padding.symmetric(4, 6),
        # side=ft.BorderSide(1, color=colors.primary_medium),
    )

    nested_submenu = ft.MenuStyle(
        alignment=ft.alignment.top_right,
        bgcolor=colors.true_white,
        shadow_color=colors.true_white,
        surface_tint_color=colors.true_white,
        padding=ft.padding.symmetric(0, 0),
        shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        # side=ft.BorderSide(1, color=colors.primary_medium),
        mouse_cursor=ft.MouseCursor.CELL,
        # alignment=ft.alignment.center_left,
        # bgcolor=colors.true_white,
        # shape=ft.RoundedRectangleBorder(radius=variables.small_radius),
        # side=ft.BorderSide(1, color=colors.primary_medium),
    )

    unit_menu = ft.ButtonStyle(
        color=colors.primary_dark,
        shape=ft.RoundedRectangleBorder(radius=0),
        padding=ft.padding.symmetric(0, 0),
        # side=ft.BorderSide(1, color=colors.primary_medium),
    )


buttons = DefaultThemeButtons()

theme = ft.Theme(
    font_family=font_family,
    primary_color=colors.primary_dark,
    primary_color_dark=colors.primary_dark,
    primary_color_light=colors.primary_light,
    popup_menu_theme=ft.PopupMenuTheme(color=colors.true_white),
    checkbox_theme=ft.CheckboxTheme(
        fill_color={ft.ControlState.SELECTED: colors.primary_medium},
        check_color=colors.true_white,
        border_side=ft.BorderSide(1, colors.primary_medium),
    ),
    text_theme=ft.TextTheme(
        title_large=ft.TextStyle(
            size=16, color=colors.primary_dark, font_family=font_family
        ),
        title_medium=ft.TextStyle(
            size=14, color=colors.primary_dark, font_family=font_family
        ),
        title_small=ft.TextStyle(
            size=12, color=colors.primary_dark, font_family=font_family
        ),
        display_large=ft.TextStyle(
            size=14, color=colors.primary_dark, font_family=font_family
        ),
        display_medium=ft.TextStyle(
            size=12, color=colors.primary_dark, font_family=font_family
        ),
        display_small=ft.TextStyle(
            size=10, color=colors.primary_dark, font_family=font_family
        ),
        headline_large=ft.TextStyle(
            size=14, color=colors.primary_dark, font_family=font_family
        ),
        headline_medium=ft.TextStyle(
            size=12, color=colors.primary_dark, font_family=font_family
        ),
        headline_small=ft.TextStyle(
            size=10, color=colors.primary_dark, font_family=font_family
        ),
        body_large=ft.TextStyle(
            size=14, color=colors.primary_dark, font_family=font_family
        ),
        body_medium=ft.TextStyle(
            size=12, color=colors.primary_dark, font_family=font_family
        ),
        body_small=ft.TextStyle(
            size=10, color=colors.primary_dark, font_family=font_family
        ),
        label_large=ft.TextStyle(
            size=14, color=colors.primary_dark, font_family=font_family
        ),
        label_medium=ft.TextStyle(
            size=12, color=colors.primary_dark, font_family=font_family
        ),
        label_small=ft.TextStyle(
            size=10, color=colors.primary_dark, font_family=font_family
        ),
    ),
)
