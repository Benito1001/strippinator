getSides.so: getSides.cpp
	g++ $^ -o $@ -shared -fPIC -std=c++17 -O3 -ffast-math -funsafe-math-optimizations $(shell pkg-config --cflags --libs gdk-pixbuf-2.0)
