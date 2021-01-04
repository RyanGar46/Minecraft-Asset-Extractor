import os, webbrowser
from Extract import *
from tkinter import *
from tkinter import filedialog
from datetime import datetime

def extract():
	Extract(
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
	bool(zipBool.get()), # Zip
	bool(compatibilityBool.get()), # Compatibility
	bool(clearBool.get()), # Clear command line
	bool(deleteBool.get())) # Delets folder after zipping

def openFolder():
	folder = filedialog.askdirectory(initialdir=os.path.normpath("C://"), title="Select Output Location")
	
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

def settingsUI():
	setting = Toplevel(root)

	setting.focus_force()
	setting.title("Credit")
	setting.iconphoto(False, windowIcon)
	setting.geometry("400x300")
	setting.resizable(False, False)

	settingsTitleText = Label(setting, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
	settingsTitleText.place(relx=0.5, rely=0.0, anchor="n")

	closeButton = Button(setting, text="Close", command=lambda:closeWindow(setting))
	closeButton.place(relx=1.0, rely=1.0, anchor="se")

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

	githubProject = Label(about, text="Minecraft Asset Extractor", fg="blue", cursor="hand2", font=('Arial',9,'underline'))
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

	version = Label(about, text="V0.3.0 - Alpha")
	version.place(relx=0.0, rely=1.0, anchor="sw")

	closeButton = Button(about, text="Close", command=lambda:closeWindow(about))
	closeButton.place(relx=1.0, rely=1.0, anchor="se")

	about.mainloop()

# Creates the available choices in the pack format drop down.
packFormats = [
"1",
"2",
"3",
"4",
"5",
"6",
"7"
]

# Creates the available choices in the snapshot letters drop down.
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
snapshotsBool = IntVar()
compatibilityBool = IntVar()
zipBool = IntVar()
clearBool = IntVar()
deleteBool = IntVar()

# Sets defualt value.
snapshotLetterSelection = StringVar(root)
snapshotLetterSelection.set(snapshotLetters[0])

# Sets defualt value.
formatChoices = StringVar(root)
formatChoices.set(packFormats[5])

# Sets the info about the window.
root.focus_force()
windowIcon = PhotoImage(file = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "pack.png"))
root.title("Minecraft Asset Extractor")
root.iconphoto(False, windowIcon)
root.resizable(False, False)

# Creating and placing labels.
titleText = Label(root, text="Minecraft Asset Extractor\nBy: Ryan Garrett")
titleText.place(relx=0.5, rely=0.0, anchor="n")

settings = Button(root, text="Settings", command=settingsUI)
settings.grid(row=0, column=0, sticky=NW)

aboutButton = Button(root, text="About", command=aboutUI)
aboutButton.place(x=53, y=0, anchor=NW)

outputLocationText = Label(root, text="Output Location:").grid(row=1, column=0, sticky="W")
outputLocation = Entry(root, width=50)
outputLocation.insert(0, os.path.normpath(os.path.expandvars(os.path.expanduser(r"~/Desktop/"))))
outputLocation.grid(row=2, column=0, sticky="W")
outputLocationButton = Button(root, text="Select Folder", command=openFolder)
outputLocationButton.grid(row=2, column=1)

packNameText = Label(root, text="Resource Pack Name:").grid(row=3, column=0, sticky="W")
packName = Entry(root, width=50)
packName.grid(row=4, column=0, sticky="W")

minecraftVersionText = Label(root, text="Minecraft Version (e.g. 1.16.4, 1.17):").grid(row=5, column=0, sticky="W")
minecraftVersion = Entry(root, width=50)
minecraftVersion.insert(0, "1.16.4")
minecraftVersion.grid(row=6, column=0, sticky="W")

snapshotText = Label(root, text="Snapshot Version:").grid(row=7, column=0, sticky="W")

