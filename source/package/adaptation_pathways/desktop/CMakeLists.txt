# add_custom_command(
#     OUTPUT
#         main_window.py
#     DEPENDS
#         main_window.ui
#     COMMAND
#         ${PYSIDE6_UIC_EXECUTABLE}
#             ${CMAKE_CURRENT_SOURCE_DIR}/main_window.ui -o ${CMAKE_CURRENT_BINARY_DIR}/main_window.py
#     VERBATIM
# )
#
# add_custom_target(ALL
#     DEPENDS
#         main_window.py
# )
