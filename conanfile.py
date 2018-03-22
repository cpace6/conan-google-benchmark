from conans import ConanFile, CMake, tools
import os, shutil

class GooglebenchmarkConan(ConanFile):
    name = "google-benchmark"
    version = "1.3.0"
    license = "https://github.com/raulbocanegra/conan-google-benchmark"
    url = "https://github.com/raulbocanegra/conan-google-benchmark"
    description = "A library to support the benchmarking of functions, similar to unit-tests."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        zip_name = "v%s.zip" % self.version        
        url = "https://github.com/google/benchmark/archive/%s" % zip_name
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        shutil.move("benchmark-%s" % self.version, "benchmark")
        tools.replace_in_file("benchmark/CMakeLists.txt", "project (benchmark)", '''project (benchmark)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()''')        
        os.unlink(zip_name)        
        
    def build_requirements(self):
        self.build_requires("gtest/1.8.0@bincrafters/stable")    
    
    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="benchmark")
        cmake.build()
        print("build=%s"%self.build_folder)
    def package(self):
        self.copy("*.h", dst="include", src="benchmark/include", keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["benchmark"]
