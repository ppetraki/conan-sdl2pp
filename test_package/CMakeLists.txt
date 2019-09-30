cmake_minimum_required(VERSION 2.8.11)
project(test_package)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# SDL2pp defines it's own Find modules for Image, Mixer, and TTF
# XXX TTF depends on Image
list(APPEND CMAKE_MODULE_PATH "${CONAN_SDL2PP_ROOT}/cmake")

find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${SDL2_LIBRARIES})

# from upstream
ADD_DEFINITIONS(-DTESTDATA_DIR="${PROJECT_SOURCE_DIR}/testdata")

# in travis we're just checking whether we can find the headers and link
# this is forwarded by conanfile.py
if(CONAN_DOCKER_IMAGE)
  message(WARNING "DISABLING HW TESTS")
  add_definitions(-DDISABLE_HW_TESTS)
endif()

#
# doing this with try_compile() was a nightmare, so this will have to do
#

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLImage.hh")
  find_package(SDL2_image REQUIRED)
  add_definitions(-DWITH_IMAGE)
  target_link_libraries(${PROJECT_NAME} ${SDL2_IMAGE_LIBRARY})
  message(STATUS "SDLImage extension test enabled")
else()
  message(STATUS "SDLImage extension test disabled")
endif()

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLMixer.hh")
  find_package(SDL2_mixer REQUIRED)
  add_definitions(-DWITH_MIXER)
  target_link_libraries(${PROJECT_NAME} ${SDL2_MIXER_LIBRARY})
  message(STATUS "SDLMixer extension test enabled")
else()
  message(STATUS "SDLMixer extension test disabled")
endif()

if (EXISTS "${CONAN_INCLUDE_DIRS_SDL2PP}/SDL2pp/SDLTTF.hh")
  find_package(SDL2_image REQUIRED)
  find_package(SDL2_ttf REQUIRED)
  target_link_libraries(${PROJECT_NAME} ${SDL2_TTF_LIBRARY} ${SDL2_IMAGE_LIBRARY})
  add_definitions(-DWITH_TTF)
  message(STATUS "SDLTTF extension test enabled")
else()
  message(STATUS "SDLTTF extension test disabled")
endif()
