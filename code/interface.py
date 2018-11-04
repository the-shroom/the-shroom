import tkinter as tk
import tkinter.ttk as ttk

import csv

import os
import sys
import serial
import time
import signal
import threading
from pathlib import Path

from collections import namedtuple

DATA_CSV = 'data.csv'

Relay = namedtuple('Relay', ['name', 'physical'])

relays = [ Relay('fans', 3),
 Relay('fogger', 4),
 Relay('peltier_warm', 5),
 Relay('peltier_cool', 6)]

relays_map = dict(list(zip([r.name for r in relays], relays)))
print(relays_map)

PORT = Path('/dev/cu.usbmodemFA131')
OP_SET = 1
ON = 1
OFF = 0


class Controller:
    def connect(self, serialport, speed = 9600):
        self.connection = serial.Serial(serialport, speed, timeout=0, stopbits=serial.STOPBITS_TWO)
        self.data = threading.Thread(target=self.printThread)
        self.data.start();

    def send_command(self, opcode=OP_SET, port=3, value=0):
        print('Sending command {} {}'.format(opcode, port, value))
        data = bytearray([opcode, port, value])
        self.connection.write(data)


    def close(self):
        # self.data.st
        self.connection.close()

    def printThread(self):
        print("local: starting log")
        file = open(DATA_CSV, 'a')
        writer = csv.writer(file)
        while self.connection.is_open:
            time.sleep(0.5)
            data = self.connection.readline()
            if len(data) > 0 and len(str(data.decode('ascii'))) > 0:
                try:
                    row = [float(d) for d in data.decode('ascii').split(',')[:-1]]
                    row.append(time.time())
                    if len(row) == 3:
                        writer.writerow(row)
                        file.flush()
                        print(row)
                except ValueError:
                    pass






def testswitch():
    print(relays)
    time.sleep(1)
    arduino = Controller()
    arduino.connect(str(PORT))
    for i in range(100):
        time.sleep(1)
        arduino.send_command(OP_SET, 5, ON)
        time.sleep(2)
        arduino.send_command(OP_SET, 4, ON)
        time.sleep(3)
        arduino.send_command(OP_SET, 5, OFF)

    arduino.close()


# def toggle():
#     if toggle_btn.config('relief')[-1] == 'sunken':
#         toggle_btn.config(relief="raised")
#     else:
#         toggle_btn.config(relief="sunken")


class App:
    def __init__(self, parent):
        self.parent = parent
        self.combo()

    def newselection(self, event):
        self.value_of_combo = self.box.get()
        print(self.value_of_combo)

    def combo(self):
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.parent, values=list(relays_map.keys()), textvariable=self.box_value)
        self.box.current(1)
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        # self.box

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot():
    print("plot")
    df = pd.read_csv(DATA_CSV, usecols=['humidity', 'temperature', 'time'])


def startGUI():
    def sendON():
        print("send on")
        print(relays_map[relay_box.box.get()])
        # print(type(relay_box.box.get()))
        target = relays_map[relay_box.box.get()]
        arduino.send_command(OP_SET,target.physical,ON)

    def sendOFF():
        print("send off")
        print(relay_box.box.get())
        target = relays_map[relay_box.box.get()]
        arduino.send_command(OP_SET, target.physical, OFF)

    # TODO:  on exit events
    def on_closing():
        arduino.close()

    arduino = Controller()
    arduino.connect(str(PORT))

    root = tk.Tk()
    root.minsize(500, 500)

    relay_box = App(root)
    frame = tk.Frame()
    btn_on  = tk.Button(root, text="On", width=12, relief="raised", command=sendON)
    btn_off = tk.Button(root, text="Off", width=12, relief="raised", command=sendOFF)

    btn_plot = tk.Button(root, text="Plot", width=12, relief="raised", command=plot)

    relay_box.box.grid(column=0, row=0)
    btn_off.grid(column=1, row=0)
    btn_on.grid(column=2, row=0)
    btn_plot.grid(columnspan=3, row=1)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # btn_on.pack(pady=5)
    # btn_off.pack(pady=5)
    root.mainloop()


# testswitch()
startGUI()