configure_file(
    conf.py.in
    conf.py
    @ONLY
)

set(AP_SPHINX_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(AP_SPHINX_BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/html)

add_custom_target(
    documentation
    COMMAND
        ${SPHINX_EXECUTABLE}
            -b html
            -c ${CMAKE_CURRENT_BINARY_DIR}
            ${AP_SPHINX_SOURCE_DIR} ${AP_SPHINX_BUILD_DIR}
)
