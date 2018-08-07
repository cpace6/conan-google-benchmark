from conans import ConanFile, CMake, tools

class GoogleBenchmarkConan(ConanFile):
    name = "google-benchmark"
    version = "1.4.1"
    settings = "arch", "build_type", "compiler", "os"
    generators = "cmake"
    url = "http://github.com/cpace6/conan-google-benchmark"
    source_root = "benchmark-1.4.1"
    license = "https://github.com/google/benchmark/blob/master/LICENSE"

    def source(self):
        zip_name = "v%s.zip" % self.version
        url = "https://github.com/google/benchmark/archive/%s" % zip_name
        tools.download(url, zip_name)
        tools.unzip(zip_name)
        tools.replace_in_file('{:s}/src/CMakeLists.txt'.format(self.source_root),
                              'if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")\n  target_link_libraries(benchmark Shlwapi)\nendif()',
                              'if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")\n  target_link_libraries(benchmark Shlwapi)\nelse()\n if(NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")\n  find_library(LIB_RT rt)\n  target_link_libraries(benchmark ${LIB_RT})\n endif()\nendif()')
        self.run("find %s -name '*.py' -exec chmod u+x {} \\;" % self.source_root)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BENCHMARK_ENABLE_GTEST_TESTS"]="OFF"
        cmake.configure(source_folder=self.source_root)
        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.source_root, keep_path=True)
        self.copy(pattern="*.a", dst="lib", src=".", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["benchmark"]
