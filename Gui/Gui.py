import base64
import ctypes
import tkinter as tk
from io import BytesIO
from PIL import ImageTk, Image
from Gui.pic2str import flipkart
from Web.ReadTracker import Tracker

class Gui:

    def __init__(self,tracker, username, password):
        self.inputfile = tracker
        self.username = username
        self.password = password

    def open_gui(self):

        global label_status

        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

        window = tk.Tk()

        window.configure(background='#00AAE4')
        window.title("Flipkart")

        window.columnconfigure(0, weight=1, minsize=75)
        window.rowconfigure(0, weight=1, minsize=50)
        window.columnconfigure(1, weight=1, minsize=75)
        window.rowconfigure(1, weight=1, minsize=50)
        window.columnconfigure(2, weight=1, minsize=75)
        window.rowconfigure(2, weight=1, minsize=50)

        w = 350
        h = 400
        x = 900
        y = 0

        window.geometry('%dx%d+%d+%d' % (w, h, x, y))

        frame_image = tk.Frame(
            master=window,
            relief=tk.RAISED,
            background='#00AAE4',
        )

        byte_data = base64.b64decode(flipkart)
        image_data = BytesIO(byte_data)
        image = Image.open(image_data)
        resize_image = image.resize((90, 70))
        img = ImageTk.PhotoImage(resize_image)
        label2 = tk.Label(master=frame_image, image=img)
        label2.pack()

        frame_button = tk.Frame(
            master=window,
            relief=tk.RAISED,
            background='#00AAE4',
        )

        button = tk.Button(
            master=frame_button,
            width=15,
            height=2,
            text="Draft Consignment",
            command=self.process_tracker
        )
        button.pack()

        frame_button2 = tk.Frame(
            master=window,
            relief=tk.RAISED,
            background='#00AAE4',
        )

        button2 = tk.Button(
            master=frame_button2,
            width=15,
            height=2,
            text="Create Consignment",
            command=self.create_consignment
        )
        button2.pack()

        frame_status = tk.Frame(
            master=window,
            relief=tk.RAISED,
            background='#00AAE4',
        )

        label_status = tk.Label(master=frame_status, text="", fg="white", bg="#00AAE4", font=('Arial', 13))
        label_status.pack()

        frame_image.grid(row=0, column=0)
        frame_button.grid(row=1, column=1)
        frame_button2.grid(row=2, column=1)
        frame_status.grid(row=3, column=1)
        window.mainloop()

    def process_tracker(self):
        tracker = Tracker(tracker=self.inputfile,username=self.username,password=self.password,label=label_status)
        tracker.read()

    def create_consignment(self):
        tracker = Tracker(tracker=self.inputfile, username=self.username, password=self.password, label=label_status)
        tracker.createconsignment()







