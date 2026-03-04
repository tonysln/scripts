import glob
import os
import sys


assert len(sys.argv) > 1
folder = sys.argv[1]
print('Running on path:', folder)

for ext in ['*.JPG', '*.jpeg', '*.JPEG']:
	for file in glob.glob(os.path.join(folder, ext)):
		os.rename(file, file.removesuffix(ext[1:]).lower() + '.jpg')

print('Done.')
