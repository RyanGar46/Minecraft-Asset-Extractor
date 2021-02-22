import json, os, platform, shutil, sys, multiprocessing, time
from zipfile import ZipFile
from pathlib import Path
from threading import Thread
import array as arr

OUTPUT_PATH = ""
PACK_NAME = ""
MC_VERSION = ""
SNAPSHOT = ""
SNAPSHOT_BOOL = False
PACK_PNG = ""
CUSTOM_PACK_PNG = False
DESCRIPTION = ""
MC_PACK = ""
AUTO_PACK = False
SOUNDS = False
LANGBOOL = False
ZIP_FILES = False
COMPATIBILITY = False
CLEAR = False
DELETE = False

completed = 0

def Clear(clear):
	if clear == True:
		os.system("cls")

def ExtractStart(outPath, packName, version, snapshot, snapshotBool, packPNG, customPackPNG, Description, pack, autoPack, sounds, langBool, zipFiles, compatibility, clear, delete):
	global OUTPUT_PATH, PACK_NAME, MC_VERSION, SNAPSHOT, SNAPSHOT_BOOL, PACK_PNG, CUSTOM_PACK_PNG, DESCRIPTION, MC_PACK, AUTO_PACK, SOUNDS, LANGBOOL, ZIP_FILES, COMPATIBILITY, CLEAR, DELETE

	OUTPUT_PATH = outPath
	PACK_NAME = packName
	MC_VERSION = version
	SNAPSHOT = snapshot
	SNAPSHOT_BOOL = snapshotBool
	PACK_PNG = packPNG
	CUSTOM_PACK_PNG = customPackPNG
	DESCRIPTION = Description
	MC_PACK = pack
	AUTO_PACK = autoPack
	SOUNDS = sounds
	LANGBOOL = langBool
	ZIP_FILES = zipFiles
	COMPATIBILITY = compatibility
	CLEAR = clear
	DELETE = delete

	thread = Thread(target = Extract, args = (0,))
	thread.start()

def ExtractOBJ(args, src, dest):
	os.makedirs(os.path.dirname(dest), exist_ok=True)
	shutil.copyfile(src, dest)

def ExtractJAR(args, zip, file):
	global completed
	os.makedirs(os.path.dirname(f"{OUTPUT_PATH}\\{PACK_NAME}\\{file}"), exist_ok=True)
	try:
		zip.extract(file, os.path.normpath(f"{OUTPUT_PATH}\\{PACK_NAME}"))
	except:
		None
	completed += 1

def getListOfFiles(dirName):
	# create a list of file and sub directories 
	# names in the given directory 
	listOfFile = os.listdir(dirName)
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFile:
		# Create full path
		fullPath = os.path.join(dirName, entry)
		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)
				
	return allFiles
	
