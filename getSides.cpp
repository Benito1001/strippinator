#include <iostream>
#include <chrono>
#include <tuple>
#include <gdk-pixbuf/gdk-pixbuf.h>

using namespace std;


struct ImgData {
	guchar *pixels;
	int w, h, stride, channels;

	tuple<int, int, int> getColor(size_t x, size_t y) {
		size_t pos = x*channels + y*stride;
		int r = (int) pixels[pos];
		int g = (int) pixels[pos + 1];
		int b = (int) pixels[pos + 2];

		return tuple<int, int, int>(r, g, b);
	}

	int getColorSum(size_t x, size_t y) {
		auto [r, g, b] = getColor(x, y);
		return r+g+b;
	}
};


int getTop(int w, int h, ImgData &imgData) {
	for (size_t y = 0; y < h; y++) {
		for (size_t x = 0; x < w; x++) {
			if (imgData.getColorSum(x, y) != 255*3) {
				return y;
			}
		}
	}
}

int getBottom(int w, int h, ImgData &imgData) {
	for (size_t y = h - 1; y >= 0; y--) {
		for (size_t x = 0; x < w; x++) {
			if (imgData.getColorSum(x, y) != 255*3) {
				return y;
			}
		}
	}
}

int getLeft(int w, int h, ImgData &imgData) {
	for (size_t x = 0; x < w; x++) {
		for (size_t y = 0; y < h; y++) {
			if (imgData.getColorSum(x, y) != 255*3) {
				return x;
			}
		}
	}
}

int getRight(int w, int h, ImgData &imgData) {
	for (size_t x = w - 1; x >= 0; x--) {
		for (size_t y = 0; y < h; y++) {
			if (imgData.getColorSum(x, y) != 255*3) {
				return x;
			}
		}
	}
}

extern "C" void getSides(char* filename, int *topy, int *bottomy, int *leftx, int *rightx) {
	GError *error = nullptr;
	GdkPixbuf *pix = gdk_pixbuf_new_from_file(filename, &error);

	int w = gdk_pixbuf_get_width(pix);
	int h = gdk_pixbuf_get_height(pix);
	int stride = gdk_pixbuf_get_rowstride(pix);
	int channels = gdk_pixbuf_get_n_channels(pix);

	guchar *pixels =  gdk_pixbuf_get_pixels(pix);
	ImgData imgData{pixels, w, h, stride, channels};

	*topy = getTop(w, h, imgData);
	*bottomy = getBottom(w, h, imgData) + 1;
	*leftx = getLeft(w, h, imgData);
	*rightx = getRight(w, h, imgData) + 1;
}
