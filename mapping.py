import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import cv2 as cv
import socket
import time

host = "192.168.42.1"
port = 5454
x_car=250
y_car=250
r=3.5

"""
def get_data_array(file):
    data_array = []
    # Gets the pixels of the image
    f = open(file, 'r')
    data = f.readlines()
    for i in range(0, len(data)):
        data_array += map(float, data[i].split(" "))
    return data_array
"""


def send_data_to_host(host, port, data):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
    x = data[0]
    y = data[1]
    s.send(x.to_bytes(8, 'big'))
    s.send(y.to_bytes(8, 'big'))
    print("send: " + str(data))
    time.sleep(1)

def get_map(contours):
    for c in contours:
        for a in c:
            for b in a:
                x1, y1 = b
                point(canvas, x1, y1, 1.5, "#FFFFFF")

def get_xy(event):
    # Takes the coordinates of the mouse when you click the mouse
    # global x, y
    canvas.delete(ALL)
    r=3.5
    x, y = event.x, event.y
    canvas.create_text(55,30,fill="white",font="Times 20 italic bold",text="x={}\ny={}".format(x,y))
    canvas.create_oval(x-r,y-r,x+r,y+r,fill="#FF0000")
    canvas.create_oval(x_car-r,y_car-r,x_car+r,y_car+r,fill="#0000FF") 
    send_data_to_host(host, port, [x, y])
    get_map(contours)


def point(canvas, x, y, r, color):
    return canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)


root = tk.Tk()
root.title("Map")
root.wm_iconbitmap('logo2.ico')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

im = cv.imread('img.jpg', cv.IMREAD_GRAYSCALE)
canvas_height = im.shape[0]
canvas_width = im.shape[1]

canvas = tk.Canvas(root, height=canvas_height,
                   width=canvas_width, bg="#000000")
canvas.grid(row=0, column=1)
canvas.pack()
root.bind("<Button-1>", get_xy)


canvas.create_oval(x_car-r,y_car-r,x_car+r,y_car+r,fill="#0000FF") 

_, thresh = cv.threshold(im, 127, 255, 0)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
get_map(contours)

root.mainloop()
