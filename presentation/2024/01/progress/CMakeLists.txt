add_custom_target(
    presentation.2024.01.progress
    COMMAND
        ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/presentation.qmd ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND
        ${QUARTO_EXECUTABLE} render ${CMAKE_CURRENT_BINARY_DIR}/presentation.qmd --to html
)
