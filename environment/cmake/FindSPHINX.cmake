find_program(SPHINX_APIDOC_EXECUTABLE
    NAMES sphinx-apidoc
)

find_program(SPHINX_BUILD_EXECUTABLE
    NAMES sphinx-build
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(SPHINX DEFAULT_MSG
    SPHINX_APIDOC_EXECUTABLE
    SPHINX_BUILD_EXECUTABLE
)

mark_as_advanced(
    SPHINX_APIDOC_EXECUTABLE
    SPHINX_BUILD_EXECUTABLE
)
