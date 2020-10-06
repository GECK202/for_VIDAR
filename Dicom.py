import pydicom
import numpy as np
import sys
import glob
from PIL import Image

# load the DICOM files
files = []
print('glob: {}'.format(sys.argv[1]))
for fname in glob.glob(sys.argv[1], recursive=False):
	print("loading: {}".format(fname))
	files.append(pydicom.dcmread(fname))

print("file count: {}".format(len(files)))

# skip files with no SliceLocation (eg scout views)
slices = []
skipcount = 0
for f in files:
	if hasattr(f, 'SliceLocation'):
		slices.append(f)
	else:
		skipcount = skipcount + 1

# ensure they are in the correct order
slices = sorted(slices, key=lambda s: s.SliceLocation)

img_shape = list(slices[0].pixel_array.shape)
for k, s in enumerate(slices):
	img2d = s.pixel_array
	img2d = img2d & 0xff
	img2d = img2d.astype('uint8')
	i_shape = img2d.shape
	img2d = np.concatenate((img2d, img2d, img2d), axis=1)
	img2d = np.reshape(img2d, (i_shape[0], i_shape[1], 3), order='F')
	pil_img = Image.fromarray(img2d)
	pil_img.save('png_image/'+str(k)+'.png')
	print(k)
