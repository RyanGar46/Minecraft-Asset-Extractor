import os, webbrowser
from time import sleep
from threading import Thread
from configparser import *
from Extract import *
from tkinter import *
from tkinter import filedialog
from datetime import datetime

programVersion = "V0.5.0 - Beta"

desktopDir = os.path.normpath(os.path.expandvars(os.path.expanduser(r"~/Desktop/")))

settingsDefaultOutputLocation = desktopDir

def convertToRGB(r, g, b):
	"""translates rgb to a tkinter friendly color code
	"""
	return f"#{r:02x}{g:02x}{b:02x}"

# When mouse is hovering over button
def onEnter(e):
	if e.widget["state"] == NORMAL:
		e.widget["background"] = convertToRGB(220, 220, 220)

# When mouse leaves button
def onLeave(e):
    e.widget["background"] = "SystemButtonFace"

def extract():
	ExtractStart(
	os.path.normpath(outputLocation.get()), # Output Location
	packName.get(), # Pack Name
	minecraftVersion.get(), # Minecraft Version
	f"{snapshotYear.get()}w{snapshotWeek.get()}{snapshotLetterSelection.get()}", # Snapshot
	bool(snapshotsBool.get()), # Snapshot bool
	packPNGSelect.get(), # pack.png
	bool(packPNGBool.get()), # Custom pack.png
	description.get(), # Description
	formatChoices.get(), # Pack Format
	bool(autoPackBool.get()), # Auto Pack Format
	bool(soundsBool.get()), # Sounds
	bool(languagesBool.get()), # LANG
	bool(realmBool.get()), # Realm Files
	bool(zipBool.get()), # Zip
	bool(compatibilityBool.get()), # Compatibility
	bool(clearBool.get()), # Clear command line
	bool(deleteBool.get())) # Delets folder after zipping

def openFolder(parent, outputLocation):
	folder = filedialog.askdirectory(parent=parent,initialdir=os.path.normpath("C://"), title="Select Output Location")
	
	if folder != "":
		outputLocation.delete(0, END)
		outputLocation.insert(0, folder)

def openFile():
	folder = filedialog.askopenfilename(initialdir=os.path.normpath("C://"), title="Select File", filetypes =(("PNG", "*.png"),("All Files","*.*")))

	if folder != "":
		packPNGSelect.delete(0, END)
		packPNGSelect.insert(0, folder)

def zipButton():
	if zipBool.get():
		delete.configure(state="normal")
	if not zipBool.get():
		delete.configure(state="disabled")

def snapshotButton():
	if snapshotsBool.get():
		snapshotLetter.configure(state="normal")
		snapshotWeek.configure(state="normal")
		snapshotYear.configure(state="normal")
	elif not snapshotsBool.get():
		snapshotLetter.configure(state="disabled")
		snapshotWeek.configure(state="disabled")
		snapshotYear.configure(state="disabled")

def packFormatButton():
	if not autoPackBool.get():
		packFormat.configure(state="active")
	elif autoPackBool.get():
		packFormat.configure(state="disabled")

def packPNGButton():
	if packPNGBool.get():
		packPNGSelect.configure(state="normal")
		packPNGSelectButton.configure(state="normal")
	elif not packPNGBool.get():
		packPNGSelect.configure(state="disabled")
		packPNGSelectButton.configure(state="disabled")

def callback(url):
    webbrowser.open_new(url)

def closeWindow(window):
	window.destroy()
	root.focus_force()

