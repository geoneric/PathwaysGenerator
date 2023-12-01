
# Build presentation in binary directory

# Add a target that builds the presentation in the bindary directory


add_custom_target(
    2023.12.progress.presentation
    COMMAND
        ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/presentation.qmd ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND
        ${QUARTO_EXECUTABLE} render ${CMAKE_CURRENT_BINARY_DIR}/presentation.qmd --to html
)
