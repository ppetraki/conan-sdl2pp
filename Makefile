PROJECT_NAME:=sdl2pp
PROJECT_VERSION:=0.16.0

#_PROFILE:=-pr arm2
PROFILE:=$(_PROFILE)

CHANNEL:=ppetraki
RELEASE:=testing
SRC_FOLDER:=tmp/source
BUILD_FOLDER:=tmp/build
INSTALL_FOLDER:=$(BUILD_FOLDER)
PACKAGE_FOLDER:=tmp/package

# Cross building can be irritating
# https://github.com/conan-io/conan/issues/2355
ifneq ($(_PROFILE),)
	SKIP_TEST:=-tf None
endif

all: clean source install build package

clean:
	rm -rf tmp

source:
	conan source . --source-folder=$(SRC_FOLDER)

install:
	conan install  . --install-folder=$(INSTALL_FOLDER) $(PROFILE)

build:
	conan build . --source-folder=$(SRC_FOLDER) --build-folder=$(BUILD_FOLDER)

package:
	conan package . -sf=$(SRC_FOLDER) -bf=$(BUILD_FOLDER) -pf=$(PACKAGE_FOLDER)

export-package:
	conan export-pkg . $(CHANNEL)/$(PROJECT_NAME) -f --source-folder=$(SRC_FOLDER) \
		--build-folder=$(BUILD_FOLDER) $(PROFILE)

test: export-package
	conan test test_package $(PROJECT_NAME)/$(PROJECT_VERSION)@$(CHANNEL)/$(RELEASE)

# when you're satisfied that the package is correct, install it for real
package-install: package-uninstall
	conan create . $(CHANNEL)/$(RELEASE) $(SKIP_TEST) --build=outdated  -s build_type=Release $(PROFILE)
	conan create . $(CHANNEL)/$(RELEASE) $(SKIP_TEST) --build=outdated  -s build_type=Debug  $(PROFILE)

package-uninstall:
	# always exit with success because you could have removed
	# it manually ahead of time which will cause package-install to
	# fail as this dependent rule will fail first
	conan remove -f $(PROJECT_NAME)/$(PROJECT_VERSION)@$(CHANNEL)/$(RELEASE) || :

format:
	autopep8 -i conanfile.py

table:
	python3 -c "import conanfile; conanfile.PackageConfig().output_markdown_table()"
