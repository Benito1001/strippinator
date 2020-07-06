import os
import sys
import time
import ctypes
import PIL.Image as image

def get_new_fraction(width, left, right, fraction):
	new_width = width - (left+right)
	if fraction <= 0.5:
		return (width*fraction - left) / new_width
	else:
		return 1 - (width*(1-fraction) - right) / new_width

def get_padding(width, fraction):
	if fraction <= 0.5:
		return "left", width*(1 - 2*fraction)
	else:
		return "right", width*(2*fraction - 1)

def get_new_padding(width, left, right, fraction):
	new_fraction = get_new_fraction(width, left, right, fraction)
	return get_padding(width - (left+right), new_fraction)

def stripImg(img, filename, keep_name=False, center=True, center_frac=None):
	w, h = img.size

	getSides = ctypes.CDLL('./getSides.so')
	topy, bottomy, leftx, rightx = (ctypes.c_int(0) for i in range(4))
	getSides.getSides(ctypes.byref(topy), ctypes.byref(bottomy), ctypes.byref(leftx), ctypes.byref(rightx))
	topy, bottomy, leftx, rightx = topy.value, bottomy.value, leftx.value, rightx.value

	if center_frac is not None:
		if center:
			dir, padding = get_new_padding(w, leftx, w - rightx, center_frac)
			if dir == "left":
				leftx -= int(padding)
			else:
				rightx += int(padding)

		new_img = image.new('RGB', (rightx - leftx, bottomy - topy), (255, 255, 255))
		new_img.paste(img, (-leftx, -topy))
	else:
		new_img = img.crop([0, topy, w, bottomy])

	if keep_name:
		new_img.save(filename)
	else:
		name, extension = filename.split(".")
		new_img.save(f"{name}-stripped.{extension}")

center_frac = None
center = True
keep_name = False
args = sys.argv[1:]
for arg in args[:]:
	if arg.startswith("--"):
		if "--crop-sides" in arg:
			if center_frac is None:
				center_frac = 0.5
		if "--no-center" in arg:
			center = False
			center_frac = 0.5
		elif "--center-frac" in arg:
			center_frac = float(arg.split("=")[1])
		elif "--keep-name" in arg:
			keep_name = True
		args.remove(arg)

if len(args) == 0:
	pass
elif args[0] == "all":
	for file in os.listdir():
		if not os.path.isdir(file):
			filetype = file.split(".")[-1].upper()
			if filetype == "PNG" or filetype == "JPG" or filetype == "JPEG":
				img = image.open(file)
				stripImg(img, file, keep_name, center, center_frac)
else:
	for file in args:
		img = image.open(file)
		stripImg(img, file, keep_name, center, center_frac)
