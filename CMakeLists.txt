cmake_minimum_required(
    VERSION 3.26)
project(AdaptationPathways
    LANGUAGES NONE
    VERSION 0.0.5
    DESCRIPTION "Adaptation Pathways TODO"
    HOMEPAGE_URL "https://publicwiki.deltares.nl/display/AP/Adaptation+Pathways"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

find_package(CairoSVG REQUIRED)
find_package(PyInstaller REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
find_package(QtTools)
find_package(Quarto)
find_package(Sphinx REQUIRED)

set(AP_PLOT_GRAPHS
    "${CMAKE_CURRENT_SOURCE_DIR}/source/script/ap_plot_graphs.py"
)

add_subdirectory(documentation)

if(Quarto_FOUND)
    add_subdirectory(presentation)
endif()
add_subdirectory(source)

add_custom_target(logo
    VERBATIM
    COMMAND
        # Creates logo.{pdf,svg}
        ap_create_logo.py logo
)

add_custom_target(icon
    VERBATIM
    COMMAND
        cairosvg logo.svg -o icon.png
    COMMAND
    ${Python3_EXECUTABLE} -c "from PIL import Image; img = Image.open('icon.png'); img.save('icon.ico'); img.save('icon.icns')"
    DEPENDS
        logo
)

if(WIN32)
    set(AP_ICON icon.ico)
elseif(APPLE)
    set(AP_ICON icon.icns)
else()
    set(AP_ICON icon.png)
endif()

configure_file(
    adaptation_pathways.spec.in
    adaptation_pathways.spec
    @ONLY
)

add_custom_target(package
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND}
            -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
                ${Python3_EXECUTABLE}
                    -m build
                    --wheel
                    --outdir ${CMAKE_CURRENT_BINARY_DIR}/dist
                    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_custom_target(installer
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND}
            -E env "PYTHONPATH=${PROJECT_SOURCE_DIR}/source/package:$ENV{PYTHONPATH}"
                ${PyInstaller_EXECUTABLE} --noconfirm
                    adaptation_pathways.spec
    DEPENDS
        adaptation_pathways.spec
        icon
)

add_custom_target(release
    VERBATIM
    COMMAND
        ${CMAKE_COMMAND} -E rm -rf adaptation_pathways-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E make_directory
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/dist
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/documentation/html
    COMMAND
        ${CMAKE_COMMAND} -E copy
            "dist/*-${CMAKE_PROJECT_VERSION}-*.whl"
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/dist
    COMMAND
        ${CMAKE_COMMAND} -E copy_directory
            documentation/html
            adaptation_pathways-${CMAKE_PROJECT_VERSION}/documentation/html
    COMMAND
        ${CMAKE_COMMAND} -E tar "cf"
            "adaptation_pathways-${CMAKE_PROJECT_VERSION}.zip" --format=zip --
            adaptation_pathways-${CMAKE_PROJECT_VERSION}
    COMMAND
        ${CMAKE_COMMAND} -E rm -rf adaptation_pathways-${CMAKE_PROJECT_VERSION}
)

add_dependencies(release
    test
    documentation
    package
)
