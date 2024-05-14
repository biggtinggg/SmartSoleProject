import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color
import csv
import asyncio
from bleak import BleakClient
from collections import deque
from PIL import ImageTk, Image

# Global parameters
# # Sole prototype
# data = np.array([415, 395, 180, 180, 190, 440, 480, 220, 230, 180])
# Sock prototype
data = np.array([337,238,269,192,150,352,278,172,172,107])

cond = False
# csv_file_name = " "

# Bluetooth parameters
address = "D5:B6:C5:1E:71:4B"
UID_1 = "19b10001-e8f2-537e-4f6c-d104768a1214"
UID_2 = "19b10001-e8f2-537e-4f6c-d104768a1215"

# Sensor parameters for each sensor //10 sensors being tested right now
# Board Prototype
# nominal_capacitance = [895, 395, 405, 155, 135, 155, 135, 140, 195, 195, 230, 370, 385, 355, 145, 120, 120, 125, 125, 200]

## Sole Prototype:
# nominal_capacitance = [415, 395, 180, 180, 190, 440, 480, 220, 230, 180]
# saturation_capacitance = [66, 66, 53, 53, 53, 65, 70, 60, 60, 53]

## Sock Prototype:
nominal_capacitance = [337,238,269,192,150,352,278,172,172,107]
saturation_capacitance = [37, 37, 26, 26, 26, 37, 37, 34, 34, 26]

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
    color2 = Color('black')
    
    # Calculate the mix ratio, which is indicative of how much the sensor has been pressed
    try:
        mix_ratio = (nominal_capacitance[sensor_no]-current_capacitance)/(nominal_capacitance[sensor_no]-saturation_capacitance[sensor_no])
    except TypeError:
        mix_ratio = 1

    # Calculate the R, G, B intensities to be used for colouring tkinter shapes
    r, g, b, a = color2.lerp(color1, mix_ratio)
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)
    # a_int = int((1-mix_ratio) * 255)

    # Converting the RGB intensities into colour hex codes without transparency
    # color_string = f"#{a_int:02x}{r_int:02x}{g_int:02x}{b_int:02x}"
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
        self.root.configure(background = 'white')
        self.root.geometry("1920x1080")    # Set the window size

        self.foreground = tk.Canvas(self.root, bg='light blue', width = 431, height = 846)
        self.foreground.place(x=0, y=0)

        # Instantiate data queue object
        self.sensor_data_queue = SensorDataQueue()

        # Create plot object on GUI
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title('Serial Data')
        self.ax.set_xlabel('Sample')
        self.ax.set_ylabel('Capacitance (pF)')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 900)

        self.lines1 = self.ax.plot([],[], color = 'r', label='Sensor 1')[0]
        self.lines2 = self.ax.plot([],[], color = 'b', label='Sensor 2')[0]
        self.lines3 = self.ax.plot([],[], color = 'g', label='Sensor 3')[0]
        self.lines4 = self.ax.plot([],[], color = 'c', label='Sensor 4')[0]
        self.lines5 = self.ax.plot([],[], color = 'm', label='Sensor 5')[0]
        self.lines6 = self.ax.plot([],[], color = 'y', label='Sensor 6')[0]
        self.lines7 = self.ax.plot([],[], color = 'k', label='Sensor 7')[0]
        self.lines8 = self.ax.plot([],[], color = 'tab:purple', label='Sensor 8')[0]
        self.lines9 = self.ax.plot([],[], color = 'tab:orange', label='Sensor 9')[0]
        self.lines10 = self.ax.plot([],[], color = 'tab:brown', label='Sensor 10')[0]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=500, y=10, width=800, height=800)
        self.canvas.draw()


        # Create color squares in the canvas
        # self.square_canvas1 = tk.Canvas(self.root, width=80, height=200, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas2 = tk.Canvas(self.root, width=80, height=200, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas3 = tk.Canvas(self.root, width=40, height=150, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas4 = tk.Canvas(self.root, width=40, height=150, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas5 = tk.Canvas(self.root, width=40, height=150, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas6 = tk.Canvas(self.root, width=100, height=200, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas7 = tk.Canvas(self.root, width=100, height=200, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas8 = tk.Canvas(self.root, width=80, height=80, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas9 = tk.Canvas(self.root, width=80, height=80, bd=0, highlightthickness=0, relief='ridge')
        # self.square_canvas10 = tk.Canvas(self.root, width=135, height=40, bd=0, highlightthickness=0, relief='ridge')

        # self.square_canvas1.place(x=215, y=600)
        # self.square_canvas2.place(x=120, y=580)
        # self.square_canvas3.place(x=205, y=415)
        # self.square_canvas4.place(x=150, y=415)
        # self.square_canvas5.place(x=95, y=415)
        # self.square_canvas6.place(x=185, y=200)
        # self.square_canvas7.place(x=70, y=200)
        # self.square_canvas8.place(x=215, y=105)
        # self.square_canvas9.place(x=110, y=105)
        # self.square_canvas10.place(x=145, y=50)

        self.square_canvas1 = self.foreground.create_rectangle(215, 600, 295, 720, fill="black")
        self.square_canvas2 = self.foreground.create_rectangle(120, 580, 200, 700, fill="black")
        self.square_canvas3 = self.foreground.create_rectangle(205, 415, 245, 565, fill="black")
        self.square_canvas4 = self.foreground.create_rectangle(150, 415, 190, 565, fill="black")
        self.square_canvas5 = self.foreground.create_rectangle(95, 415, 135, 565, fill="black")
        self.square_canvas6 = self.foreground.create_rectangle(185, 200, 285, 400, fill="black")
        self.square_canvas7 = self.foreground.create_rectangle(70, 200, 170, 400, fill="black")
        self.square_canvas8 = self.foreground.create_rectangle(215, 105, 295, 185, fill="black")
        self.square_canvas9 = self.foreground.create_rectangle(110, 105, 190, 185, fill="black")
        self.square_canvas10 = self.foreground.create_rectangle(145, 50, 280, 90, fill="black")

        self.foreground.itemconfig(self.square_canvas1, fill=interpolate_color(nominal_capacitance[0], 0))
        self.foreground.itemconfig(self.square_canvas2, fill=interpolate_color(nominal_capacitance[1], 1))
        self.foreground.itemconfig(self.square_canvas3, fill=interpolate_color(nominal_capacitance[2], 2))
        self.foreground.itemconfig(self.square_canvas4, fill=interpolate_color(nominal_capacitance[3], 3))
        self.foreground.itemconfig(self.square_canvas5, fill=interpolate_color(nominal_capacitance[4], 4))
        self.foreground.itemconfig(self.square_canvas6, fill=interpolate_color(nominal_capacitance[5], 5))
        self.foreground.itemconfig(self.square_canvas7, fill=interpolate_color(nominal_capacitance[6], 6))
        self.foreground.itemconfig(self.square_canvas8, fill=interpolate_color(nominal_capacitance[7], 7))
        self.foreground.itemconfig(self.square_canvas9, fill=interpolate_color(nominal_capacitance[8], 8))
        self.foreground.itemconfig(self.square_canvas10, fill=interpolate_color(nominal_capacitance[9], 9))

        self.square_tag1 = self.foreground.create_text(40, 100, text=str(data[0]), fill = 'red')
        # self.square_tag2 = self.foreground.create_text(40, 100, text=str(data[1]), fill = 'white')
        # self.square_tag3 = self.foreground.create_text(20, 75, text=str(data[2]), fill = 'white')
        # self.square_tag4 = self.foreground.create_text(20, 75, text=str(data[3]), fill = 'white')
        # self.square_tag5 = self.foreground.create_text(20, 75, text=str(data[4]), fill = 'white')
        # self.square_tag6 = self.foreground.create_text(50, 100, text=str(data[5]), fill = 'white')
        # self.square_tag7 = self.foreground.create_text(50, 100, text=str(data[6]), fill = 'white')
        # self.square_tag8 = self.foreground.create_text(40, 40, text=str(data[7]), fill = 'white')
        # self.square_tag9 = self.foreground.create_text(40, 40, text=str(data[8]), fill = 'white')
        # self.square_tag10 = self.foreground.create_text(67.5, 20, text=str(data[9]), fill = 'white')

        # Apply masking
        self.photoimage1 = ImageTk.PhotoImage(file="Sole Mask.png")
        self.mask = self.foreground.create_image(431/2, 846/2, image=self.photoimage1)
        # self.label = tk.Label(self.foreground, image=self.photoimage1)
        
        

        # Create buttons
        self.root.update()
        start=tk.Button(self.root, text = "Start", command=lambda: self.plot_start())
        # start=tk.Button(self.root, text = "Start")

        start.place(x=50, y=900)

        self.root.update()
        stop=tk.Button(self.root, text="Stop", command=lambda: self.plot_stop())
        # stop=tk.Button(self.root, text="Stop")
        stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=900)

        self.root.update()
        # save_button = tk.Button(self.root, text= "Save .csv file", padx = 40.0, pady = 50.0, command=lambda: save_csv())
        # save_button.place(x=stop.winfo_x() + stop.winfo_reqwidth() + 20, y=850)

        # Create entry widget
        e = tk.Entry(self.root)
        e.place(x=start.winfo_x(), y=start.winfo_y() + 50)
        e.insert(0, "Enter csv file name for saving (___.csv)")
        e.get()

    def plot_start(self):
        global cond 
        cond = True

    def plot_stop(self):
        global cond
        cond = False

    async def show(self):
        async with BleakClient(address) as client:
            await client.start_notify(UID_1, self.notification_handler1) 
            await client.start_notify(UID_2, self.notification_handler2)
            while True:
                self.root.update()

                self.ax.legend()

                self.foreground.itemconfig(self.square_canvas1, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(0),0))
                self.foreground.itemconfig(self.square_canvas2, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(1),1))
                self.foreground.itemconfig(self.square_canvas3, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(2),2))
                self.foreground.itemconfig(self.square_canvas4, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(3),3))
                self.foreground.itemconfig(self.square_canvas5, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(4),4))
                self.foreground.itemconfig(self.square_canvas6, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(5),5))
                self.foreground.itemconfig(self.square_canvas7, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(6),6))
                self.foreground.itemconfig(self.square_canvas8, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(7),7))
                self.foreground.itemconfig(self.square_canvas9, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(8),8))
                self.foreground.itemconfig(self.square_canvas10, fill=interpolate_color(self.sensor_data_queue.get_latest_datapoint(9),9))

                # self.square_canvas1.itemconfig(self.square_tag1, text=str(self.sensor_data_queue.get_latest_datapoint(0)))
                # self.square_canvas2.itemconfig(self.square_tag2, text=str(self.sensor_data_queue.get_latest_datapoint(1)))
                # self.square_canvas3.itemconfig(self.square_tag3, text=str(self.sensor_data_queue.get_latest_datapoint(2)))
                # self.square_canvas4.itemconfig(self.square_tag4, text=str(self.sensor_data_queue.get_latest_datapoint(3)))
                # self.square_canvas5.itemconfig(self.square_tag5, text=str(self.sensor_data_queue.get_latest_datapoint(4)))
                # self.square_canvas6.itemconfig(self.square_tag6, text=str(self.sensor_data_queue.get_latest_datapoint(5)))
                # self.square_canvas7.itemconfig(self.square_tag7, text=str(self.sensor_data_queue.get_latest_datapoint(6)))
                # self.square_canvas8.itemconfig(self.square_tag8, text=str(self.sensor_data_queue.get_latest_datapoint(7)))
                # self.square_canvas9.itemconfig(self.square_tag9, text=str(self.sensor_data_queue.get_latest_datapoint(8)))
                # self.square_canvas10.itemconfig(self.square_tag10, text=str(self.sensor_data_queue.get_latest_datapoint(9)))

                self.lines1.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(0))))
                self.lines1.set_ydata(self.sensor_data_queue.get_latest_data(0))
                self.lines2.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(1))))
                self.lines2.set_ydata(self.sensor_data_queue.get_latest_data(1))
                self.lines3.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(2))))
                self.lines3.set_ydata(self.sensor_data_queue.get_latest_data(2))
                self.lines4.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(3))))
                self.lines4.set_ydata(self.sensor_data_queue.get_latest_data(3))
                self.lines5.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(4))))
                self.lines5.set_ydata(self.sensor_data_queue.get_latest_data(4))
                self.lines6.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(5))))
                self.lines6.set_ydata(self.sensor_data_queue.get_latest_data(5))
                self.lines7.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(6))))
                self.lines7.set_ydata(self.sensor_data_queue.get_latest_data(6))
                self.lines8.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(7))))
                self.lines8.set_ydata(self.sensor_data_queue.get_latest_data(7))
                self.lines9.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(8))))
                self.lines9.set_ydata(self.sensor_data_queue.get_latest_data(8))
                self.lines10.set_xdata(np.arange(0,len(self.sensor_data_queue.get_latest_data(9))))
                self.lines10.set_ydata(self.sensor_data_queue.get_latest_data(9))

                self.canvas.draw()

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
        # print(type(self.sensor_data_queue.get_latest_datapoint(9)))
            
       
#----------------------------------------------------------------------------------------------------
# Main instatiation call
asyncio.run(start_window())