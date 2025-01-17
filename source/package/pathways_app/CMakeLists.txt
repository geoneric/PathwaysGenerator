find_program(AP_FLET_COMMAND flet REQUIRED)


configure_file(
    pyproject.toml.in
    pyproject.toml
    @ONLY
)

add_custom_target(web_app
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory_if_different
            ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND
        ${CMAKE_COMMAND} -E env "PIP_FIND_LINKS=file://${PROJECT_BINARY_DIR}/dist"
            ${AP_FLET_COMMAND} build web ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND
        ${CMAKE_COMMAND} -E echo
            "Run a command like this to start the web app:"
            "${Python3_EXECUTABLE} -m http.server --directory ${CMAKE_CURRENT_BINARY_DIR}/build/web"
    DEPENDS
        package
    VERBATIM
)
