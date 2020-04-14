#!/bin/bash
apt update -qq
apt install -y python3-pip  python3-yaml cmake git make ninja-build

pip3 install conan --upgrade
pip3 install conan_package_tools bincrafters_package_tools

conan profile new default --detect || :
conan profile update settings.compiler.libcxx=libstdc++11 default
conan remote remove bincrafters || :
conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
