import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color
import csv
import asyncio
from bleak import BleakClient
import threading
import tracemalloc
from collections import deque

# Global parameters
data = np.array([0,0,0,0,0,0,0,0,0,0])
cond = False
# csv_file_name = " "

# Bluetooth parameters
address = "D5:B6:C5:1E:71:4B"
UID_1 = "19b10001-e8f2-537e-4f6c-d104768a1214"
UID_2 = "19b10001-e8f2-537e-4f6c-d104768a1215"

# Sensor parameters for each sensor //10 sensors being tested right now
# Port 1
nominal_capacitance = [895, 395, 405, 155, 135, 155, 135, 140, 195, 195, 230, 370, 385, 355, 145, 120, 120, 125, 125, 200]
saturation_capacitance = [155, 95, 95, 60, 60, 60, 65, 65, 70, 70, 70, 80, 90, 90, 50, 50, 50, 50, 50, 50]

# #----------------------------------------------------------------------------------------------------
# # Button function definition for starting GUI program
# def plot_start():
#     global cond
#     cond = True

# #----------------------------------------------------------------------------------------------------
# # Button function definition for stopping GUI program
# def plot_stop():
#     global cond
#     cond = False
#----------------------------------------------------------------------------------------------------
# Interpolation of color from capacitance value
def interpolate_color(current_capacitance, sensor_no):
    color1 = Color('red')
    color2 = Color('green')
    
    # Calculate the mix ratio, which is indicative of how much the sensor has been pressed
    mix_ratio = (nominal_capacitance[sensor_no]-current_capacitance)/(nominal_capacitance[sensor_no]-saturation_capacitance[sensor_no])

    # Calculate the R, G, B intensities to be used for colouring tkinter shapes
    r, g, b, a = color2.lerp(color1, mix_ratio)
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)

    # Converting the RGB intensities into colour hex codes without transparency
    color_string = f"#{r_int:02x}{g_int:02x}{b_int:02x}"

    return color_string

#----------------------------------------------------------------------------------------------------
# Starts tkinter window
async def start_window():
    my_window = MyWindow(asyncio.get_event_loop())
    await my_window.show()

#----------------------------------------------------------------------------------------------------
# Queue class for storing sensor data
class SensorDataQueue:
    def __init__(self, max_len=100):
        self.max_len = max_len
        self.data = [deque(maxlen=max_len) for _ in range(10)]  # Create 10 queues

    def add_data(self, sensor_id, data):
        if 0 <= sensor_id < 10:
            self.data[sensor_id].append(data)

    def get_latest_data(self, sensor_id):
        if 0 <= sensor_id < 10:
            return self.data[sensor_id]
        else:
            return None
    
    def get_latest_datapoint(self, sensor_id):
        if 0 <= sensor_id < 10:
            if self.data[sensor_id]:  # Check if queue is not empty
                return self.data[sensor_id][-1]  # Return the last element (latest)
            else:
                return None  # Return None if queue is empty
        else:
            return None  # Return None for invalid sensor ID
        
    def print_data(self, sensor_id):
        if 0 <= sensor_id < 10:
            print(f"Sensor {sensor_id} data:", self.data[sensor_id])
        else:
            print(f"Invalid sensor ID: {sensor_id}")

    def get_all_data(self):
        return self.data

