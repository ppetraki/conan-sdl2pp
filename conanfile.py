#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools


class PackageConfig:
    # XXX add a function to generate a table in markdown format
    # XXX add description field
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
            "default": False,
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
            print("incoming conan options {}={}".format(k, v))
            cmake_key = PackageConfig._data[k]["cmake_key"]
            print("setting cmake {}={}".format(cmake_key, v))
            cmake_ref.definitions[cmake_key] = v


class SDL2ppConan(ConanFile):
    name = "sdl2pp"
    version = "0.16.0"
    description = "C++11 bindings/wrapper for SDL2"
    url = "https://github/ppetraki/conan-sdl2pp"
    homepage = "https://sdl2pp.amdmi3.ru"
    author = "Peter M. Petrakis  peter.petrakis@protonmail.com"
    license = "MIT"
    topics = ("gui", "modern-cpp", "cross-platform")

    # The CMakeLists.txt turns the upstream project into
    # a subproject which allows us to inject the conan
    # environment definitions.
    #
    # Requires CONAN_INSTALL_FOLDER, who's value is determined
    # at runtime
    #
    # The patch makes sure our options aren't overridden by upstream
    # There is also some intrinsic behavior that prevented the build
    # from producing install targets now that it's a subproject.
    #
    # XXX refactor upstream patch to detect conan environment and load
    # defs conditionally. Then we can dump the parent cmake file and
    # there will be less conditions in the upstream cmake as we'll
    # just enable conan *after* the project sets it's defaults so we
    # can get our config in.
    exports_sources = ['CMakeLists.txt', 'cmake.patch']

    generators = ['cmake']

    _build_subfolder = "build_subfolder"
    _source_subfolder = "source_subfolder"

    settings = "os", "arch", "compiler", "build_type"
    options = PackageConfig.generate_options()
    default_options = PackageConfig.generate_default_options()

    def _verify_options(self, stage):
        print("======== begin-stage {} ===========".format(stage))
        for k, v in self.options.items():
            print("self.options {} = {}".format(k, v))
        print("======== end-stage {} ===========".format(stage))

    def requirements(self):
        # XXX newer versions blowup on Android due to hid linking issue
        self.requires.add("sdl2/2.0.8@bincrafters/stable")

    def source(self):
        tag = "0.16.0"
        upstream = "https://github.com/libSDL2pp/libSDL2pp.git"
        self.run("rm -rf %s" % self._source_subfolder)
        self.run("git clone --branch %s  -- %s %s" %
                 (tag, upstream, self._source_subfolder))
        tools.patch(base_path=self._source_subfolder, patch_file="cmake.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
        # CONAN_INSTALL_FOLDER is necessary for our nested project style
        # workaround. Otherwise we can't find the conan definitions.
        #
        # Ignore JEDI complaining that the install_folder variable doesn't
        # exist, it will at runtime.
        cmake.definitions['CONAN_INSTALL_FOLDER'] = self.install_folder
        PackageConfig.populate_cmake_configuration(self.options, cmake)
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        if self.options.with_tests:
            cmake.test()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install(build_dir=self._build_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["SDL2pp"]
