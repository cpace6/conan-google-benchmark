#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class GooglebenchmarkConan(ConanFile):
    name = "google-benchmark"
    version = "1.3.0"
    description = "A library to support the benchmarking of functions, similar to unit-tests."
    url = "https://github.com/raulbocanegra/conan-google-benchmark"
    homepage = "https://github.com/google/benchmark"
    # Indicates License type of the packaged library
    license = "https://github.com/raulbocanegra/conan-google-benchmark"
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        #zip_name = "v%s.zip" % self.version        
        #source_url = "https://github.com/google/benchmark/archive/%s" % zip_name
        source_url = "https://github.com/google/benchmark"
        tools.get("{0}/archive/v{1}.zip".format(source_url, self.version))
        extracted_dir = "benchmark-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

        #tools.download(url, zip_name)
        #tools.unzip(zip_name)
        #shutil.move("benchmark-%s" % self.version, "benchmark")
        #tools.replace_in_file("benchmark/CMakeLists.txt", "project (benchmark)", '''project (benchmark)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()''')
        #os.unlink(zip_name)        
        
    def configure_cmake(self):
        cmake = CMake(self)
        #cmake.definitions["BUILD_TESTS"] = False # example
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        else:
            self.build_subfolder = os.path.join("c:\\", "build_google_test")
            print(self.build_subfolder)
                        
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build_requirements(self):
        self.build_requires("gtest/1.8.0@bincrafters/stable")    
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        
    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self.source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
         #self.cpp_info.libs = ["benchmark"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("Shlwapi")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")