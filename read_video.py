import cv2
from imutils.video import VideoStream
import time
import json
import tkinter as tk
from tkinter import *
import ttk
from ttk import Frame
from PIL import Image, ImageTk
from detector import Detector


with open("config.json", "r") as file:
    config = json.load(file)

img_size = config["img_output_resolution"]
yolo_detector = Detector()
# Configuracion de la ventana
mainWindow = tk.Tk()
mainWindow.geometry("%dx%d+%d+%d" % (img_size[0], img_size[1], 0, 0))
mainWindow.resizable(0, 0)
mainFrame = Frame(mainWindow)
mainFrame.place(x=0, y=0)
lmain = tk.Label(mainFrame)
lmain.grid(row=0, column=0)

cap = cv2.VideoCapture(config["stream_url"])
# cap = cv2.VideoCapture('video_3.mp4')
# cap = VideoStream(config['stream_url']).start()
# time.sleep(2)

# Ciclo principal
def show_frame():
    ret, frame = cap.read()
    detections = yolo_detector.detect(frame)
    frame = detections["ploted_img"]
    frame = Image.fromarray(frame) if not type(frame) == Image else frame
    frame = frame.resize((img_size[0], img_size[1]))
    imgtk = ImageTk.PhotoImage(image=frame)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


show_frame()
mainWindow.mainloop()

