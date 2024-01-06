find_program(PYSIDE6_UIC_EXECUTABLE
    NAMES pyside6-uic
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(QtTools DEFAULT_MSG
    PYSIDE6_UIC_EXECUTABLE
)

mark_as_advanced(
    PYSIDE6_UIC_EXECUTABLE
)