# This is a heavly modified version of https://minecraft.gamepedia.com/Tutorials/Sound_directory.
def Extract(args):
	global OUTPUT_PATH, PACK_NAME, MC_VERSION, SNAPSHOT, SNAPSHOT_BOOL, PACK_PNG, CUSTOM_PACK_PNG, DESCRIPTION, MC_PACK, AUTO_PACK, SOUNDS, LANGBOOL, ZIP_FILES, COMPATIBILITY, CLEAR, DELETE

	Clear(CLEAR)

	MC_VERSION_SNAPSHOT = MC_VERSION

	if SNAPSHOT_BOOL:
		MC_VERSION_SNAPSHOT = SNAPSHOT

	if PACK_NAME.replace(" ", "") == "":
		PACK_NAME = "Minecraft Resources"

	# Finds the pack format that matches with the selected version.
	if AUTO_PACK == True:
		if int(MC_VERSION.split(".")[1]) >= 17:
			MC_PACK = 7
		elif int(MC_VERSION.split(".")[1]) == 16:
			if int(MC_VERSION.split(".")[2]) >= 2:
				MC_PACK = 6
			else:
				MC_PACK = 5
		elif int(MC_VERSION.split(".")[1]) >= 15:
			MC_PACK = 5
		elif int(MC_VERSION.split(".")[1]) >= 13:
			MC_PACK = 4
		elif int(MC_VERSION.split(".")[1]) >= 11:
			MC_PACK = 3
		elif int(MC_VERSION.split(".")[1]) >= 9:
			MC_PACK = 2
		elif int(MC_VERSION.split(".")[1]) >= 7:
			MC_PACK = 1
		elif int(MC_VERSION.split(".")[1]) >= 6:
			if int(MC_VERSION.split(".")[2]) == 1:
				MC_PACK = 1

	if SOUNDS == True:
		SOUND = "s";
	else:
		SOUND = "null"

	if LANGBOOL == True:
		LANG = "l";
	else:
		LANG = "null"

	REAL_OUTPUT_PATH = OUTPUT_PATH

	if ZIP_FILES == True and DELETE == True:
		OUTPUT_PATH = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "temp\\")

	Clear(CLEAR)
	if platform.system() == "Windows":
		MC_ASSETS = os.path.expandvars("%APPDATA%\\.minecraft\\assets")
		MC_VERSION_JAR = os.path.expandvars(f"%APPDATA%\\.minecraft\\versions\\{MC_VERSION_SNAPSHOT}\\{MC_VERSION_SNAPSHOT}.jar")
	else:
		MC_ASSETS = os.path.expanduser("~\\.minecraft\\assets")
		MC_VERSION_JAR = os.path.expanduser(f"~\\.minecraft\\versions\\{MC_VERSION_SNAPSHOT}\\{MC_VERSION_SNAPSHOT}.jar")

	# Compatibility fixes
	if COMPATIBILITY == True:
		if int(MC_VERSION.split(".")[1]) == 13:
			MC_OBJECT_INDEX = f"{MC_ASSETS}/indexes/1.13.1.json"
		elif int(MC_VERSION.split(".")[1]) >= 8:
			MC_OBJECT_INDEX = f"""{MC_ASSETS}/indexes/{MC_VERSION.split(".")[0]}.{MC_VERSION.split(".")[1]}.json"""
		elif int(MC_VERSION.split(".")[1]) == 7:
			MC_OBJECT_INDEX = f"""{MC_ASSETS}/indexes/{MC_VERSION}.json"""
		else:
			MC_OBJECT_INDEX = f"{MC_ASSETS}/indexes/legacy.json"
	else:
		MC_OBJECT_INDEX = f"""{MC_ASSETS}/indexes/{MC_VERSION.split(".")[0]}.{MC_VERSION.split(".")[1]}.json"""

	# Where the unextracted asset files are.
	MC_OBJECTS_PATH = f"{MC_ASSETS}/objects"
	# How it finds out weather it is an asset or somthing else.
	MC_SOUNDS = r"minecraft/"

	Clear(CLEAR)

	# Opens the .jar
	with ZipFile(MC_VERSION_JAR, 'r') as zip:
		# Get a list of all archived file names from the zip
		listOfFileNames = zip.namelist()
	
		length = 0
		current = 0

		for fileName in listOfFileNames:
			if fileName.startswith("assets"):
				if len(fileName.split("/")) >= 6:
					if fileName.split("/")[5] != "background":
						length += 1
				else:
					length += 1

		global completed

		# Iterate over the file names
		for fileName in listOfFileNames:
			if fileName.startswith("assets"):
				if len(fileName.split("/")) >= 6:
					if fileName.split("/")[5] != "background":
						current += 1
						print("Extracting .jar Progress: " + str(format(round(100 * (current / length), 2), '.2f')) + "%")
						
						# finds out what thread to use.
						currentThread = round((os.cpu_count() - 2) * (current / length)) + 1

						# Copy the file
						threadJAR = Thread(target = ExtractJAR, args = (currentThread, zip, fileName))
						threadJAR.start()
				else:
					current += 1
					print("Extracting .jar Progress: " + str(format(round(100 * (current / length), 2), '.2f')) + "%")
						
					# finds out what thread to use.
					currentThread = round((os.cpu_count() - 2) * (current / length)) + 1

					# Copy the file
					threadJAR = Thread(target = ExtractJAR, args = (currentThread, zip, fileName))
					threadJAR.start()

		while completed != current:
			time.sleep(0.1)

	if os.path.exists(os.path.normpath(f"{OUTPUT_PATH}/{PACK_NAME}\\assets\\.mcassetsroot")):
		os.remove(os.path.normpath(f"{OUTPUT_PATH}/{PACK_NAME}\\assets\\.mcassetsroot"))

	Clear(CLEAR)

	# Handles files that are not in .jar
	with open(MC_OBJECT_INDEX, "r") as read_file:
		# Parse the JSON file into a dictionary
		data = json.load(read_file)

		# Find each line with MC_SOUNDS prefix, remove the prefix and keep the rest of the path and the hash
		sounds = {k[len(MC_SOUNDS):] : v["hash"] for (k,v) in data["objects"].items() if k.startswith(MC_SOUNDS)}

		length = 0
		current = 0

		if SOUNDS and LANGBOOL:
			print("Extracting Sounds And Languages.")
		elif not SOUNDS and LANGBOOL:
			print("Extracting Languages.")
		elif SOUNDS and not LANGBOOL:
			print("Extracting Sounds.")

		for fpath, fhash in sounds.items():
			if fpath[0] == SOUND or fpath[0] == "t" or fpath[0] == LANG:
				length += 1

		for fpath, fhash in sounds.items():
			if fpath[0] == SOUND or fpath[0] == "t" or fpath[0] == LANG:
				current += 1

				if SOUNDS and LANGBOOL:
					print("Extracting Sounds And Languages Progress: " + str(format(round(100 * (current / length), 1), '.2f')) + "%")
				elif not SOUNDS and LANGBOOL:
					print("Extracting Languages Progress: " + str(format(round(100 * (current / length), 1), '.2f')) + "%")
				elif SOUNDS and not LANGBOOL:
					print("Extracting Sounds Progress: " + str(format(round(100 * (current / length), 1), '.2f')) + "%")

				src_fpath = os.path.normpath(f"{MC_OBJECTS_PATH}/{fhash[:2]}/{fhash}")
				dest_fpath = os.path.normpath(f"{OUTPUT_PATH}/{PACK_NAME}/assets/minecraft/{fpath}")

				# finds out what thread to use.
				if current < os.cpu_count():
					current += 1
				else:
					current = 1
			
				currentThread = current

				# Copy the file
				threadOBJ = Thread(target = ExtractOBJ, args = (currentThread, src_fpath, dest_fpath))
				threadOBJ.start()

	if CUSTOM_PACK_PNG == False or CUSTOM_PACK_PNG == None or PACK_PNG.replace(" ", "") == "":
		PACK_PNG = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "pack.png")
	
	os.makedirs(os.path.dirname(f"{OUTPUT_PATH}\\{PACK_NAME}"), exist_ok=True)

	# Data to be written 
	dictionary ={
	"pack": {
		"pack_format": int(MC_PACK),
		"description": DESCRIPTION
	}
}

	# Serializing json  
	json_object = json.dumps(dictionary, indent = 3)

	# Creates json file
	with open(f"{OUTPUT_PATH}\\{PACK_NAME}\\pack.mcmeta", "w") as outfile:
		outfile.write(json_object)

	shutil.copyfile(PACK_PNG, os.path.normpath(f"{OUTPUT_PATH}/{PACK_NAME}/pack.png"))

	print(f"Extracted All Assets To {OUTPUT_PATH}{PACK_NAME} ")

	if ZIP_FILES == False:
		print("Finished.")
	else:
		Clear(CLEAR)

		print(f"Ziping {OUTPUT_PATH}{PACK_NAME}...")

		files = getListOfFiles(os.path.normpath(f"{OUTPUT_PATH}\{PACK_NAME}"))

		current = 0
		length = len(files)

		try:
			shutil.rmtree(os.path.normpath(f"{OUTPUT_PATH}\\{PACK_NAME}.zip"))
		except:
			None

		zip = ZipFile(os.path.normpath(f"{OUTPUT_PATH}\\{PACK_NAME}.zip"),"a")

		for file in files:
			current += 1
			print(str(format(round(100 * (current / length), 2), '.2f')) + "%")

			zip.write(file, arcname=f"{file.replace(os.path.normpath(f'{OUTPUT_PATH}//{PACK_NAME}'), '')}")
		
		zip.close()

		print(f"Zipped {REAL_OUTPUT_PATH}{PACK_NAME}.zip")

		Clear(CLEAR)

		if DELETE:
			print("Cleaning Temp Files...")
			shutil.rmtree(os.path.normpath(f"{OUTPUT_PATH}\\{PACK_NAME}"))

		print("Finished.")
