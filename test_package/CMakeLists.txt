cmake_minimum_required(VERSION 2.8.11)
project(test_package)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${SDL2_LIBRARIES})

function(add_option option)
    if(${option})
        target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE "${option}")
    endif()
endfunction()

# from upstream
ADD_DEFINITIONS(-DTESTDATA_DIR="${PROJECT_SOURCE_DIR}/testdata")

# XXX get options from upstream package
#add_option(WITH_IMAGE)
#add_option(WITH_MIXER)
#add_option(WITH_TTF)
