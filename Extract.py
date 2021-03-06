import json, os, platform, shutil, sys, multiprocessing, time
from zipfile import ZipFile
from pathlib import Path
from threading import Thread
import array as arr
from PIL import Image

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
SHADERSBOOL = False
LANGBOOL = False
REALMBOOL = False
ZIP_FILES = False
COMPATIBILITY = False
CLEAR = False
DELETE = False

completed = 0

# Finds the pack format that matches with the selected version
def AutoPack(version):
	version = str(version)
	if int(version.split(".")[1]) >= 17:
		return int(version.split(".")[1]) - 10
	elif int(version.split(".")[1]) == 16:
		if int(version.split(".")[2]) >= 2:
			return 6
		else:
			return 5
	elif int(version.split(".")[1]) >= 15:
		return 5
	elif int(version.split(".")[1]) >= 13:
		return 4
	elif int(version.split(".")[1]) >= 11:
		return 3
	elif int(version.split(".")[1]) >= 9:
		return 2
	elif int(version.split(".")[1]) >= 7:
		return 1
	elif int(version.split(".")[1]) >= 6:
		if int(version.split(".")[2]) == 1:
			return 1
	return 5

# Clears the console
def Clear(clear):
	if clear == True:
		os.system("cls")

# Starts the extracting process
def ExtractStart(outPath, packName, version, snapshot, snapshotBool, packPNG, customPackPNG, Description, pack, autoPack, sounds, shaders, langBool, realmBool, zipFiles, compatibility, clear, delete):
	global OUTPUT_PATH, PACK_NAME, MC_VERSION, SNAPSHOT, SNAPSHOT_BOOL, PACK_PNG, CUSTOM_PACK_PNG, DESCRIPTION, MC_PACK, AUTO_PACK, SOUNDS, SHADERSBOOL, LANGBOOL, REALMBOOL, ZIP_FILES, COMPATIBILITY, CLEAR, DELETE

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
	SHADERSBOOL = shaders
	LANGBOOL = langBool
	REALMBOOL = realmBool
	ZIP_FILES = zipFiles
	COMPATIBILITY = compatibility
	CLEAR = clear
	DELETE = delete

	thread = Thread(target = Extract, args = (0,))
	thread.start()

# Extracts a file that is not in the .jar
def ExtractOBJ(args, src, dest):
	os.makedirs(os.path.dirname(dest), exist_ok=True)
	shutil.copyfile(src, dest)

# Extracts a file from the .jar
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

# Prints a progress bar in the console
def ProgressBar(message, current, total, barLength = 40):
	percent = float(current) * 100 / total
	arrow   = "\u25A0" * int(percent/100 * barLength - 1)
	spaces  = " " * (barLength - len(arrow))

	if current >= total:
		print(f"  | %s%s| %d %% {message}" % (arrow, spaces, percent))
	else:
		print(f"  | %s%s| %d %% {message}" % (arrow, spaces, percent), end='\r')

def Check(fileName, text, index):
	if (len(fileName.split("/")) >= index + 1):
		if (fileName.split("/")[index] == text):
			return False
		else:
			return True
	else:
		return False

