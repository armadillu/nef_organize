# pip install ExifRead

import glob
import sys
import random
import os
import subprocess
import exifread
import shutil
import datetime

if len(sys.argv) != 3:
	print("python nef_organize.py input_dir output_dir")
	exit(1)

print("input dir: " + sys.argv[1])
print("output dir: " + sys.argv[2])

inDirPath = sys.argv[1];
outDirPath = sys.argv[2];

filesList = glob.glob(inDirPath + '/**/*', recursive=True)


for filePath in filesList:

	filename = os.path.basename(filePath)
	if filename.endswith(".nef") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".mp4"):

		print("### " + filename + " ####################")
		nefFile = open(filePath, 'rb')
		try:
			exifData = exifread.process_file(nefFile)
		except Exception as exc:
			print("Cant parse exif for " + filename + "; skipping")
			continue

		print(exifData)

		#cameraID = str(exifData.get("Image Model"))
		date = str(exifData.get("EXIF DateTimeOriginal", "Unknown_Date")) #try get a date from file

		if date == "Unknown_Date":
			os.makedirs(str(outDirPath + "/" + date), exist_ok=True)
			nefFolderName = date
			nefOutputPath = outDirPath + "/" + date + "/" + filename
		else:
			try:
				date_time_obj = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
			except Exception as exc:
				print("invalid date? " + date)
				date_time_obj = None

			if date_time_obj is None:
				nefFolderName = "Unknown_Date"
			else:
				nefFolderName = date_time_obj.strftime("%Y/%B/%d")


		# create dir in year / month / dat format
		os.makedirs(str(outDirPath + "/" + nefFolderName), exist_ok=True)
		nefOutputPath = outDirPath + "/" + nefFolderName + "/" + filename

		print("Copying file to " + nefOutputPath)

		shutil.copyfile(filePath, nefOutputPath)



