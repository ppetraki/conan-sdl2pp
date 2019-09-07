# conan sdl2pp package

C++11 bindings/wrapper for SDL2

https://sdl2pp.amdmi3.ru

### TODO
- only drive test_package with the optional flags used in the parent build
- only static libs work on arm. Dynamic libs somehow lose all of their transitive deps
- prevent package-install from running the test_package during a cross build
- add a table of options
