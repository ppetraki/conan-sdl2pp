#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import yaml

# Make your package default changes here or on the CLI
# It would be much nicer to provide this as a seperate file but
# alas conan makes this very difficult, even with adding this
# to the exports list.
CONFIG_YAML = """
options:
  cxxstd:
    description: Used c++ standard
    default: c++11
    type: string
    cmake_key: SDL2PP_CXXSTD
  static:
    description: Build static library instead of shared one
    default: true
    type: boolean
    cmake_key: SDL2PP_STATIC
  with_image:
    description: Enable SDL2_image support
    default: true
    type: boolean
    cmake_key: SDL2PP_WITH_IMAGE
  with_mixer:
    description: Enable SDL2_mixer support
    default: true
    type: boolean
    cmake_key: SDL2PP_WITH_MIXER
  with_ttf:
    description: Enable SDL2_ttf support
    default: true
    type: boolean
    cmake_key: SDL2PP_WITH_TTF
  with_tests:
    description: Build tests
    default: false
    type: boolean
    cmake_key: SDL2PP_WITH_TESTS
  with_examples:
    description: Build examples
    default: false
    type: boolean
    cmake_key: SDL2PP_WITH_EXAMPLES
  enable_livetests:
    description: Enable live tests (require X11 display and audio device)
    default: false
    type: boolean
    cmake_key: SDL2PP_ENABLE_LIVE_TESTS
dependencies:
    Linux:
        apt:
            arch:
                x86:    i386
                x86_64: amd64
                armv7:  armhf
                armv8:  arm64
            packages:
                image: libsdl2-image-dev
                mixer: libsdl2-mixer-dev
                ttf:   libsdl2-ttf-dev
            package_format: "{0}:{1}"
        yum:
            arch:
                x86:    i686
                x86_64: x86_64
            packages:
                image: SDL2_image-devel
                mixer: SDL2_mixer-devel
                ttf:   SDL2_ttf-devel
            package_format: "{0}.{1}"
    Android:
        XXX: BuildFromSource
"""

class ConfigItem:
    def parse_options(self):
        if self.conan_type == 'boolean':
            # the value is already a valid boolean
            self.conan_type = [True, False]
        elif self.conan_type == 'int':
            self.default = int(self.default)
            self.conan_type = 'Integer'
        elif self.conan_type == 'float':
            self.default = float(self.default)
            self.conan_type = 'Float'
        elif self.conan_type == 'string':
            self.default = str(self.default)
            self.conan_type = 'ANY'
        else:
            raise Exception("unsupported type: {0}".format(self.conan_type))

    def __init__(self, name, dictionary):
        self.name = name
        self.conan_type = dictionary.get('type')
        self.default = dictionary.get('default')
        self.description = dictionary.get('description')
        self.cmake_key = str(dictionary.get('cmake_key'))
        self.parse_options()

    def __str__(self):
        line_template = '|{0}    | {1} |  {2} | {3} |'
        return line_template.format(self.name, self.default, self.conan_type, self.description)


class PackageConfig(object):
    def load_config(self):
        return yaml.load(CONFIG_YAML, Loader=yaml.FullLoader)

    def generate_options(self):
        options = {}
        for k, v in self.load_config()['options'].items():
            item = ConfigItem(k, v)
            options[k] = item.conan_type
        return options

    def generate_default_options(self):
        default_options = {}
        for k, v in self.load_config()['options'].items():
            item = ConfigItem(k, v)
            default_options[k] = item.default
        return default_options

    def populate_cmake_configuration(self, options, cmake_ref):
        print("enter cmake config")
        for k, v in self.load_config()['options'].items():
            item = ConfigItem(k, v)
            cmake_ref.definitions[item.cmake_key] = item.default

    def get_dependencies(self):
        return self.load_config()['dependencies']

    def output_markdown_table(self):
        header = '''
### Available Package Options
| Option        | Default | Possible Values  | Description
|:------------- |:-----------------  |:----------------- |:------------|'''
        print(header)
        for k, v in self.load_config()['options'].items():
            print(str(ConfigItem(k, v)))


class SDL2ppConan(ConanFile, PackageConfig):
    def __init__(self, *args, **kwargs):
        super(SDL2ppConan, self).__init__(*args, **kwargs)
        self.options = self.generate_options()
        self.default_options = self.generate_default_options()

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
    exports_sources = ['CMakeLists.txt', 'cmake.patch', 'sdl2ttf_path.patch']

    generators = ['cmake']

    _build_subfolder = "build_subfolder"
    _source_subfolder = "source_subfolder"

    settings = "os", "arch", "compiler", "build_type"

    def _verify_options(self, stage):
        print("======== begin-stage {} ===========".format(stage))
        for k, v in self.options.items():
            print("self.options {} = {}".format(k, v))
        print("======== end-stage {} ===========".format(stage))

    def _verify_default_options(self, stage):
        print("======== begin-stage {} ===========".format(stage))
        for k, v in self.default_options.items():
            print("self.default_options {} = {}".format(k, v))
        print("======== end-stage {} ===========".format(stage))

    def _verify_all(self, stage=""):
        self._verify_options(stage)
        self._verify_default_options(stage)

    def requirements(self):
        # XXX newer versions blowup on Android due to hid linking issue
        self.requires.add("sdl2/2.0.8@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            platform = 'Linux'
            package_manager = None

            if tools.os_info.with_apt:
                package_manager = 'apt'
            elif tools.os_info.with_apt:
                package_manager = 'yum'
            else:
                raise 'package_manager has undefined dependencies!'

            package_manager = self.get_dependencies()[platform][package_manager]
            print("using package manager %s" % package_manager)
            packages = []

            if self.options.with_image:
                packages.append(package_manager['packages']['image'])

            if self.options.with_mixer:
                packages.append(package_manager['packages']['mixer'])

            if self.options.with_ttf:
                packages.append(package_manager['packages']['ttf'])

            installer = tools.SystemPackageTool()
            print ("package list {0}".format(packages))
            for p in packages:
                package_format = package_manager['package_format']
                # why do I need to cast to str?
                native_arch    = str(self.settings.arch)
                package_arch   = package_manager['arch'][native_arch]
                installer.install(package_format.format(p, package_arch))
        else:
            print ("dependencies undefined, disabling all extensions!")
            # XXX is this going to stick?
            self.options.with_image = false
            self.options.with_mixer = false
            self.options.with_ttf = false

    def source(self):
        tag = "0.16.0"
        upstream = "https://github.com/libSDL2pp/libSDL2pp.git"
        self.run("rm -rf %s" % self._source_subfolder)
        self.run("git clone --branch %s  -- %s %s" %
                 (tag, upstream, self._source_subfolder))
        tools.patch(base_path=self._source_subfolder, patch_file="cmake.patch")
        tools.patch(base_path=self._source_subfolder, patch_file="sdl2ttf_path.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
        # CONAN_INSTALL_FOLDER is necessary for our nested project style
        # workaround. Otherwise we can't find the conan definitions.
        #
        # Ignore JEDI complaining that the install_folder variable doesn't
        # exist, it will at runtime.
        cmake.definitions['CONAN_INSTALL_FOLDER'] = self.install_folder
        self.populate_cmake_configuration(self.options, cmake)
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
        self.copy("*", dst="cmake", src=self._source_subfolder+"/cmake")

    def package_info(self):
        self.cpp_info.libs = ["SDL2pp"]