snapshotYearText = Label(root, text="Year:").place(x=0, y=210, anchor=W)
snapshotYear = Entry(root, width=2)
snapshotYear.insert(0, str(datetime.today().year)[-2:]) # I don't care that this is more robust than it needs to be.
snapshotYear.configure(state="disabled")
snapshotYear.place(x=40, y=210, anchor=W)

snapshotWeekText = Label(root, text="Week:").place(x=60, y=210, anchor=W)
snapshotWeek = Entry(root, width=2)
snapshotWeek.insert(0, str(datetime.today().isocalendar()[1]))
snapshotWeek.configure(state="disabled")
snapshotWeek.place(x=105, y=210, anchor=W)

snapshotLetterText = Label(root, text="Pack Format:").grid(row=13, column=0, sticky="W")
snapshotLetter = OptionMenu(root, snapshotLetterSelection, *snapshotLetters)
snapshotLetter.configure(state="disabled")
snapshotLetter.place(x=130, y=210, anchor=W)

packPNGSelectText = Label(root, text="Custom Pack Icon:").grid(row=9, column=0, sticky="W")
packPNGSelect = Entry(root, width=50, state="disabled")
packPNGSelect.grid(row=10, column=0, sticky="W")
packPNGSelectButton = Button(root, text="Select File", command=openFile, state="disabled")
packPNGSelectButton.grid(row=10, column=1)

descriptionText = Label(root, text="Description:").grid(row=11, column=0, sticky="W")
description = Entry(root, width=50)
description.grid(row=12, column=0, sticky="W")

packFormatText = Label(root, text="Pack Format:").grid(row=13, column=0, sticky="W")
packFormat = OptionMenu(root, formatChoices, *packFormats)
packFormat.configure(state="disabled")
packFormat.grid(row=14, column=0, sticky="W")

### Options
sounds = Checkbutton(root, variable=soundsBool).grid(row=2, column=2, sticky="E")
soundsText = Label(root, text="Sound Files").grid(row=2, column=3, sticky="W")

languages = Checkbutton(root, variable=languagesBool).grid(row=3, column=2, sticky="E")
languagesText = Label(root, text="Lang Files").grid(row=3, column=3, sticky="W")

compatibilityFixes = Checkbutton(root, variable=compatibilityBool)
compatibilityFixes.grid(row=4, column=2, sticky="E")
compatibilityFixes.select()
compatibilityFixesText = Label(root, text="Compatibility Fixes").grid(row=4, column=3, sticky="W")

snapshots = Checkbutton(root, command=snapshotButton, variable=snapshotsBool)
snapshots.grid(row=5, column=2, sticky="E")
snapshotsText = Label(root, text="Is a Snapshot").grid(row=5, column=3, sticky="W")

packPNG = Checkbutton(root, command=packPNGButton, variable=packPNGBool)
packPNG.grid(row=6, column=2, sticky="E")
packPNGText = Label(root, text="Custom Pack Image").grid(row=6, column=3, sticky="W")

autoPack = Checkbutton(root, command=packFormatButton, variable=autoPackBool)
autoPack.grid(row=7, column=2, sticky="E")
autoPack.select()
autoPackText = Label(root, text="Auto Pack Format").grid(row=7, column=3, sticky="W")

zip = Checkbutton(root, command=zipButton, variable=zipBool)
zip.grid(row=8, column=2, sticky="E")
zipText = Label(root, text="Zip Files").grid(row=8, column=3, sticky="W")

delete = Checkbutton(root, variable=deleteBool)
delete.grid(row=9, column=2, sticky="E")
delete.configure(state="disabled")
deleteText = Label(root, text="Delete Folder After Zip").grid(row=9, column=3, sticky="W")

clear = Checkbutton(root, variable=clearBool)
clear.grid(row=10, column=2, sticky="E")
clearText = Label(root, text="Clear Command Line").grid(row=10, column=3, sticky="W")

### Bottom
extractButton = Button(root, text="Extract", command=lambda:extract()).place(relx=1.0, rely=1.0, anchor="se")

root.mainloop()

# Stops the menu from opening again
root.destroy()
