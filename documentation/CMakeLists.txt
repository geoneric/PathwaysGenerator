configure_file(
    conf.py.in
    conf.py
    @ONLY
)

configure_file(
    index.rst
    index.rst
    COPYONLY
)

set(AP_SPHINX_SOURCE_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(AP_SPHINX_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/html)

# https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html
add_custom_target(
    ap_apidoc
    COMMAND
        ${SPHINX_APIDOC_EXECUTABLE}
            --force
            --separate
            --module-first
            -o ${CMAKE_CURRENT_BINARY_DIR}
            ${PROJECT_SOURCE_DIR}/source/package/adaptation_pathways
)

# https://www.sphinx-doc.org/en/master/man/sphinx-build.html
# TODO Make this target depend on the ap_apidoc target
add_custom_target(
    documentation
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
            ${SPHINX_BUILD_EXECUTABLE}
                -b html
                -c ${CMAKE_CURRENT_BINARY_DIR}
                ${CMAKE_CURRENT_BINARY_DIR} ${AP_SPHINX_BUILD_DIR}
)
