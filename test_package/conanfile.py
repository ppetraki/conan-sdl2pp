#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            with tools.vcvars(self.settings, filter_known_paths=False):
                self.build_cmake()
        else:
            self.build_cmake()

    def build_cmake(self):
        flags = {}
        if (os.environ.get('CONAN_DOCKER_IMAGE')):
            flags['CONAN_DOCKER_IMAGE'] = 1

        cmake = CMake(self)
        cmake.configure(defs=flags)
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "test_package")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_path))
