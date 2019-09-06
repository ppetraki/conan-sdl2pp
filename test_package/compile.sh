#!/bin/bash -x
PP_INC=/home/ppetraki/tmp/conan-sdl2pp/tmp/package/include
PP_LIB=/home/ppetraki/tmp/conan-sdl2pp/tmp/package/lib
TD="/home/ppetraki/tmp/conan-sdl2pp/test_package/testdata"

rm -f test_package test_package.cpp.o

/usr/bin/c++ -D_GLIBCXX_USE_CXX11_ABI=1 \
	-DWITH_TTF \
	-DWITH_IMAGE \
	-DWITH_MIXER \
  -DTESTDATA_DIR=\"${TD}\" \
  -I$PP_INC \
  -I/usr/include/SDL2 \
  -m64 -O3 -DNDEBUG  -o test_package.cpp.o -c test_package.cpp


/usr/bin/c++ -m64 -O3 -DNDEBUG -rdynamic  test_package.cpp.o -o test_package  \
  -L$PP_LIB -Wl,-rpath,$PP_LIB  -lSDL2pp -lSDL2 -lSDL2main \
  -ldl -lrt -lpthread -lasound -lm -ldl -lpthread -lrt -ljack \
  -lpthread -lpulse -laudio -ldl -lrt -lasound -lm -ljack -lpulse -laudio \
