import tkinter as tk
from PIL import ImageTk, Image  # Picture import library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color
import csv

# Global parameters
data = np.array([0,0,0,0,0,0,0,0,0,0])
cond = False
# csv_file_name = " "

# Sensor parameters for each sensor //10 sensors being tested right now
# Port 1
nominal_capacitance = [230, 370, 385, 355, 145, 120, 120, 125, 125, 200]
saturation_capacitance = [70, 80, 90, 90, 50, 50, 50, 50, 50, 50]

# Plot data
def plot_data():
    global cond, data

    # Display legend || Disable if buggy
    ax.legend()


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

                # Catch exceptions that would otherwise cause discrepancies in the data
                except ValueError or float(element)==0.0:
                    try:
                        temp = np.append(temp,data[-1, index])
                    except IndexError:
                        temp = np.append(temp, 0.0)

                index += 1
                    
            # print(temp)
            data = np.vstack([data, temp])
            y_values = data.copy()
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

                square_canvas1.itemconfig(square_tag1, text=str(data[-1,0]))
                square_canvas2.itemconfig(square_tag2, text=str(data[-1,1]))
                square_canvas3.itemconfig(square_tag3, text=str(data[-1,2]))
                square_canvas4.itemconfig(square_tag4, text=str(data[-1,3]))
                square_canvas5.itemconfig(square_tag5, text=str(data[-1,4]))
                square_canvas6.itemconfig(square_tag6, text=str(data[-1,5]))
                square_canvas7.itemconfig(square_tag7, text=str(data[-1,6]))
                square_canvas8.itemconfig(square_tag8, text=str(data[-1,7]))
                square_canvas9.itemconfig(square_tag9, text=str(data[-1,8]))
                square_canvas10.itemconfig(square_tag10, text=str(data[-1,9]))
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
            for element in temp_line:
                try:
                    value = float(element)
                    temp = np.append(temp, value)

                # Catch exceptions that would otherwise cause discrepancies in the data
                except ValueError or float(element)==0.0:
                    temp = np.append(temp,data[-1, index])
                    pass
                index += 1

            data = np.vstack([data, temp])
            y_values = data[-100:]

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

                square_canvas1.itemconfig(square_tag1, text=str(data[-1,0]))
                square_canvas2.itemconfig(square_tag2, text=str(data[-1,1]))
                square_canvas3.itemconfig(square_tag3, text=str(data[-1,2]))
                square_canvas4.itemconfig(square_tag4, text=str(data[-1,3]))
                square_canvas5.itemconfig(square_tag5, text=str(data[-1,4]))
                square_canvas6.itemconfig(square_tag6, text=str(data[-1,5]))
                square_canvas7.itemconfig(square_tag7, text=str(data[-1,6]))
                square_canvas8.itemconfig(square_tag8, text=str(data[-1,7]))
                square_canvas9.itemconfig(square_tag9, text=str(data[-1,8]))
                square_canvas10.itemconfig(square_tag10, text=str(data[-1,9]))
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
 
        lines1.set_xdata(np.arange(0,y_values.shape[0]))
        lines1.set_ydata([y_values[:,0]])
        lines2.set_xdata(np.arange(0,y_values.shape[0]))
        lines2.set_ydata([y_values[:,1]])
        lines3.set_xdata(np.arange(0,y_values.shape[0]))
        lines3.set_ydata([y_values[:,2]])
        lines4.set_xdata(np.arange(0,y_values.shape[0]))
        lines4.set_ydata([y_values[:,3]])
        lines5.set_xdata(np.arange(0,y_values.shape[0]))
        lines5.set_ydata([y_values[:,4]])
        lines6.set_xdata(np.arange(0,y_values.shape[0]))
        lines6.set_ydata([y_values[:,5]])
        lines7.set_xdata(np.arange(0,y_values.shape[0]))
        lines7.set_ydata([y_values[:,6]])
        lines8.set_xdata(np.arange(0,y_values.shape[0]))
        lines8.set_ydata([y_values[:,7]])
        lines9.set_xdata(np.arange(0,y_values.shape[0]))
        lines9.set_ydata([y_values[:,8]])
        lines10.set_xdata(np.arange(0,y_values.shape[0]))
        lines10.set_ydata([y_values[:,9]])
        canvas.draw()

    root.after(1, plot_data)

