find_program(CairoSVG_EXECUTABLE
    NAMES cairosvg
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(CairoSVG DEFAULT_MSG
    CairoSVG_EXECUTABLE
)

mark_as_advanced(
    CairoSVG_EXECUTABLE
)
