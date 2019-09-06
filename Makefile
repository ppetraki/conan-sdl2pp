PROJECT_NAME:=sdl2pp
PROJECT_VERSION:=0.16.0

PROFILE:=
CHANNEL:=ppetraki
SRC_FOLDER:=tmp/source
BUILD_FOLDER:=tmp/build
INSTALL_FOLDER:=$(BUILD_FOLDER)
PACKAGE_FOLDER:=tmp/package

all: clean source install build package

clean:
	rm -rf tmp

source:
	conan source . --source-folder=$(SRC_FOLDER)

install:
	conan install  . --install-folder=$(INSTALL_FOLDER)

build:
	conan build . --source-folder=$(SRC_FOLDER) --build-folder=$(BUILD_FOLDER)

package:
	conan package . -sf=$(SRC_FOLDER) -bf=$(BUILD_FOLDER) -pf=$(PACKAGE_FOLDER)

export-package:
	conan export-pkg . $(CHANNEL)/$(PROJECT_NAME) -f --source-folder=$(SRC_FOLDER) \
		--build-folder=$(BUILD_FOLDER) $(PROFILE)

test: export-package
	conan test test_package $(PROJECT_NAME)/$(PROJECT_VERSION)@$(CHANNEL)/$(PROJECT_NAME)


# when you're satisfied that the package is correct, install it for real
package-install: package-uninstall
	conan create   . $(CHANNEL)/$(PROJECT_NAME) -s build_type=Release
	conan create   . $(CHANNEL)/$(PROJECT_NAME) -s build_type=Debug

package-uninstall:
	# always exit with success because you could have removed
	# it manually ahead of time which will cause package-install to
	# fail as this dependent rule will fail first
	conan remove -f $(PROJECT_NAME)/$(PROJECT_VERSION)@$(CHANNEL)/$(PROJECT_NAME) || :
