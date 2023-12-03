set(AP_PLOT_GRAPHS "${CMAKE_SOURCE_DIR}/source/script/ap_plot_graphs.py")

add_custom_command(
    OUTPUT
        pathways-1-actions_graph.svg
        pathways-1-pathways_graph.svg
        pathways-1-pathways_map.svg
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
            ${Python3_EXECUTABLE} ${AP_PLOT_GRAPHS}
                ${CMAKE_CURRENT_SOURCE_DIR}/pathways-1.txt ${CMAKE_CURRENT_BINARY_DIR}
)

add_custom_target(
    presentation.2023.12.progress
    COMMAND
        ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/presentation.qmd ${CMAKE_CURRENT_BINARY_DIR}
    COMMAND
        ${QUARTO_EXECUTABLE} render ${CMAKE_CURRENT_BINARY_DIR}/presentation.qmd --to html
    DEPENDS
        pathways-1-actions_graph.svg
        pathways-1-pathways_graph.svg
        pathways-1-pathways_map.svg
)
