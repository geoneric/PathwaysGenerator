cmake_minimum_required(
    VERSION 3.26)
project(AdaptationPathways
    LANGUAGES NONE
    VERSION 0.0.0
    DESCRIPTION "Adaptation Pathways TODO"
    HOMEPAGE_URL "https://publicwiki.deltares.nl/display/AP/Adaptation+Pathways"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

find_package(Sphinx REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

add_subdirectory(documentation)
add_subdirectory(source)
