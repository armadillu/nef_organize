# pip install Pillow
import glob
import sys
from PIL import Image
import os

if len(sys.argv) != 2:
	print("python jpeg_cleanup.py directory_with_jpgs")
	exit(1)


print("input dir: " + sys.argv[1])

inDirPath = sys.argv[1];

jpegsList = glob.glob(inDirPath + '/**/*.jpg', recursive=True)

for jpegFile in jpegsList:
	try:
		print("trying " + jpegFile + " ...")
		img = Image.open(jpegFile)
		img.verify()
		img.close()
	except (IOError, SyntaxError) as e:
		print('Bad file:' + jpegFile + " " + str(e))
		os.remove(jpegFile)

