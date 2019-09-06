#include <SDL2pp/SDL.hh>
#include <SDL2pp/Exception.hh>
#include <SDL2pp/Font.hh>
#include <SDL2pp/RWops.hh>

#ifdef WITH_TTF
#include <SDL2pp/SDLTTF.hh>
#endif

#include <stdexcept>
#include <string>
#include <sstream>
#include <iostream>
#include <cstdlib>

using namespace SDL2pp;

static void throw_exception(const char * message, const char * name)
{
    std::stringstream s;
    s << message << " - " << name;
    throw std::runtime_error(s.str().c_str());
}

static void check_ttf()
{
    std::cout << "checking font\n";
    SDLTTF sdl_ttf;

    bool found = false;
    auto rwops = RWops::FromFile(TESTDATA_DIR "/Vera.ttf");
    Font font_by_rw(rwops, 30);

    if (font_by_rw.Get()) {
      found = true;
    }

    if (!found)
        throw_exception("Failed to get font!", "ttf");
    std::cout << "OK!" << std::endl;
}

int main(int argc, char* argv[]) try {
  SDL sdl(SDL_INIT_VIDEO | SDL_INIT_AUDIO);

#ifdef WITH_IMAGE
  check_video_driver("x11");
#endif

#ifdef WITH_MIXER
  check_audio_driver("alsa");
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

