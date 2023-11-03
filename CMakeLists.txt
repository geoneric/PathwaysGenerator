cmake_minimum_required(
    VERSION 3.26)
project(AdaptationPathways
    LANGUAGES NONE
    VERSION 0.0.2
    DESCRIPTION "Adaptation Pathways TODO"
    HOMEPAGE_URL "https://publicwiki.deltares.nl/display/AP/Adaptation+Pathways"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

find_package(Sphinx REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

add_subdirectory(documentation)
add_subdirectory(source)

add_custom_target(
    package
    COMMAND
        ${CMAKE_COMMAND} -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
            ${Python3_EXECUTABLE}
                -m build
                --wheel
                --outdir ${CMAKE_CURRENT_BINARY_DIR}/dist
                ${CMAKE_CURRENT_SOURCE_DIR}
)

add_custom_target(
    release
    COMMAND
        ${CMAKE_COMMAND} -E tar "cf" "adaptation_pathways-${CMAKE_PROJECT_VERSION}.zip" --format=zip --
            "dist/*-${CMAKE_PROJECT_VERSION}-*.whl"
            documentation/html
)

add_dependencies(release
    test
    documentation
    package
)
