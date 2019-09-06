#include <SDL2pp/SDL.hh>
#include <SDL2pp/Exception.hh>
#include <SDL2pp/RWops.hh>

#ifdef WITH_IMAGE
#include <SDL2pp/SDLImage.hh>
#endif

#ifdef WITH_MIXER
#include <SDL2pp/SDLMixer.hh>
#endif

#ifdef WITH_TTF
#include <SDL2pp/Font.hh>
#include <SDL2pp/SDLTTF.hh>
#endif

#include <stdexcept>
#include <string>
#include <sstream>
#include <iostream>
#include <cstdlib>

using namespace SDL2pp;

static void throw_exception(const char* message, const char* name) {
  std::stringstream s;
  s << message << " - " << name;
  throw std::runtime_error(s.str().c_str());
}

#ifdef WITH_TTF
static void check_ttf() {
  SDL sdl(SDL_INIT_VIDEO);

  std::cout << "checking font\n";
  SDLTTF sdl_ttf;

  bool found = false;
  auto rwops = RWops::FromFile(TESTDATA_DIR "/Vera.ttf");
  Font font_by_rw(rwops, 30);

  if (font_by_rw.Get()) { found = true; }

  if (!found) { throw_exception("Failed to get font!", "ttf"); }
  std::cout << "OK!" << std::endl;
}
#endif

#ifdef WITH_IMAGE
// this requires drawing to the screen so just test that we can
// resolve the symbol and bring the subsystem online.
static void check_image() {
  SDL  sdl(SDL_INIT_VIDEO);
  bool found = false;

  std::cout << "checking image\n";
  SDLImage image();
  // if we didn't throw we're ok
  found = true;

  if (!found) { throw_exception("Failed to get image!", "image"); }
  std::cout << "OK!" << std::endl;
}
#endif

#ifdef WITH_MIXER
static void check_mixer() {
  SDL  sdl(SDL_INIT_AUDIO);
  bool found = false;
  std::cout << "checking mixer\n";
  SDLImage mixer();
  // if we didn't throw we're ok
  found = true;

  if (!found) { throw_exception("Failed to get mixer!", "mixer"); }
  std::cout << "OK!" << std::endl;
}
#endif

int main(int argc, char* argv[]) try {
  { SDL sdl(); }
#ifdef WITH_IMAGE
  check_image();
#endif

#ifdef WITH_MIXER
  check_mixer();
#endif

#ifdef WITH_TTF
  check_ttf();
#endif

  return EXIT_SUCCESS;
} catch (std::runtime_error& e) {
  std::cout << "FAIL!" << std::endl;
  std::cerr << e.what() << std::endl;
  return EXIT_FAILURE;
}

