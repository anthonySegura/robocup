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
import time
import serial 
ser = serial.Serial('COM5', 9600)


def buscar():
    print("buscar")
    time.sleep(1)
    izquierda()

def forward(distance):
    print("forward"+str(distance+10))
    ser.write(str.encode('F'))
    time.sleep((distance/96))
    ser.write(str.encode('S'))



def buscarMarco(distancia):
    print("buscar marco")
    derecha()
    forward(distancia)
    izquierda()

def derecha():
    print("derecha")
    ser.write(str.encode('R'))
    #time.sleep(1)

def izquierda():
    print("izquierda")
    ser.write(str.encode('L'))
    #time.sleep(1)

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

cap = cv2.VideoCapture(config['stream_url'])
#cap = cv2.VideoCapture('video_3.mp4')
# cap = VideoStream(config['stream_url']).start()
# time.sleep(2)

count = 0

# Ciclo principal
def show_frame():
    global count
    ret, frame = cap.read()
    if ((count % 100) == 0):

        detections = yolo_detector.detect(frame)
        frame = detections["ploted_img"]

        if (detections["location_data"] == {}):
            buscar()  
        if (detections["location_data"] != {}):
            detectionsAux = detections["location_data"]
            ballAngleDistance = None
            markAngleDistance = None
            try: 
                ballAngleDistance = detectionsAux['ball']
            except:
                ballAngleDistance = None
            try:
                markAngleDistance = detectionsAux['mark']
            except:
                markAngleDistance = None
            print(ballAngleDistance,markAngleDistance)
            if ballAngleDistance != None:
                if (ballAngleDistance['rot_angle'] > 20):
                    izquierda()
                    pass
                elif ballAngleDistance['rot_angle'] < -20:
                    derecha()
                    pass

            if (markAngleDistance != None and ballAngleDistance == None):
                buscar()
            
            if (ballAngleDistance != None and markAngleDistance != None):
                if (ballAngleDistance['rot_angle'] <20 and ballAngleDistance['rot_angle'] > -20):
                    forward(ballAngleDistance['distance'])
            if (ballAngleDistance != None and markAngleDistance == None):
                buscarMarco(ballAngleDistance['distance'])
    
    frame = Image.fromarray(frame) if not type(frame) == Image else frame
    frame = frame.resize((img_size[0], img_size[1]))
    imgtk = ImageTk.PhotoImage(image=frame)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


show_frame()
mainWindow.mainloop()


