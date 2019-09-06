#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class PackageConfig:
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
            "cmake_key": "SDL2PP_STATIC"
        },
        "with_image":
        {
            "default": False,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_WITH_IMAGE"
        },
        "with_mixer":
        {
            "default": False,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_WITH_MIXER"
        },
        "with_ttf":
        {
            "default": False,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_WITH_TTF"
        },
        "with_tests":
        {
            "default": False,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_WITH_TESTS"
        },
        "with_examples":
        {
            "default": True,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_WITH_EXAMPLES"
        },
        "enable_livetests":
        {
            "default": False,
            "conan_options": [True, False],
            "cmake_key": "SDL2PP_ENABLE_LIVE_TESTS"
        },
    }

    @staticmethod
    def generate_options():
        options = {}
        for k, v in PackageConfig._data.items():
            options[k] = v["conan_options"]
        return options

    @staticmethod
    def generate_default_options():
        default_options = {}
        for k, v in PackageConfig._data.items():
            default_options[k] = v["default"]
        return default_options

    @staticmethod
    def populate_cmake_configuration(options, cmake_ref):
        for k, v in options.items():
            cmake_key = PackageConfig._data[k]["cmake_key"]
            cmake_ref.definitions[cmake_key] = v


class SDL2ppConan(ConanFile):
    name = "sdl2pp"
    version = "0.16.0"
    license = "MIT"
    author = "Peter M. Petrakis  peter.petrakis@protonmail.com"
    url = "https://sdl2pp.amdmi3.ru"
    description = "C++11 bindings/wrapper for SDL2"
    topics = ("gui", "modern-cpp", "cross-platform")
    settings = "os", "arch", "compiler", "build_type"
    generators = ['cmake']

    # XXX newer versions blowup on Android due to hid linking issue
    requires = "sdl2/2.0.8@bincrafters/stable"

    _source_subfolder = "source_subfolder"
    _upstream = "https://github.com/libSDL2pp/libSDL2pp.git"
    _tag = "0.16.0"

    default_options = PackageConfig.generate_default_options()
    options = PackageConfig.generate_options()

    def source(self):
        self.run("rm -rf %s" % self._source_subfolder)
        self.run("git clone --branch %s  -- %s %s" %
                 (self._tag, self._upstream, self._source_subfolder))

    def _configure_cmake(self):
        cmake = CMake(self)
        PackageConfig.populate_cmake_configuration(self.options, cmake)
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if self.options.with_tests:
            cmake.test()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["SDL2pp"]
