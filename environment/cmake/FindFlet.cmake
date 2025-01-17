find_program(Flet_EXECUTABLE
    NAMES flet
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Flet DEFAULT_MSG
    Flet_EXECUTABLE
)

mark_as_advanced(
    Flet_EXECUTABLE
)