# This is a heavly modified version of https://minecraft.gamepedia.com/Tutorials/Sound_directory
def Extract(args):
	global OUTPUT_PATH, PACK_NAME, MC_VERSION, SNAPSHOT, SNAPSHOT_BOOL, PACK_PNG, CUSTOM_PACK_PNG, DESCRIPTION, MC_PACK, AUTO_PACK, SOUNDS, SHADERSBOOL, LANGBOOL, REALMBOOL, ZIP_FILES, COMPATIBILITY, CLEAR, DELETE

	Clear(CLEAR)

	# Errors & Warrnings
	if OUTPUT_PATH.replace(" ", "") == "":
		print("Error: No output path provided.")
		return
	if PACK_NAME.replace(" ", "") == "":
		print("Warning: no name provided.")
		PACK_NAME = "Minecraft Resources"
	if MC_VERSION.replace(" ", "") == "":
		print("Error: No version provided.")
		return
	if PACK_PNG.replace(" ", "") == "" and CUSTOM_PACK_PNG == True:
		print("Warning: no image provided.")

	if CUSTOM_PACK_PNG == False or CUSTOM_PACK_PNG == None or PACK_PNG.replace(" ", "") == "":
		PACK_PNG = "icon.png"
	else:
		image = Image.open(PACK_PNG)
		width, height = image.size
		image.close()
		if image.size[0] != image.size[1]:
			print("Error: Image needs to be 1/1 aspect ratio.")
			return

	MC_VERSION_SNAPSHOT = MC_VERSION

	if SNAPSHOT_BOOL:
		MC_VERSION_SNAPSHOT = SNAPSHOT

	MC_PACK = AutoPack(MC_VERSION)

	if SOUNDS == True:
		SOUND = "sounds"
	else:
		SOUND = "null"

	if SHADERSBOOL == False:
		SHADERS = "shaders"
	else:
		SHADERS = "null"

	if LANGBOOL == True:
		LANG = "lang"
	else:
		LANG = "null"

	if REALMBOOL == False:
		REALM = "realms"
	else:
		REALM = "null"

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

	# Errors
	if not os.path.exists(MC_ASSETS):
		print("Error: Minecraft not found.")
		return
	if not os.path.exists(MC_VERSION_JAR):
		print("Error: Minecraft version can not be found. Check to see if the version is installed, or if you typed the right version.")
		return

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

	# Where the unextracted asset files are
	MC_OBJECTS_PATH = f"{MC_ASSETS}/objects"
	# How it finds out weather it is an asset or somthing else
	MC_SOUNDS = r"minecraft/"

	Clear(CLEAR)

	if os.path.exists(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}")) and not ZIP_FILES:
		shutil.rmtree(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}"))
	elif os.path.exists(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}.zip")) and ZIP_FILES:
		os.remove(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}.zip"))

	# Opens the .jar
	with ZipFile(MC_VERSION_JAR, 'r') as zip:
		# Get a list of all archived file names from the zip
		listOfFileNames = zip.namelist()
	
		length = 0
		current = 0

		for fileName in listOfFileNames:
			if fileName.startswith("assets"):
				if fileName.split("/")[1] != REALM and Check(fileName, SHADERS, 2):
					length += 1

		global completed

		# Iterate over the file names
		for fileName in listOfFileNames:
			if fileName.startswith("assets"):
				if fileName.split("/")[1] != REALM and Check(fileName, SHADERS, 2):
					current += 1
					ProgressBar("Extracting .jar Progress", current, length)
							
					# Finds out what thread to use
					currentThread = round((os.cpu_count() - 1) * (current / length)) + 1

					# Copy the file
					threadJAR = Thread(target = ExtractJAR, args = (currentThread, zip, fileName))
					threadJAR.start()

		# Waits for all threads to be complete
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

		for fpath, fhash in sounds.items():
			if fpath.split("/")[0] == SOUND or fpath[0] == "t" or fpath.split("/")[0] == LANG:
				length += 1

		for fpath, fhash in sounds.items():
			if fpath.split("/")[0] == SOUND or fpath[0] == "t" or fpath.split("/")[0] == LANG:
				current += 1

				if SOUNDS and LANGBOOL:
					ProgressBar("Extracting Sounds And Languages Progress", current, length)
				elif not SOUNDS and LANGBOOL:
					ProgressBar("Extracting Languages Progress", current, length)
				elif SOUNDS and not LANGBOOL:
					ProgressBar("Extracting Sounds Progress", current, length)

				src_fpath = os.path.normpath(f"{MC_OBJECTS_PATH}/{fhash[:2]}/{fhash}")
				dest_fpath = os.path.normpath(f"{OUTPUT_PATH}/{PACK_NAME}/assets/minecraft/{fpath}")

				# finds out what thread to use
				if currentThread < os.cpu_count():
					currentThread += 1
				else:
					currentThread = 1

				# Copy the file
				threadOBJ = Thread(target = ExtractOBJ, args = (currentThread, src_fpath, dest_fpath))
				threadOBJ.start()
	
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

	print(f"\nExtracted All Assets To {os.path.normpath(f'{OUTPUT_PATH}//{PACK_NAME}')}\ \n")

	# Handles zipping the files
	if ZIP_FILES == False:
		print("Finished.")
	else:
		Clear(CLEAR)

		files = getListOfFiles(os.path.normpath(f"{OUTPUT_PATH}\{PACK_NAME}"))

		current = 0
		length = len(files)

		if os.path.exists(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}.zip")):
			os.remove(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}.zip"))

		zip = ZipFile(os.path.normpath(f"{REAL_OUTPUT_PATH}\\{PACK_NAME}.zip"),"a")

		for file in files:
			current += 1
			ProgressBar("Zipping files", current, length)

			zip.write(file, arcname=f"{file.replace(os.path.normpath(f'{OUTPUT_PATH}//{PACK_NAME}'), '')}")
		
		zip.close()

		print(f"\nZipped {os.path.normpath(f'{REAL_OUTPUT_PATH}//{PACK_NAME}')}.zip")

		Clear(CLEAR)

		# Deletes unzipped files
		if DELETE:
			print("Cleaning Temp Files...")
			shutil.rmtree(os.path.normpath(f"{OUTPUT_PATH}\\{PACK_NAME}"))

		print("Finished.")
