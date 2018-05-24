import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import threading
import time

class Settings:

    def __init__(self, parent):

        self.file = 'settings.json'
        self.savePath = os.path.expanduser("~\\Documents\\NBGI\\DARK SOULS REMASTERED\\")
        self.saveFileName = 'DRAKS0005.sl2'
        self.backupFolder = self.savePath + "backup\\"
        self.folder = None

        for x in os.listdir(self.savePath):

            if len(x) == 8 and os.path.isdir(self.savePath + x + "\\"):

                self.folder = x
                print(x + " chosen")

        if not os.path.isdir(self.backupFolder):
            os.mkdir(self.backupFolder)

        self.data = {
            'folder': self.folder,
            'backups': os.listdir(self.backupFolder),
            'last': None
        }

        self.fullPath = None

        if os.path.isfile(self.file):
            self.load()

        else:
            self.save()
            self.load()

    def load(self):

        with open(self.file) as file:
            data = file.readlines()[0]

        data = json.loads(data)
        _flag = False

        for x in self.data:
            if x not in data:
                data[x] = self.data[x]
                _flag = True

        self.data = data

        if _flag:
            self.save()

        if self.fullPath == None and self.data['folder'] != None:

            self.fullPath = self.savePath + self.data['folder'] + "\\" + self.saveFileName

    def save(self):

        data = json.JSONEncoder().encode(self.data)
        file = open(self.file, 'w')
        file.write(data)
        file.close()


#########
#GUI#
#########

class mainWindow:

    def __init__(self, master):

        self.master = master
        self.settings = Settings(self)
        self.data = self.settings.data
        self.master.title("DS Remastered Backup")

        if self.data['folder'] == None:

            self.pickFolder()

        self.info = ttk.Label(self.master, text="Current savefile: {}".format('N/A' if self.data['last'] == None else self.data['last']))
        self.info.grid(row=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        self.backupButton = ttk.Button(self.master, text="Back up savefile", command=self.backup)
        self.restoreButton = ttk.Button(self.master, text="Restore savefile", command=self.restore)

        self.backupButton.grid(row=1, padx=10, pady=10)
        self.restoreButton.grid(row=1, column=1, padx=10, pady=10)

        self.status = ttk.Label(self.master, text="")
        self.status.grid(row=2, columnspan=2, sticky=tk.W)

        self.checkButtons()

    def checkButtons(self):

        if len(os.listdir(self.settings.backupFolder)) == 0:

            self.restoreButton.config(state=tk.DISABLED)

        else:

            self.restoreButton.config(state=tk.NORMAL)

    def backup(self):

        res = filedialog.asksaveasfilename(filetypes=[('Backup file', '.bak')], initialdir=self.settings.savePath + "backup\\", defaultextension=".bak", initialfile="save{}".format(len(os.listdir(self.settings.backupFolder))+1))

        if res != "" and res != None:

            shutil.copyfile(self.settings.fullPath, res)

            noop = res.split("/")[-1][:-4]

            self.updateInfo(noop)

            print("Done")
            self.status.config(text="{} backed up".format(noop), foreground="green")
            t = threading.Thread(target=self.reset)
            t.start()

        self.checkButtons()

    def updateInfo(self, fname):

        self.info.config(text="Current savefile: {}".format(fname))
        self.data['last'] = fname
        self.settings.save()

    def restore(self):

        if len(os.listdir(self.settings.backupFolder)) == 0:

            self.status.config(text="You have no backups!", foreground="red")

            t = threading.Thread(target=self.reset)
            t.start()

            return

        else:

            res = filedialog.askopenfilename(filetypes=[('Backup file', '.bak')], initialdir=self.settings.savePath + "backup\\")

            if res != None and res != "":

                shutil.copyfile(res, self.settings.fullPath)

                noop = res.split("/")[-1][:-4]
                self.updateInfo(noop)

                print("Done")
                self.status.config(text="{} restored".format(noop), foreground="green")
                t = threading.Thread(target=self.reset)
                t.start()

        self.checkButtons()

    def reset(self):
        time.sleep(3)
        self.status.config(text="")

def getResource(relative_path):

    try:
        base_path = os.path.join(sys._MEIPASS, 'data')
    except:
        print("No bueno")

    return os.path.join(base_path, relative_path)