# Save data into a .csv file
def save_csv():
    global data

    csv_file_name = tk.Label.config(text=e.get())

    with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        string_array = np.array2string(data)
        writer.writerows(string_array)

    print("Data collection complete!")
    csv_file_name.close()


# Button function definitions
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

    

## Main GUI code
root = tk.Tk()
root.title('Smart Sole GUI')
root.configure(background = 'light blue')
root.geometry("1600x1000")    # Set the window size

# Create plot object on GUI
fig = Figure()
ax = fig.add_subplot(111)


ax.set_title('Serial Data')
ax.set_xlabel('Sample')
ax.set_ylabel('Capacitance (pF)')
ax.set_xlim(0, 100)
ax.set_ylim(0, 600)


lines1 = ax.plot([],[], color = 'r', label='Sensor 11')[0]
lines2 = ax.plot([],[], color = 'b', label='Sensor 12')[0]
lines3 = ax.plot([],[], color = 'g', label='Sensor 13')[0]
lines4 = ax.plot([],[], color = 'c', label='Sensor 14')[0]
lines5 = ax.plot([],[], color = 'm', label='Sensor 15')[0]
lines6 = ax.plot([],[], color = 'y', label='Sensor 16')[0]
lines7 = ax.plot([],[], color = 'k', label='Sensor 17')[0]
lines8 = ax.plot([],[], color = 'tab:purple', label='Sensor 18')[0]
lines9 = ax.plot([],[], color = 'tab:orange', label='Sensor 19')[0]
lines10 = ax.plot([],[], color = 'tab:brown', label='Sensor 20')[0]


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=500, y=10, width=800, height=800)
canvas.draw()

# Create color squares in the canvas
square_canvas1 = tk.Canvas(root, width=70, height=70)
square_canvas2 = tk.Canvas(root, width=120, height=250)
square_canvas3 = tk.Canvas(root, width=120, height=250)
square_canvas4 = tk.Canvas(root, width=120, height=250)
square_canvas5 = tk.Canvas(root, width=50, height=50)
square_canvas6 = tk.Canvas(root, width=50, height=50)
square_canvas7 = tk.Canvas(root, width=50, height=50)
square_canvas8 = tk.Canvas(root, width=50, height=50)
square_canvas9 = tk.Canvas(root, width=50, height=50)
square_canvas10 = tk.Canvas(root, width=50, height=50)

square_canvas1.place(x=50, y=425)
square_canvas2.place(x=50, y=125)
square_canvas3.place(x=195, y=125)
square_canvas4.place(x=340, y=125)
square_canvas5.place(x=425, y=50)
square_canvas6.place(x=350, y=50)
square_canvas7.place(x=275, y=50)
square_canvas8.place(x=200, y=50)
square_canvas9.place(x=125, y=50)
square_canvas10.place(x=50, y=50)

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

square_tag1 = square_canvas1.create_text(35, 35, text=str(data[0]))
square_tag2 = square_canvas2.create_text(60, 125, text=str(data[1]))
square_tag3 = square_canvas3.create_text(60, 125, text=str(data[2]))
square_tag4 = square_canvas4.create_text(60, 125, text=str(data[3]))
square_tag5 = square_canvas5.create_text(25, 25, text=str(data[4]))
square_tag6 = square_canvas6.create_text(25, 25, text=str(data[5]))
square_tag7 = square_canvas7.create_text(25, 25, text=str(data[6]))
square_tag8 = square_canvas8.create_text(25, 25, text=str(data[7]))
square_tag9 = square_canvas9.create_text(25, 25, text=str(data[8]))
square_tag10 = square_canvas10.create_text(25, 25, text=str(data[9]))

# Create buttons
root.update()
start=tk.Button(root, text = "Start", command=lambda: plot_start())
start.place(x=50, y=850)

root.update()
stop=tk.Button(root, text="Stop", command=lambda: plot_stop())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=850)

root.update()
save_button = tk.Button(root, text= "Save .csv file", padx = 40.0, pady = 50.0, command=lambda: save_csv())
save_button.place(x=stop.winfo_x() + stop.winfo_reqwidth() + 20, y=850)

# Create entry widget
e = tk.Entry(root)
e.place(x=start.winfo_x(), y=start.winfo_y() - 50)
e.insert(0, "Enter csv file name for saving (___.csv)")
e.get()

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