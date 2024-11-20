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

colors = DefaultThemeColors()

class DefaultThemeTextStyles:
    logo = ft.TextStyle(size=16, height=1.1)

class DefaultThemeVariables:
    small_radius = 3
    large_radius = 6
    panel_spacing = 6

class DefaultThemeIcons:
    globe = "icons/icon_globe.svg"

theme = ft.Theme(font_family = "Open Sans")
icon = "images/deltares-logo-white.png"
icons = DefaultThemeIcons()
text = DefaultThemeTextStyles()
variables = DefaultThemeVariables()
