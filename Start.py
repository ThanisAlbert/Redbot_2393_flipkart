import os
from Gui.Gui import Gui

folder_path = 'Tracker//'
files = os.listdir(folder_path)
for file_name in files:
    filename = file_name

try:
    os.remove("Log.log")
except:
    pass

username ="mekala.p@redservglobal.com"
password = "@Password22"

gui = Gui(tracker="Tracker//" +filename,username=username,password=password)
gui.open_gui()

