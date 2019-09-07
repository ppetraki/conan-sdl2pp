cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

# this is our top level project which gives us the opportunity
# to absorb the conan environment and adjust module paths
include(${CONAN_INSTALL_FOLDER}/conanbuildinfo.cmake)

conan_basic_setup()

# the upstream sources
add_subdirectory(source_subfolder)
