# pip install ExifRead

import glob
import sys
import os
import exifread
import shutil
import datetime
import exiftool
import pprint

if len(sys.argv) != 3:
	print("python movie_organize.py input_dir output_dir")
	exit(1)

print("input dir: " + sys.argv[1])
print("output dir: " + sys.argv[2])

inDirPath = sys.argv[1];
outDirPath = sys.argv[2];

filesList = glob.glob(inDirPath + '/**/*', recursive=True)
moviesList = []
metadataByFile = {}

for filePath in filesList:

	filename = os.path.basename(filePath)
	if filename.endswith(".mp4") or filename.endswith(".mov") or filename.endswith(".avi"):
		#moviesList.append(filePath)
		with exiftool.ExifTool() as et:
			metadataByFile[filePath] = et.get_metadata_batch([filePath])


#pprint.pprint(metadataByFile)

for filePath in metadataByFile:

	meta = metadataByFile[filePath][0]
	filename = os.path.basename(filePath)
	#print(meta)

	date = meta.get("QuickTime:CreateDate", "noDate")
	if date == "noDate":
		date = meta.get("QuickTime:CreateDate", "noDate")

	if date == "noDate":
		os.makedirs(str(outDirPath + "/" + date), exist_ok=True)
		nefFolderName = date
		nefOutputPath = outDirPath + "/" + date + "/" + filename
	else:
		try:
			date_time_obj = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
		except Exception as exc:
			print("invalid date? " + date + " for file " + filePath)
			date_time_obj = None

		if date_time_obj is None:
			nefFolderName = "noDate"
		else:
			nefFolderName = date_time_obj.strftime("%Y/%B/%d")


	# create dir in year / month / dat format
	os.makedirs(str(outDirPath + "/" + nefFolderName), exist_ok=True)
	nefOutputPath = outDirPath + "/" + nefFolderName + "/" + filename

	print("Copying file to " + nefOutputPath)

	shutil.copyfile(filePath, nefOutputPath)



