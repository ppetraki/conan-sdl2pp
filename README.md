[![Build Status](https://travis-ci.com/ppetraki/conan-sdl2pp.svg?branch=master)](https://travis-ci.com/ppetraki/conan-sdl2pp)

# conan sdl2pp package

C++11 bindings/wrapper for SDL2

https://sdl2pp.amdmi3.ru

### Available Package Options
| Option        | Default | Possible Values  | Description
|:------------- |:-----------------  |:----------------- |:------------|
|cxxstd    | c++11 |  ANY | Used c++ standard |
|static    | True |  [True, False] | Build static library instead of shared one |
|with_image    | True |  [True, False] | Enable SDL2_image support |
|with_mixer    | True |  [True, False] | Enable SDL2_mixer support |
|with_ttf    | True |  [True, False] | Enable SDL2_ttf support |
|with_tests    | False |  [True, False] | Build tests |
|with_examples    | False |  [True, False] | Build examples |
|enable_livetests    | False |  [True, False] | Enable live tests (require X11 display and audio device) |

### TODO
- fix find module dependencies for ttf extension
- only static libs work on arm. Dynamic libs somehow lose all of their transitive deps
