import tkinter as tk
from PIL import ImageTk, Image  # Picture import library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color

# Global parameters
data = np.array([0,0,0,0,0,0,0,0,0,0])
cond = False

# # Sensor parameters for one sensor
# nominal_capacitance = [200]
# saturation_capacitance = [44]

# Sensor parameters for each sensor //10 sensors being tested right now
nominal_capacitance = [230, 370, 385, 355, 145, 120, 120, 125, 125, 200]
saturation_capacitance = [70, 80, 90, 90, 50, 50, 50, 50, 50, 50]

# Plot data
def plot_data():
    global cond, data

    temp = np.array([])

    if (cond == True):
        ser.reset_input_buffer()
        a = ser.readline()
        temp_line = a.decode().split(",")

        if (data.shape[0]<100):
            index =0 
            temp = []
            for element in temp_line:
                try:
                    value = float(element)
                    temp = np.append(temp, value)
                except ValueError or float(element)==0.0:
                    try:
                        temp = np.append(temp,data[-1, index])
                    except IndexError:
                        temp = np.append(temp, 0.0)

                index += 1
                    
            # print(temp)
            data = np.vstack([data, temp])
            # print(data)
            try:
                square_canvas1.configure(background=interpolate_color(data[-1,0],0))
                square_canvas2.configure(background=interpolate_color(data[-1,1],1))
                square_canvas3.configure(background=interpolate_color(data[-1,2],2))
                square_canvas4.configure(background=interpolate_color(data[-1,3],3))
                square_canvas5.configure(background=interpolate_color(data[-1,4],4))
                square_canvas6.configure(background=interpolate_color(data[-1,5],5))
                square_canvas7.configure(background=interpolate_color(data[-1,6],6))
                square_canvas8.configure(background=interpolate_color(data[-1,7],7))
                square_canvas9.configure(background=interpolate_color(data[-1,8],8))
                square_canvas10.configure(background=interpolate_color(data[-1,9],9))
            except IndexError:
                square_canvas1.configure(background=interpolate_color(230, 0))
                square_canvas2.configure(background=interpolate_color(370, 1))
                square_canvas3.configure(background=interpolate_color(385, 2))
                square_canvas4.configure(background=interpolate_color(355, 3))
                square_canvas5.configure(background=interpolate_color(145, 4))
                square_canvas6.configure(background=interpolate_color(120, 5))
                square_canvas7.configure(background=interpolate_color(120, 6))
                square_canvas8.configure(background=interpolate_color(125, 7))
                square_canvas9.configure(background=interpolate_color(125, 8))
                square_canvas10.configure(background=interpolate_color(200, 9))
    
        else:
            index =0 
            temp = []
            ghost_data = data[-1]
            data[:99] = data[-99:]
            for element in temp_line:
                try:
                    value = float(element)
                    temp = np.append(temp, value)
                except ValueError or float(element)==0.0:
                    temp = np.append(temp,ghost_data[index])
                    pass
                index += 1

            data = np.vstack([data, temp])

            try:
                square_canvas1.configure(background=interpolate_color(data[-1,0],0))
                square_canvas2.configure(background=interpolate_color(data[-1,1],1))
                square_canvas3.configure(background=interpolate_color(data[-1,2],2))
                square_canvas4.configure(background=interpolate_color(data[-1,3],3))
                square_canvas5.configure(background=interpolate_color(data[-1,4],4))
                square_canvas6.configure(background=interpolate_color(data[-1,5],5))
                square_canvas7.configure(background=interpolate_color(data[-1,6],6))
                square_canvas8.configure(background=interpolate_color(data[-1,7],7))
                square_canvas9.configure(background=interpolate_color(data[-1,8],8))
                square_canvas10.configure(background=interpolate_color(data[-1,9],9))
            except IndexError:
                square_canvas1.configure(background=interpolate_color(230, 0))
                square_canvas2.configure(background=interpolate_color(370, 1))
                square_canvas3.configure(background=interpolate_color(385, 2))
                square_canvas4.configure(background=interpolate_color(355, 3))
                square_canvas5.configure(background=interpolate_color(145, 4))
                square_canvas6.configure(background=interpolate_color(120, 5))
                square_canvas7.configure(background=interpolate_color(120, 6))
                square_canvas8.configure(background=interpolate_color(125, 7))
                square_canvas9.configure(background=interpolate_color(125, 8))
                square_canvas10.configure(background=interpolate_color(200, 9))

        # print(data[:,0])

        # lines1.set_xdata(np.arange(0,data.shape[0]))
        # lines1.set_ydata([data[:,0]])
        
        # lines2.set_xdata(np.arange(0,data.shape[0]))
        # lines2.set_ydata([data[:,1]])


        canvas.draw()

    root.after(1, plot_data)

