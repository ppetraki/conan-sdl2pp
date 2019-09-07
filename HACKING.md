Then you need to use either cmake paths or cmake find package generator
ppetraki 4:34 AM
which is why it works on the host fine because I have it exposed through the regular search paths + pkg-config
tomskside:bincrafters: 4:34 AM
First one just appends directories to the cmake find root path
Second generates its own find files
For pkg config, there is another generator
ppetraki 4:35 AM
the first option sounds right
tomskside:bincrafters: 4:35 AM
Yeah, check out the docs and try it out
As long as sdl2 exports find files it will work I believe
