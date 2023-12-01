find_program(QUARTO_EXECUTABLE
    NAMES quarto
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Quarto DEFAULT_MSG
    QUARTO_EXECUTABLE
)

mark_as_advanced(
    QUARTO_EXECUTABLE
)
