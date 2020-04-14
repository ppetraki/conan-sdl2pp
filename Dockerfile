FROM ubuntu:18.04
USER root
RUN apt-get update -qq
RUN apt install sudo

COPY . conan-sdl2pp/
WORKDIR "/conan-sdl2pp"
ENV CONAN_DOCKER_IMAGE=1
RUN sudo ./bootstrap.sh && make package-install
