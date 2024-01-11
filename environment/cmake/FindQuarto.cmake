find_program(Quarto_EXECUTABLE
    NAMES quarto
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Quarto DEFAULT_MSG
    Quarto_EXECUTABLE
)

mark_as_advanced(
    Quarto_EXECUTABLE
)
