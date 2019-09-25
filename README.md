# conan sdl2pp package

C++11 bindings/wrapper for SDL2

https://sdl2pp.amdmi3.ru

### Available Package Options
| Option        | Default | Possible Values  | Description
|:------------- |:-----------------  |:----------------- |:------------|
|cxxstd    | c++11 |  ANY | Used c++ standard |
|static    | True |  [True, False] | Build static library instead of shared one |
|with_image    | False |  [True, False] | Enable SDL2_image support |
|with_mixer    | False |  [True, False] | Enable SDL2_ttf support |
|with_ttf    | False |  [True, False] | Enable SDL2_mixer support |
|with_tests    | False |  [True, False] | Build tests |
|with_examples    | False |  [True, False] | Build examples |
|enable_livetests    | False |  [True, False] | Enable live tests (require X11 display and audio device) |

### TODO
- only drive test_package with the optional flags used in the parent build
- only static libs work on arm. Dynamic libs somehow lose all of their transitive deps
