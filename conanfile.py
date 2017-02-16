from conans import ConanFile, CMake
from conans.tools import download, unzip, replace_in_file


class GoogleBenchmarkConan(ConanFile):
    name = "google-benchmark"
    version = "1.1.0"
    settings = "arch", "build_type", "compiler", "os"
    generators = "cmake"
    url = "http://github.com/cpace6/conan-google-benchmark"
    source_root = "benchmark-1.1.0"
    license = "https://github.com/google/benchmark/blob/master/LICENSE"

    def source(self):
        zip_name = "v%s.zip" % self.version
        url = "https://github.com/google/benchmark/archive/%s" % zip_name
        download(url, zip_name)
        unzip(zip_name)
        replace_in_file('{:s}/src/CMakeLists.txt'.format(self.source_root),
                              'if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")\n  target_link_libraries(benchmark Shlwapi)\nendif()',
                              'if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")\n  target_link_libraries(benchmark Shlwapi)\nelse()\n if(NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")\n  find_library(LIB_RT rt)\n  target_link_libraries(benchmark ${LIB_RT})\n endif()\nendif()')

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        configure_command = 'cd _build && cmake ../%s %s' % (self.source_root, cmake.command_line)
        self.run(configure_command)
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.source_root, keep_path=True)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["benchmark"]
