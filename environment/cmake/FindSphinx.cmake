find_program(Sphinx_APIDOC_EXECUTABLE
    NAMES sphinx-apidoc
)

find_program(Sphinx_BUILD_EXECUTABLE
    NAMES sphinx-build
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Sphinx DEFAULT_MSG
    Sphinx_APIDOC_EXECUTABLE
    Sphinx_BUILD_EXECUTABLE
)

mark_as_advanced(
    Sphinx_APIDOC_EXECUTABLE
    Sphinx_BUILD_EXECUTABLE
)
