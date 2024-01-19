find_program(PyInstaller_EXECUTABLE
    NAMES pyinstaller
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(PyInstaller DEFAULT_MSG
    PyInstaller_EXECUTABLE
)

mark_as_advanced(
    PyInstaller_EXECUTABLE
)
