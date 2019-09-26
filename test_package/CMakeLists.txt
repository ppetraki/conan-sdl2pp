cmake_minimum_required(VERSION 2.8.11)
project(test_package)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${SDL2_LIBRARIES})

# from upstream
ADD_DEFINITIONS(-DTESTDATA_DIR="${PROJECT_SOURCE_DIR}/testdata")

#
# doing this with try_compile() was a nightmare, so this will have to do
#

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLImage.hh")
  add_definitions(-DWITH_IMAGE)
  message(STATUS "SDLImage extension test enabled")
else()
  message(STATUS "SDLImage extension test disabled")
endif()

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLMixer.hh")
  add_definitions(-DWITH_MIXER)
  message(STATUS "SDLMixer extension test enabled")
else()
  message(STATUS "SDLMixer extension test disabled")
endif()

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLTTF.hh")
  add_definitions(-DWITH_TTF)
  message(STATUS "SDLTTF extension test enabled")
else()
  message(STATUS "SDLTTF extension test disabled")
endif()
