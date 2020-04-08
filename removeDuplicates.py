# pip install Pillow
# pip install numpy

import glob
import sys
from PIL import Image
import pprint
import os
import numpy



def mse(imageA, imageB):
	err = numpy.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

##########################

if len(sys.argv) != 2:
	print("python removeDuplicates.py directory_with_jpgs")
	exit(1)


print("input dir: " + sys.argv[1])

inDirPath = sys.argv[1];

fileList = glob.glob(inDirPath + '/**/*.jpg', recursive=True)

allImages = {}

# first pass, load all images, index them by aspect ratio. we will only
# loop for duplicates within images of the same aspect ratio the goal here
# is find duplicates of the same image at different sizes

for imgFile in fileList:

	try:
		#print("trying " + jpegFile + " ...")
		img = Image.open(imgFile)
		img.verify()
	except (IOError, SyntaxError) as e:
		print('Bad file:' + imgFile + " " + str(e))
		#os.remove(jpegFile)
		continue

	ar = int(1000 * img.width / img.height) #aspect ratio as an int for indexing based on image aspect ratio
	rar = img.width / img.height

	resizeX = 32
	resizeY = 32

	if (rar >= 1.0): #img is wider than taller
		resizeY = int(resizeY / rar)
	else:
		resizeX = int(resizeX * rar)

	img = Image.open(imgFile) #reopen bc we verified (wtf python!)
	try:
		bwImg = img.convert('L')
	except Exception as e:
		print("cant load data for image " + imgFile)
		continue

	bwThumb = bwImg.resize((resizeX, resizeY));

	np_thumb = numpy.array(bwThumb)
	img.close()

	imgInfo = {}
	imgInfo["width"] = img.width
	imgInfo["height"] = img.height
	imgInfo["aspectRatio"] = ar
	imgInfo["path"] = imgFile
	imgInfo["thumb"] = np_thumb

	if ar not in allImages:
		allImages[ar] = [];

	allImages[ar].append(imgInfo);

# at this point we have all images indexed by aspect ratio; and their thumb
# the next step is to compare each thumb to all other thumbs of the same aspect ratio
# and see if they are equal or not

print("found " + str(len(allImages)) + " aspect ratios")
pprint.pprint(allImages.keys())


for ar in allImages: # for each AR cluster, list all images

	numImg = len(allImages[ar])

	for i in range(0, numImg):
		print("########################################################################################################")
		for j in range(0, numImg):
			if(i != j):
				mseErr = mse(allImages[ar][i]["thumb"], allImages[ar][j]["thumb"])
				print("mse " + os.path.basename(allImages[ar][i]["path"]) + " and " + os.path.basename(allImages[ar][j]["path"]) + " is " + str(mseErr))


