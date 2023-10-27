find_program(SPHINX_APIDOC_EXECUTABLE
    NAMES sphinx-apidoc
)

find_program(SPHINX_BUILD_EXECUTABLE
    NAMES sphinx-build
)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(Sphinx "Failed to find sphinx-apidoc executable" SPHINX_APIDOC_EXECUTABLE)
find_package_handle_standard_args(Sphinx "Failed to find sphinx-build executable" SPHINX_BUILD_EXECUTABLE)
