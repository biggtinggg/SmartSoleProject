import tkinter as tk
from PIL import ImageTk, Image  # Picture import library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color

# Global parameters
data = np.array([])
cond = False
nominal_capacitance = 200
saturation_capacitance = 44

# Plot data
def plot_data():
    global cond, data

    if (cond == True):
        ser.reset_input_buffer()
        a = ser.readline()
        a.decode()
        print(a)
        if (len(data)<100):
            try:
                if float(a) == 0.0:
                    pass
                else:
                    data = np.append(data, float(a))
                    square_canvas.configure(background=interpolate_color(float(a)))
            except ValueError:
                pass
        else:
            try:
                if float(a) == 0.0:
                    pass
                else:
                    data[0:99] = data[1:100]
                    data[99] = float(a)
                    square_canvas.configure(background=interpolate_color(float(a)))
            except ValueError:
                pass


        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)


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
def interpolate_color(current_capacitance):
    color1 = Color('red')
    color2 = Color('green')
    
    mix_ratio = (nominal_capacitance-current_capacitance)/(nominal_capacitance-saturation_capacitance)

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
ax = fig.add_subplot(111)

ax.set_title('Serial Data')
ax.set_xlabel('Sample')
ax.set_ylabel('Capacitance (pF)')
ax.set_xlim(0, 100)
ax.set_ylim(0, 800)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=10, y=10, width=500, height=400)
canvas.draw()

# Create a square in the canvas
square_canvas = tk.Canvas(root, bg = 'white', width=50, height=50)
square_canvas.place(x=550, y=50)

square_canvas.create_rectangle((0, 0, 50, 50))
square_canvas.configure(background=interpolate_color(200))


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