#----------------------------------------------------------------------------------------------------
# Tkinter Window class
class MyWindow(tk.Tk):

    global cond
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()

        self.root.title('Smart Sole GUI')
        self.root.configure(background = 'light blue')
        self.root.geometry("1600x1000")    # Set the window size

        # Instantiate data queue object
        self.sensor_data_queue = SensorDataQueue()

        # Create plot object on GUI
        fig = Figure()
        ax = fig.add_subplot(111)

        ax.set_title('Serial Data')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Capacitance (pF)')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 900)

        self.lines1 = ax.plot([],[], color = 'r', label='Sensor 1')[0]
        self.lines2 = ax.plot([],[], color = 'b', label='Sensor 2')[0]
        self.lines3 = ax.plot([],[], color = 'g', label='Sensor 3')[0]
        self.lines4 = ax.plot([],[], color = 'c', label='Sensor 4')[0]
        self.lines5 = ax.plot([],[], color = 'm', label='Sensor 5')[0]
        self.lines6 = ax.plot([],[], color = 'y', label='Sensor 6')[0]
        self.lines7 = ax.plot([],[], color = 'k', label='Sensor 7')[0]
        self.lines8 = ax.plot([],[], color = 'tab:purple', label='Sensor 8')[0]
        self.lines9 = ax.plot([],[], color = 'tab:orange', label='Sensor 9')[0]
        self.lines10 = ax.plot([],[], color = 'tab:brown', label='Sensor 10')[0]

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().place(x=500, y=10, width=800, height=800)
        canvas.draw()

        # Create color squares in the canvas
        square_canvas1 = tk.Canvas(self.root, width=250, height=150)
        square_canvas2 = tk.Canvas(self.root, width=120, height=60)
        square_canvas3 = tk.Canvas(self.root, width=120, height=60)
        square_canvas4 = tk.Canvas(self.root, width=40, height=150)
        square_canvas5 = tk.Canvas(self.root, width=40, height=150)
        square_canvas6 = tk.Canvas(self.root, width=40, height=150)
        square_canvas7 = tk.Canvas(self.root, width=40, height=150)
        square_canvas8 = tk.Canvas(self.root, width=40, height=150)
        square_canvas9 = tk.Canvas(self.root, width=70, height=70)
        square_canvas10 = tk.Canvas(self.root, width=70, height=70)

        square_canvas1.place(x=50, y=635)
        square_canvas2.place(x=190, y=560)
        square_canvas3.place(x=50, y=560)
        square_canvas4.place(x=270, y=395)
        square_canvas5.place(x=215, y=395)
        square_canvas6.place(x=160, y=395)
        square_canvas7.place(x=105, y=395)
        square_canvas8.place(x=50, y=395)
        square_canvas9.place(x=240, y=310)
        square_canvas10.place(x=145, y=310)

        square_canvas1.configure(background=interpolate_color(nominal_capacitance[0], 0))
        square_canvas2.configure(background=interpolate_color(nominal_capacitance[1], 1))
        square_canvas3.configure(background=interpolate_color(nominal_capacitance[2], 2))
        square_canvas4.configure(background=interpolate_color(nominal_capacitance[3], 3))
        square_canvas5.configure(background=interpolate_color(nominal_capacitance[4], 4))
        square_canvas6.configure(background=interpolate_color(nominal_capacitance[5], 5))
        square_canvas7.configure(background=interpolate_color(nominal_capacitance[6], 6))
        square_canvas8.configure(background=interpolate_color(nominal_capacitance[7], 7))
        square_canvas9.configure(background=interpolate_color(nominal_capacitance[8], 8))
        square_canvas10.configure(background=interpolate_color(nominal_capacitance[9], 9))

        self.square_tag1 = square_canvas1.create_text(125, 75, text=str(data[0]))
        self.square_tag2 = square_canvas2.create_text(60, 30, text=str(data[1]))
        self.square_tag3 = square_canvas3.create_text(60, 30, text=str(data[2]))
        self.square_tag4 = square_canvas4.create_text(20, 75, text=str(data[3]))
        self.square_tag5 = square_canvas5.create_text(20, 75, text=str(data[4]))
        self.square_tag6 = square_canvas6.create_text(20, 75, text=str(data[5]))
        self.square_tag7 = square_canvas7.create_text(20, 75, text=str(data[6]))
        self.square_tag8 = square_canvas8.create_text(20, 75, text=str(data[7]))
        self.square_tag9 = square_canvas9.create_text(35, 35, text=str(data[8]))
        self.square_tag10 = square_canvas10.create_text(35, 35, text=str(data[9]))


        # Create buttons
        self.root.update()
        start=tk.Button(self.root, text = "Start", command=lambda: self.plot_start())
        # start=tk.Button(self.root, text = "Start")

        start.place(x=50, y=850)

        self.root.update()
        stop=tk.Button(self.root, text="Stop", command=lambda: self.plot_stop())
        # stop=tk.Button(self.root, text="Stop")
        stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=850)

        self.root.update()
        # save_button = tk.Button(self.root, text= "Save .csv file", padx = 40.0, pady = 50.0, command=lambda: save_csv())
        # save_button.place(x=stop.winfo_x() + stop.winfo_reqwidth() + 20, y=850)

        # Create entry widget
        e = tk.Entry(self.root)
        e.place(x=start.winfo_x(), y=start.winfo_y() - 50)
        e.insert(0, "Enter csv file name for saving (___.csv)")
        e.get()

    def plot_start():
        global cond 
        cond = True

    def plot_stop():
        global cond
        cond = False

    async def show(self):
        async with BleakClient(address) as client:
            await client.start_notify(UID_1, self.notification_handler1) 
            await client.start_notify(UID_2, self.notification_handler2)
            while True:
                # self.root.update()
                if cond:
                    self.square_canvas1.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(0),0))
                    self.square_canvas2.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(1),1))
                    self.square_canvas3.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(2),2))
                    self.square_canvas8.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(3),3))
                    self.square_canvas7.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(4),4))
                    self.square_canvas6.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(5),5))
                    self.square_canvas5.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(6),6))
                    self.square_canvas4.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(7),7))
                    self.square_canvas9.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(8),8))
                    self.square_canvas10.configure(background=interpolate_color(self.sensor_data_queue.get_latest_datapoint(9),9))


                    self.square_canvas1.itemconfig(self.square_tag1, text=str(self.sensor_data_queue.get_latest_datapoint(0)))
                    self.square_canvas2.itemconfig(self.square_tag2, text=str(self.sensor_data_queue.get_latest_datapoint(1)))
                    self.square_canvas3.itemconfig(self.square_tag3, text=str(self.sensor_data_queue.get_latest_datapoint(2)))
                    self.square_canvas8.itemconfig(self.square_tag4, text=str(self.sensor_data_queue.get_latest_datapoint(3)))
                    self.square_canvas7.itemconfig(self.square_tag5, text=str(self.sensor_data_queue.get_latest_datapoint(4)))
                    self.square_canvas6.itemconfig(self.square_tag6, text=str(self.sensor_data_queue.get_latest_datapoint(5)))
                    self.square_canvas5.itemconfig(self.square_tag7, text=str(self.sensor_data_queue.get_latest_datapoint(6)))
                    self.square_canvas4.itemconfig(self.square_tag8, text=str(self.sensor_data_queue.get_latest_datapoint(7)))
                    self.square_canvas9.itemconfig(self.square_tag9, text=str(self.sensor_data_queue.get_latest_datapoint(8)))
                    self.square_canvas10.itemconfig(self.square_tag10, text=str(self.sensor_data_queue.get_latest_datapoint(9)))

                    self.root.update()

                await asyncio.sleep(0.1)

    async def notification_handler1(self, sender, data):
        values = data.decode("utf-8").split(",")
        index = 0    
        for element in values:
            try:
                value = int(element)
                self.sensor_data_queue.add_data(index, value)
                index += 1
            except ValueError or int(element)==0:
                pass

    async def notification_handler2(self, sender, data):
        values = data.decode("utf-8").split(",")
        index = 5    
        for element in values:
            try:
                value = int(element)
                self.sensor_data_queue.add_data(index, value)
                index += 1
            except ValueError or int(element)==0:
                pass
        self.sensor_data_queue.print_data(9)


asyncio.run(start_window())