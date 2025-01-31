find_program(Sed_EXECUTABLE
    NAMES sed
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Sed DEFAULT_MSG
    Sed_EXECUTABLE
)

mark_as_advanced(
    Sed_EXECUTABLE
)
