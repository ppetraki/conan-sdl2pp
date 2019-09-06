#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration

class Definitions:
  _data = {
      "cxxstd":
      {
        "default": "c++11",
        "conan_options": "ANY",
        "cmake_key": "SDL2PP_CXXSTD"
      },
      "static":
      {
        "default": False,
        "conan_options": [True, False],
        "cmake_key":"SDL2PP_STATIC"
      },
      "with_image":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key":"SDL2PP_WITH_IMAGE"
      },
      "with_mixer":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key": "SDL2PP_WITH_MIXER"
      },
      "with_ttf":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key": "SDL2PP_WITH_TTF"
      },
      "with_tests":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key" : "SDL2PP_WITH_TESTS"
      },
      "with_examples":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key": "SDL2PP_WITH_EXAMPLES"
      },
      "enable_livetests":
      {
        "default": True,
        "conan_options": [True, False],
        "cmake_key": "SDL2PP_ENABLE_LIVE_TESTS"
      },
  }

  def generate_options(self):
    options = {}
    for k,v in self._data.items():
      options[k] = v["conan_options"]
    return options

  def generate_default_options(self):
    default_options = {}
    for k,v in self._data.items():
      default_options[k] = v["default"]
    return default_options

  def populate_cmake_configuration(self, options, cmake_ref):
    for k, v in options.items():
      print("SELFOPT {} {}".format(k, v))

    for k, v in options.items():
      cmake_key = self._data[k]["cmake_key"]
      cmake_ref.definitions[cmake_key] = v


class SDL2ppConan(ConanFile):
    name            = "sdl2pp"
    version         = "0.16.0"
    license         = "MIT"
    author          = "Peter M. Petrakis  peter.petrakis@protonmail.com"
    url             = "https://github.com/libSDL2pp/libSDL2pp.git"
    description     = "C++11 bindings/wrapper for SDL2"
    topics          = ("gui", "modern-cpp", "cross-platform")
    settings = "os", "arch", "compiler", "build_type", "cppstd"
    generators = ['cmake']

    requires = "sdl2/2.0.8@bincrafters/stable"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _upstream   = "https://github.com/libSDL2pp/libSDL2pp.git"
    _tag        = "0.16.0"

    defs = Definitions()
    default_options = defs.generate_default_options()
    options = defs.generate_options()

    def source(self):
        self.run("rm -rf %s" % self._source_subfolder)
        self.run("git clone --branch %s  -- %s %s" %
                (self._tag, self._upstream, self._source_subfolder))

    def _configure_cmake(self):
        cmake = CMake(self)
        defs = Definitions()
        defs.populate_cmake_configuration(self.options, cmake)
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        cmake.test()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install(build_dir=self._build_subfolder)

    def package_info(self):
        self.cpp_info.libs = [self.name]
