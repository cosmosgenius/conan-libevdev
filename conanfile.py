import os
from conans import ConanFile, CMake, tools

def GetBuiltCMakeListsContent():
    content = ""
    export_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.join(
        export_path, "export_source", "BuiltCMakeLists.txt"
    )
    with open(path) as f:
        content = f.read()
    return content

class LibevdevConan(ConanFile):
    name = "libevdev"
    version = "1.9.0"
    license = "X11 license"
    author = "Sharat M R <cosmosgenius@gmail.com"
    url = "https://github.com/cosmosgenius/conan-libpng"
    homepage = "https://www.freedesktop.org/wiki/Software/libevdev/"
    description = "Sharat M R <cosmosgenius@gmail.com>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = ["CMakeLists.txt", "BuiltCMakeLists.txt"]

    _cmake = None
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("libevdev-" + self.version, self._source_subfolder)
        cmake_path = os.path.join(self._source_subfolder, "CMakeLists.txt")
        tools.save(cmake_path, GetBuiltCMakeListsContent())

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["LIBEVDEV_SHARED_LIB"] = self.options.shared
        self._cmake.definitions["LIBEVDEV_STATIC_LIB"] = not self.options.shared
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["lib"]