def plot_start():
    global cond
    cond = True
    ser.reset_input_buffer()

def plot_stop():
    global cond
    cond = False

# Interpolation of color from capacitance value
def interpolate_color(current_capacitance, sensor_no):
    color1 = Color('red')
    color2 = Color('green')
    
    mix_ratio = (nominal_capacitance[sensor_no]-current_capacitance)/(nominal_capacitance[sensor_no]-saturation_capacitance[sensor_no])

    r, g, b, a = color2.lerp(color1, mix_ratio)
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)

    # Without transparency
    color_string = f"#{r_int:02x}{g_int:02x}{b_int:02x}"

    return color_string

    

## Main GUI code
root = tk.Tk()
root.title('Smart Sole GUI')
root.configure(background = 'light blue')
root.geometry("700x500")    # Set the window size

# Create plot object on GUI
fig = Figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.set_title('Serial Data')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Capacitance (pF)')
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 800)
ax2.set_title('Serial Data')
ax2.set_xlabel('Sample')
ax2.set_ylabel('Capacitance (pF)')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 800)

lines1 = ax1.plot([],[])[0]
lines2 = ax2.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=10, y=10, width=500, height=400)
canvas.draw()

# Create color squares in the canvas
square_canvas1 = tk.Canvas(root, width=70, height=70)
square_canvas1.place(x=550, y=300)
square_canvas1.configure(background=interpolate_color(230, 0))

square_canvas2 = tk.Canvas(root, width=90, height=150)
square_canvas2.place(x=550, y=125)
square_canvas2.configure(background=interpolate_color(370, 1))

square_canvas3 = tk.Canvas(root, width=90, height=150)
square_canvas3.place(x=665, y=125)
square_canvas3.configure(background=interpolate_color(385, 2))

square_canvas4 = tk.Canvas(root, width=90, height=150)
square_canvas4.place(x=780, y=125)
square_canvas4.configure(background=interpolate_color(355, 3))

square_canvas5 = tk.Canvas(root, width=50, height=50)
square_canvas5.place(x=975, y=50)
square_canvas5.configure(background=interpolate_color(145, 4))

square_canvas6 = tk.Canvas(root, width=50, height=50)
square_canvas6.place(x=900, y=50)
square_canvas6.configure(background=interpolate_color(120, 5))

square_canvas7 = tk.Canvas(root, width=50, height=50)
square_canvas7.place(x=825, y=50)
square_canvas7.configure(background=interpolate_color(120, 6))

square_canvas8 = tk.Canvas(root, width=50, height=50)
square_canvas8.place(x=750, y=50)
square_canvas8.configure(background=interpolate_color(125, 7))

square_canvas9 = tk.Canvas(root, width=50, height=50)
square_canvas9.place(x=675, y=50)
square_canvas9.configure(background=interpolate_color(125, 8))

square_canvas10 = tk.Canvas(root, width=50, height=50)
square_canvas10.place(x=550, y=50)
square_canvas10.configure(background=interpolate_color(200, 9))

# Create buttons
root.update()
start=tk.Button(root, text = "Start", command=lambda: plot_start())
start.place(x=50, y=450)

root.update()
stop=tk.Button(root, text="Stop", command=lambda: plot_stop())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=450)

# Start serial plot
ser = serial.Serial('COM12', 115200)



root.after(1, plot_data)
root.mainloop()





# window = tkinter.Tk()
# window.title("Smart Sole GUI")
# window.iconbitmap('')

# # Create entry widget
# e = tkinter.Entry(window)
# e.pack()
# e.insert(0, "Enter command line")
# e.get()

# # Function definitions
# def myClick():
#     label3 = tkinter.Label(window, text=e.get())
#     label3.pack()

# # Creating a label widget
# # label1 = tkinter.Label(window, text = "Smart Sole GUI")

# # Creating a button
# button = tkinter.Button(window, text= "Toggle Foot Stencil Layout", padx = 40.0, pady = 50.0, command=myClick)
# button_quit = tkinter.Button(window, text="Exit Program", command=window.quit)

# # Display onto screen
# button.pack()
# button_quit.pack()

# window.mainloop()