def introUI():
	intro = Toplevel(root)

	intro.focus_force()
	intro.title("Introduction Screen")
	intro.iconphoto(False, windowIcon)
	intro.geometry("400x300")
	intro.resizable(False, False)

	settingsTitleText = Label(intro, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
	settingsTitleText.place(relx=0.5, rely=0.0, anchor="n")

	spacer = Label(intro, text="", pady=10).grid(row=0, column=0, sticky="NW")

	introgithubProject = Label(intro, text="Minecraft Asset Extractor Github Page", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	introgithubProject.place(relx=0.5, rely=0.5, anchor="center")
	introgithubProject.bind("<Button-1>", lambda e: callback("https://github.com/RyanGar46/Minecraft-Asset-Extractor"))

	introVersion = Label(intro, text=programVersion)
	introVersion.place(relx=0.0, rely=1.0, anchor="sw")

	closeButton = Button(intro, text="Close", command=lambda:closeWindow(intro), relief="flat")
	closeButton.place(relx=1.0, rely=1.0, anchor="se")
	closeButton.bind("<Enter>", onEnter)
	closeButton.bind("<Leave>", onLeave)

def settingsUI():
	setting = Toplevel(root)

	setting.focus_force()
	setting.title("Settings")
	setting.iconphoto(False, windowIcon)
	setting.geometry("400x300")
	setting.resizable(False, False)

	settingsTitleText = Label(setting, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
	settingsTitleText.place(relx=0.5, rely=0.0, anchor="n")

	spacer = Label(setting, text="", pady=10).grid(row=0, column=0, sticky="NW")

	global defaultOutputLocation

	outputLocationText = Label(setting, text="Default Output Location:").grid(row=1, column=0, sticky="W")
	defaultOutputLocation = Entry(setting, width=50)
	defaultOutputLocation.insert(0, settingsDefaultOutputLocation)
	defaultOutputLocation.grid(row=2, column=0, sticky="W")
	outputLocationButton = Button(setting, text="Select Folder", command=lambda:openFolder(setting, defaultOutputLocation), relief="flat")
	outputLocationButton.grid(row=2, column=1)
	outputLocationButton.bind("<Enter>", onEnter)
	outputLocationButton.bind("<Leave>", onLeave)

	settingsVersion = Label(setting, text=programVersion)
	settingsVersion.place(relx=0.0, rely=1.0, anchor="sw")

	closeButton = Button(setting, text="Close", command=lambda:closeWindow(setting), relief="flat")
	closeButton.place(relx=1.0, rely=1.0, anchor="se")
	closeButton.bind("<Enter>", onEnter)
	closeButton.bind("<Leave>", onLeave)

def aboutUI():
	about = Toplevel(root)

	about.focus_force()
	about.title("Credit")
	about.iconphoto(False, windowIcon)
	about.geometry("400x300")
	about.resizable(False, False)

	aboutTitleText = Label(about, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
	aboutTitleText.place(relx=0.5, rely=0.0, anchor="n")

	spacer = Label(about, text="", pady=10).grid(row=0, column=0, sticky="N")

	aboutText = Label(about, text="Ryan Garret (RyanGar46):")
	aboutText.grid(row=1, column=0, sticky="W")

	github = Label(about, text="GitHub", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	github.grid(row=2, column=0, sticky="W")
	github.bind("<Button-1>", lambda e: callback("https://github.com/RyanGar46"))

	githubProject = Label(about, text="Minecraft Asset Extractor Github Page", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	githubProject.grid(row=3, column=0, sticky="W")
	githubProject.bind("<Button-1>", lambda e: callback("https://github.com/RyanGar46/Minecraft-Asset-Extractor"))

	twitter = Label(about, text="Twitter", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	twitter.grid(row=4, column=0, sticky="W")
	twitter.bind("<Button-1>", lambda e: callback("https://twitter.com/RyanGar46"))

	youtube = Label(about, text="YouTube", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	youtube.grid(row=5, column=0, sticky="W")
	youtube.bind("<Button-1>", lambda e: callback("https://www.youtube.com/channel/UCa5CoSRScfDUtoEAenjbnZg"))

	curseforge = Label(about, text="CurseForge", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	curseforge.grid(row=6, column=0, sticky="W")
	curseforge.bind("<Button-1>", lambda e: callback("https://www.curseforge.com/members/ryangar46/projects"))

	planetMC = Label(about, text="Planet Minecraft", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
	planetMC.grid(row=7, column=0, sticky="W")
	planetMC.bind("<Button-1>", lambda e: callback("https://www.planetminecraft.com/member/ryangar46"))

	version = Label(about, text=programVersion)
	version.place(relx=0.0, rely=1.0, anchor="sw")

	closeButton = Button(about, text="Close", command=lambda:closeWindow(about), relief="flat")
	closeButton.place(relx=1.0, rely=1.0, anchor="se")
	closeButton.bind("<Enter>", onEnter)
	closeButton.bind("<Leave>", onLeave)

	about.mainloop()

def loadSettings():
	global settingsDefaultOutputLocation

	read_config = ConfigParser()

	if os.path.exists("settings.ini"):
		read_config.read("settings.ini")
	else:
		read_config.read("default_settings.ini")

	# The options on the right
	if read_config.get("CheckBoxes", "snapshot") == "True":
		snapshots.select()
	else:
		snapshots.deselect()

	if read_config.get("CheckBoxes", "png") == "True":
		packPNG.select()
	else:
		packPNG.deselect()

	if read_config.get("CheckBoxes", "auto_pack") == "True":
		autoPack.select()
	else:
		autoPack.deselect()

	if read_config.get("CheckBoxes", "sounds") == "True":
		sounds.select()
	else:
		sounds.deselect()

	if read_config.get("CheckBoxes", "shaders") == "True":
		shaders.select()
	else:
		shaders.deselect()

	if read_config.get("CheckBoxes", "languages") == "True":
		languages.select()
	else:
		languages.deselect()

	if read_config.get("CheckBoxes", "realm") == "True":
		realm.select()
	else:
		realm.deselect()

	if read_config.get("CheckBoxes", "compatibility") == "True":
		compatibilityFixes.select()
	else:
		compatibilityFixes.deselect()

	if read_config.get("CheckBoxes", "clear") == "True":
		clear.select()
	else:
		delete.deselect()

	if read_config.get("CheckBoxes", "zip") == "True":
		zip.select()
	else:
		zip.deselect()

	if read_config.get("CheckBoxes", "delete") == "True":
		delete.select()
	else:
		delete.deselect()
	zipButton()

	# The fields on the left.
	outputLocation.delete(0, END)
	if read_config.get("Fields", "output_location").replace(" ", "") == "":
		outputLocation.insert(0, desktopDir)
	else:
		outputLocation.insert(0, read_config.get("Fields", "output_location"))
	packName.delete(0, END)
	packName.insert(0, read_config.get("Fields", "name"))
	minecraftVersion.delete(0, END)
	minecraftVersion.insert(0, read_config.get("Fields", "version"))
	snapshotButton()
	packPNGSelect.delete(0, END)
	packPNGSelect.insert(0, read_config.get("Fields", "png"))
	packPNGButton()
	description.delete(0, END)
	description.insert(0, read_config.get("Fields", "description"))
	formatChoices.set(packFormats[packFormats.index(read_config.get("Fields", "pack_format"))])
	packFormatButton()

	# Settings
	if read_config.get("Settings", "default_output_location").replace(" ", "") == "":
		settingsDefaultOutputLocation = desktopDir
	else:
		settingsDefaultOutputLocation = read_config.get("Settings", "default_output_location")
		outputLocation.delete(0, END)
		outputLocation.insert(0, read_config.get("Settings", "default_output_location"))

	if read_config.get("Settings", "intro_screen") == "True":
		introUI()

def on_closing():
	saveSettings()
	root.destroy()

def saveSettings():
	# Saves the last used settings
	write_config = ConfigParser()

	# The fields on the left
	write_config.add_section("Fields")
	if outputLocation.get() != settingsDefaultOutputLocation:
		write_config.set("Fields","output_location", outputLocation.get())
	else:
		write_config.set("Fields","output_location", "")
	write_config.set("Fields","name", packName.get())
	write_config.set("Fields","version", minecraftVersion.get())
	write_config.set("Fields","png", packPNGSelect.get())
	write_config.set("Fields","description", description.get())
	write_config.set("Fields","pack_format", formatChoices.get())

	# The options on the right
	write_config.add_section("CheckBoxes")
	write_config.set("CheckBoxes","snapshot", str(bool(snapshotsBool.get())))
	write_config.set("CheckBoxes","png", str(bool(packPNGBool.get())))
	write_config.set("CheckBoxes","auto_pack", str(bool(autoPackBool.get())))
	write_config.set("CheckBoxes","sounds", str(bool(soundsBool.get())))
	write_config.set("CheckBoxes","shaders", str(bool(shadersBool.get())))
	write_config.set("CheckBoxes","languages", str(bool(languagesBool.get())))
	write_config.set("CheckBoxes","realm", str(bool(realmBool.get())))
	write_config.set("CheckBoxes","zip", str(bool(zipBool.get())))
	write_config.set("CheckBoxes","compatibility", str(bool(compatibilityBool.get())))
	write_config.set("CheckBoxes","clear", str(bool(clearBool.get())))
	write_config.set("CheckBoxes","delete", str(bool(deleteBool.get())))

	# Extra settings
	write_config.add_section("Settings")
	if settingsDefaultOutputLocation != desktopDir:
		write_config.set("Settings","default_output_location", settingsDefaultOutputLocation)
	else:
		write_config.set("Settings","default_output_location", "")
	write_config.set("Settings","intro_screen", "False")

	cfgfile = open("settings.ini",'w')
	write_config.write(cfgfile)
	cfgfile.close()

# Creates the available choices in the pack format drop down
packFormats = [
"1",
"2",
"3",
"4",
"5",
"6",
"7"
]

# Creates the available choices in the snapshot letters drop down
snapshotLetters = [
"a",
"b",
"c",
"d"
]

root = Tk()

autoPackBool = IntVar()
packPNGBool = IntVar()
soundsBool = IntVar()
languagesBool = IntVar()
realmBool = IntVar()
snapshotsBool = IntVar()
compatibilityBool = IntVar()
zipBool = IntVar()
clearBool = IntVar()
deleteBool = IntVar()

# Sets defualt value for the snapshot letter
snapshotLetterSelection = StringVar(root)
snapshotLetterSelection.set(snapshotLetters[0])

# Sets defualt value for pack format
formatChoices = StringVar(root)
formatChoices.set(packFormats[5])

# Sets the info about the window
root.focus_force()
windowIcon = PhotoImage(file = "icon.png")
root.title("Minecraft Asset Extractor")
root.iconphoto(False, windowIcon)
root.minsize(550, 375)

### Feilds
# region
titleText = Label(root, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
titleText.place(relx=0.5, rely=0.0, anchor="n")

settings = Button(root, text="Settings", command=settingsUI, relief="flat")
settings.grid(row=0, column=0, sticky=NW)
settings.bind("<Enter>", onEnter)
settings.bind("<Leave>", onLeave)

aboutButton = Button(root, text="About", command=aboutUI, relief="flat")
aboutButton.place(x=50, y=0, anchor=NW)
aboutButton.bind("<Enter>", onEnter)
aboutButton.bind("<Leave>", onLeave)

introButton = Button(root, text="Intro Screen", command=introUI, relief="flat")
introButton.place(x=91, y=0, anchor=NW)
introButton.bind("<Enter>", onEnter)
introButton.bind("<Leave>", onLeave)

outputLocationText = Label(root, text="Output Location:").grid(row=1, column=0, sticky="W")
outputLocation = Entry(root, width=50)
outputLocation.insert(0, desktopDir)
outputLocation.grid(row=2, column=0, sticky="W")
outputLocationButton = Button(root, text="Select Folder", command=lambda:openFolder(root, outputLocation), relief="flat")
outputLocationButton.grid(row=2, column=1)
outputLocationButton.bind("<Enter>", onEnter)
outputLocationButton.bind("<Leave>", onLeave)

packNameText = Label(root, text="Resource Pack Name:").grid(row=3, column=0, sticky="W")
packName = Entry(root, width=50)
packName.grid(row=4, column=0, sticky="W")

minecraftVersionText = Label(root, text="Minecraft Version (e.g. 1.16.4, 1.17):").grid(row=5, column=0, sticky="W")
minecraftVersion = Entry(root, width=50)
minecraftVersion.insert(0, "1.16.4")
minecraftVersion.grid(row=6, column=0, sticky="W")

snapshotText = Label(root, text="Snapshot Version:").grid(row=7, column=0, sticky="W")

snapshotYearText = Label(root, text="Year:").place(x=0, y=205, anchor=W)
snapshotYear = Entry(root, width=2)
snapshotYear.insert(0, str(datetime.today().year)[-2:])
snapshotYear.place(x=40, y=205, anchor=W)

snapshotWeekText = Label(root, text="Week:").place(x=60, y=205, anchor=W)
snapshotWeek = Entry(root, width=2)
snapshotWeek.insert(0, str(datetime.today().isocalendar()[1]))
snapshotWeek.place(x=105, y=205, anchor=W)

snapshotLetterText = Label(root, text="Letter:").place(x=125, y=205, anchor=W)
snapshotLetter = OptionMenu(root, snapshotLetterSelection, *snapshotLetters)
snapshotLetter.place(x=165, y=205, anchor=W)

packPNGSelectText = Label(root, text="Custom Pack Icon:").grid(row=9, column=0, sticky="W")
packPNGSelect = Entry(root, width=50)
packPNGSelect.grid(row=10, column=0, sticky="W")
packPNGSelectButton = Button(root, text="Select File", command=openFile, state="disabled", relief="flat")
packPNGSelectButton.grid(row=10, column=1)
packPNGSelectButton.bind("<Enter>", onEnter)
packPNGSelectButton.bind("<Leave>", onLeave)

descriptionText = Label(root, text="Description:").grid(row=11, column=0, sticky="W")
description = Entry(root, width=50)
description.grid(row=12, column=0, sticky="W")

packFormatText = Label(root, text="Pack Format:").grid(row=13, column=0, sticky="W")
packFormat = OptionMenu(root, formatChoices, *packFormats)
packFormat.grid(row=14, column=0, sticky="W")
# endregion

### Options
# region
sounds = Checkbutton(root, variable=soundsBool, text="Sound Files")
sounds.grid(row=2, column=2, sticky="W")

languages = Checkbutton(root, variable=languagesBool, text="Lang Files")
languages.grid(row=3, column=2, sticky="W")

realm = Checkbutton(root, variable=realmBool, text="Realm Files")
realm.grid(row=4, column=2, sticky="W")

compatibilityFixes = Checkbutton(root, variable=compatibilityBool, text="Compatibility Fixes")
compatibilityFixes.grid(row=5, column=2, sticky="W")

snapshots = Checkbutton(root, command=snapshotButton, variable=snapshotsBool, text="Is a Snapshot")
snapshots.grid(row=6, column=2, sticky="W")

packPNG = Checkbutton(root, command=packPNGButton, variable=packPNGBool, text="Custom Pack Image")
packPNG.grid(row=7, column=2, sticky="W")

autoPack = Checkbutton(root, command=packFormatButton, variable=autoPackBool, text="Auto Pack Format")
autoPack.grid(row=8, column=2, sticky="W")

zip = Checkbutton(root, command=zipButton, variable=zipBool, text="Zip Files")
zip.grid(row=9, column=2, sticky="W")

delete = Checkbutton(root, variable=deleteBool, text="Delete Folder After Zip")
delete.grid(row=10, column=2, sticky="W")

clear = Checkbutton(root, variable=clearBool, text="Clear Command Line")
clear.grid(row=11, column=2, sticky="W")
# endregion Options

### Bottom
# region
extractButton = Button(root, text="Extract", command=lambda:extract(), relief="flat")
extractButton.place(relx=1.0, rely=1.0, anchor="se")
extractButton.bind("<Enter>", onEnter)
extractButton.bind("<Leave>", onLeave)
# endregion

loadSettings()

root.protocol("WM_DELETE_WINDOW", on_closing)

def grabSettings(args):
	sleep(1)
	while True:
		sleep(1)
		try:
			global settingsDefaultOutputLocation
			settingsDefaultOutputLocation = defaultOutputLocation.get()
		except:
			None

# Saves settings every 5 seconds
def saveSettingsClock(args):
	while True:
		sleep(5)
		try:
			saveSettings()
		except:
			None

thread = Thread(target = grabSettings, args = (1,))
thread.start()

thread2 = Thread(target = saveSettingsClock, args = (1,))
thread2.start()

root.mainloop()

sys.exit(0)
