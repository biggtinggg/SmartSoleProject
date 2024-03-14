import tkinter as tk
from PIL import ImageTk, Image  # Picture import library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import serial 
from generativepy.color import Color
import csv

# Global parameters
data = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
cond = False
# csv_file_name = " "

# Sensor parameters for each sensor //10 sensors being tested right now
# Port 1
nominal_capacitance = [895, 395, 405, 155, 135, 155, 135, 140, 195, 195, 230, 370, 385, 355, 145, 120, 120, 125, 125, 200]
saturation_capacitance = [155, 95, 95, 60, 60, 60, 65, 65, 70, 70, 70, 80, 90, 90, 50, 50, 50, 50, 50, 50]

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
                square_canvas8.configure(background=interpolate_color(data[-1,3],3))
                square_canvas7.configure(background=interpolate_color(data[-1,4],4))
                square_canvas6.configure(background=interpolate_color(data[-1,5],5))
                square_canvas5.configure(background=interpolate_color(data[-1,6],6))
                square_canvas4.configure(background=interpolate_color(data[-1,7],7))
                square_canvas9.configure(background=interpolate_color(data[-1,8],8))
                square_canvas10.configure(background=interpolate_color(data[-1,9],9))
                square_canvas11.configure(background=interpolate_color(data[-1,10],10))
                square_canvas12.configure(background=interpolate_color(data[-1,11],11))
                square_canvas13.configure(background=interpolate_color(data[-1,12],12))
                square_canvas14.configure(background=interpolate_color(data[-1,13],13))
                square_canvas15.configure(background=interpolate_color(data[-1,14],14))
                square_canvas16.configure(background=interpolate_color(data[-1,15],15))
                square_canvas17.configure(background=interpolate_color(data[-1,16],16))
                square_canvas18.configure(background=interpolate_color(data[-1,17],17))
                square_canvas19.configure(background=interpolate_color(data[-1,18],18))
                square_canvas20.configure(background=interpolate_color(data[-1,19],19))

                square_canvas1.itemconfig(square_tag1, text=str(data[-1,0]))
                square_canvas2.itemconfig(square_tag2, text=str(data[-1,1]))
                square_canvas3.itemconfig(square_tag3, text=str(data[-1,2]))
                square_canvas8.itemconfig(square_tag4, text=str(data[-1,3]))
                square_canvas7.itemconfig(square_tag5, text=str(data[-1,4]))
                square_canvas6.itemconfig(square_tag6, text=str(data[-1,5]))
                square_canvas5.itemconfig(square_tag7, text=str(data[-1,6]))
                square_canvas4.itemconfig(square_tag8, text=str(data[-1,7]))
                square_canvas9.itemconfig(square_tag9, text=str(data[-1,8]))
                square_canvas10.itemconfig(square_tag10, text=str(data[-1,9]))
                square_canvas11.itemconfig(square_tag1, text=str(data[-1,10]))
                square_canvas12.itemconfig(square_tag2, text=str(data[-1,11]))
                square_canvas13.itemconfig(square_tag3, text=str(data[-1,12]))
                square_canvas14.itemconfig(square_tag4, text=str(data[-1,13]))
                square_canvas15.itemconfig(square_tag5, text=str(data[-1,14]))
                square_canvas16.itemconfig(square_tag6, text=str(data[-1,15]))
                square_canvas17.itemconfig(square_tag7, text=str(data[-1,16]))
                square_canvas18.itemconfig(square_tag8, text=str(data[-1,17]))
                square_canvas19.itemconfig(square_tag9, text=str(data[-1,18]))
                square_canvas20.itemconfig(square_tag10, text=str(data[-1,19]))
            except IndexError:
                square_canvas1.configure(background=interpolate_color(nominal_capacitance[0], 0))
                square_canvas2.configure(background=interpolate_color(nominal_capacitance[1], 1))
                square_canvas3.configure(background=interpolate_color(nominal_capacitance[2], 2))
                square_canvas8.configure(background=interpolate_color(nominal_capacitance[3], 3))
                square_canvas7.configure(background=interpolate_color(nominal_capacitance[4], 4))
                square_canvas6.configure(background=interpolate_color(nominal_capacitance[5], 5))
                square_canvas5.configure(background=interpolate_color(nominal_capacitance[6], 6))
                square_canvas4.configure(background=interpolate_color(nominal_capacitance[7], 7))
                square_canvas9.configure(background=interpolate_color(nominal_capacitance[8], 8))
                square_canvas10.configure(background=interpolate_color(nominal_capacitance[9], 9))
                square_canvas11.configure(background=interpolate_color(nominal_capacitance[10], 10))
                square_canvas12.configure(background=interpolate_color(nominal_capacitance[11], 11))
                square_canvas13.configure(background=interpolate_color(nominal_capacitance[12], 12))
                square_canvas14.configure(background=interpolate_color(nominal_capacitance[13], 13))
                square_canvas15.configure(background=interpolate_color(nominal_capacitance[14], 14))
                square_canvas16.configure(background=interpolate_color(nominal_capacitance[15], 15))
                square_canvas17.configure(background=interpolate_color(nominal_capacitance[16], 16))
                square_canvas18.configure(background=interpolate_color(nominal_capacitance[17], 17))
                square_canvas19.configure(background=interpolate_color(nominal_capacitance[18], 18))
                square_canvas20.configure(background=interpolate_color(nominal_capacitance[19], 19))

    
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
                square_canvas8.configure(background=interpolate_color(data[-1,3],3))
                square_canvas7.configure(background=interpolate_color(data[-1,4],4))
                square_canvas6.configure(background=interpolate_color(data[-1,5],5))
                square_canvas5.configure(background=interpolate_color(data[-1,6],6))
                square_canvas4.configure(background=interpolate_color(data[-1,7],7))
                square_canvas9.configure(background=interpolate_color(data[-1,8],8))
                square_canvas10.configure(background=interpolate_color(data[-1,9],9))
                square_canvas11.configure(background=interpolate_color(data[-1,10],10))
                square_canvas12.configure(background=interpolate_color(data[-1,11],11))
                square_canvas13.configure(background=interpolate_color(data[-1,12],12))
                square_canvas14.configure(background=interpolate_color(data[-1,13],13))
                square_canvas15.configure(background=interpolate_color(data[-1,14],14))
                square_canvas16.configure(background=interpolate_color(data[-1,15],15))
                square_canvas17.configure(background=interpolate_color(data[-1,16],16))
                square_canvas18.configure(background=interpolate_color(data[-1,17],17))
                square_canvas19.configure(background=interpolate_color(data[-1,18],18))
                square_canvas20.configure(background=interpolate_color(data[-1,19],19))

                square_canvas1.itemconfig(square_tag1, text=str(data[-1,0]))
                square_canvas2.itemconfig(square_tag2, text=str(data[-1,1]))
                square_canvas3.itemconfig(square_tag3, text=str(data[-1,2]))
                square_canvas8.itemconfig(square_tag4, text=str(data[-1,3]))
                square_canvas7.itemconfig(square_tag5, text=str(data[-1,4]))
                square_canvas6.itemconfig(square_tag6, text=str(data[-1,5]))
                square_canvas5.itemconfig(square_tag7, text=str(data[-1,6]))
                square_canvas4.itemconfig(square_tag8, text=str(data[-1,7]))
                square_canvas9.itemconfig(square_tag9, text=str(data[-1,8]))
                square_canvas10.itemconfig(square_tag10, text=str(data[-1,9]))
                square_canvas11.itemconfig(square_tag1, text=str(data[-1,10]))
                square_canvas12.itemconfig(square_tag2, text=str(data[-1,11]))
                square_canvas13.itemconfig(square_tag3, text=str(data[-1,12]))
                square_canvas14.itemconfig(square_tag4, text=str(data[-1,13]))
                square_canvas15.itemconfig(square_tag5, text=str(data[-1,14]))
                square_canvas16.itemconfig(square_tag6, text=str(data[-1,15]))
                square_canvas17.itemconfig(square_tag7, text=str(data[-1,16]))
                square_canvas18.itemconfig(square_tag8, text=str(data[-1,17]))
                square_canvas19.itemconfig(square_tag9, text=str(data[-1,18]))
                square_canvas20.itemconfig(square_tag10, text=str(data[-1,19]))
            except IndexError:
                square_canvas1.configure(background=interpolate_color(nominal_capacitance[0], 0))
                square_canvas2.configure(background=interpolate_color(nominal_capacitance[1], 1))
                square_canvas3.configure(background=interpolate_color(nominal_capacitance[2], 2))
                square_canvas8.configure(background=interpolate_color(nominal_capacitance[3], 3))
                square_canvas7.configure(background=interpolate_color(nominal_capacitance[4], 4))
                square_canvas6.configure(background=interpolate_color(nominal_capacitance[5], 5))
                square_canvas5.configure(background=interpolate_color(nominal_capacitance[6], 6))
                square_canvas4.configure(background=interpolate_color(nominal_capacitance[7], 7))
                square_canvas9.configure(background=interpolate_color(nominal_capacitance[8], 8))
                square_canvas10.configure(background=interpolate_color(nominal_capacitance[9], 9))
                square_canvas11.configure(background=interpolate_color(nominal_capacitance[10], 10))
                square_canvas12.configure(background=interpolate_color(nominal_capacitance[11], 11))
                square_canvas13.configure(background=interpolate_color(nominal_capacitance[12], 12))
                square_canvas14.configure(background=interpolate_color(nominal_capacitance[13], 13))
                square_canvas15.configure(background=interpolate_color(nominal_capacitance[14], 14))
                square_canvas16.configure(background=interpolate_color(nominal_capacitance[15], 15))
                square_canvas17.configure(background=interpolate_color(nominal_capacitance[16], 16))
                square_canvas18.configure(background=interpolate_color(nominal_capacitance[17], 17))
                square_canvas19.configure(background=interpolate_color(nominal_capacitance[18], 18))
                square_canvas20.configure(background=interpolate_color(nominal_capacitance[19], 19))
 
        lines1.set_xdata(np.arange(0,y_values.shape[0]))
        lines1.set_ydata([y_values[:,0]])
        lines2.set_xdata(np.arange(0,y_values.shape[0]))
        lines2.set_ydata([y_values[:,1]])
        lines3.set_xdata(np.arange(0,y_values.shape[0]))
        lines3.set_ydata([y_values[:,2]])
        lines8.set_xdata(np.arange(0,y_values.shape[0]))
        lines8.set_ydata([y_values[:,3]])
        lines7.set_xdata(np.arange(0,y_values.shape[0]))
        lines7.set_ydata([y_values[:,4]])
        lines6.set_xdata(np.arange(0,y_values.shape[0]))
        lines6.set_ydata([y_values[:,5]])
        lines5.set_xdata(np.arange(0,y_values.shape[0]))
        lines5.set_ydata([y_values[:,6]])
        lines4.set_xdata(np.arange(0,y_values.shape[0]))
        lines4.set_ydata([y_values[:,7]])
        lines9.set_xdata(np.arange(0,y_values.shape[0]))
        lines9.set_ydata([y_values[:,8]])
        lines10.set_xdata(np.arange(0,y_values.shape[0]))
        lines10.set_ydata([y_values[:,9]])
        lines11.set_xdata(np.arange(0,y_values.shape[0]))
        lines11.set_ydata([y_values[:,10]])
        lines12.set_xdata(np.arange(0,y_values.shape[0]))
        lines12.set_ydata([y_values[:,11]])
        lines13.set_xdata(np.arange(0,y_values.shape[0]))
        lines13.set_ydata([y_values[:,12]])
        lines14.set_xdata(np.arange(0,y_values.shape[0]))
        lines14.set_ydata([y_values[:,13]])
        lines15.set_xdata(np.arange(0,y_values.shape[0]))
        lines15.set_ydata([y_values[:,14]])
        lines16.set_xdata(np.arange(0,y_values.shape[0]))
        lines16.set_ydata([y_values[:,15]])
        lines17.set_xdata(np.arange(0,y_values.shape[0]))
        lines17.set_ydata([y_values[:,16]])
        lines18.set_xdata(np.arange(0,y_values.shape[0]))
        lines18.set_ydata([y_values[:,17]])
        lines19.set_xdata(np.arange(0,y_values.shape[0]))
        lines19.set_ydata([y_values[:,18]])
        lines20.set_xdata(np.arange(0,y_values.shape[0]))
        lines20.set_ydata([y_values[:,19]])
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
ax.set_ylim(0, 900)


lines1 = ax.plot([],[], color = 'r', label='Sensor 1')[0]
lines2 = ax.plot([],[], color = 'b', label='Sensor 2')[0]
lines3 = ax.plot([],[], color = 'g', label='Sensor 3')[0]
lines4 = ax.plot([],[], color = 'c', label='Sensor 4')[0]
lines5 = ax.plot([],[], color = 'm', label='Sensor 5')[0]
lines6 = ax.plot([],[], color = 'y', label='Sensor 6')[0]
lines7 = ax.plot([],[], color = 'k', label='Sensor 7')[0]
lines8 = ax.plot([],[], color = 'tab:purple', label='Sensor 8')[0]
lines9 = ax.plot([],[], color = 'tab:orange', label='Sensor 9')[0]
lines10 = ax.plot([],[], color = 'tab:brown', label='Sensor 10')[0]
lines11 = ax.plot([],[], color = 'r', label='Sensor 11')[0]
lines12 = ax.plot([],[], color = 'b', label='Sensor 12')[0]
lines13 = ax.plot([],[], color = 'g', label='Sensor 13')[0]
lines14 = ax.plot([],[], color = 'c', label='Sensor 14')[0]
lines15 = ax.plot([],[], color = 'm', label='Sensor 15')[0]
lines16 = ax.plot([],[], color = 'y', label='Sensor 16')[0]
lines17 = ax.plot([],[], color = 'k', label='Sensor 17')[0]
lines18 = ax.plot([],[], color = 'tab:purple', label='Sensor 18')[0]
lines19 = ax.plot([],[], color = 'tab:orange', label='Sensor 19')[0]
lines20 = ax.plot([],[], color = 'tab:brown', label='Sensor 20')[0]


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=500, y=10, width=800, height=800)
canvas.draw()

# Create color squares in the canvas
square_canvas1 = tk.Canvas(root, width=250, height=150)
square_canvas2 = tk.Canvas(root, width=120, height=60)
square_canvas3 = tk.Canvas(root, width=120, height=60)
square_canvas4 = tk.Canvas(root, width=40, height=150)
square_canvas5 = tk.Canvas(root, width=40, height=150)
square_canvas6 = tk.Canvas(root, width=40, height=150)
square_canvas7 = tk.Canvas(root, width=40, height=150)
square_canvas8 = tk.Canvas(root, width=40, height=150)
square_canvas9 = tk.Canvas(root, width=70, height=70)
square_canvas10 = tk.Canvas(root, width=70, height=70)
square_canvas11 = tk.Canvas(root, width=70, height=70)
square_canvas12 = tk.Canvas(root, width=80, height=200)
square_canvas13 = tk.Canvas(root, width=80, height=200)
square_canvas14 = tk.Canvas(root, width=80, height=200)
square_canvas15 = tk.Canvas(root, width=30, height=30)
square_canvas16 = tk.Canvas(root, width=30, height=30)
square_canvas17 = tk.Canvas(root, width=30, height=30)
square_canvas18 = tk.Canvas(root, width=30, height=30)
square_canvas19 = tk.Canvas(root, width=30, height=30)
square_canvas20 = tk.Canvas(root, width=30, height=30)

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
square_canvas11.place(x=50, y=310)
square_canvas12.place(x=50, y=95)
square_canvas13.place(x=145, y=95)
square_canvas14.place(x=240, y=95)
square_canvas15.place(x=275, y=50)
square_canvas16.place(x=230, y=50)
square_canvas17.place(x=185, y=50)
square_canvas18.place(x=140, y=50)
square_canvas19.place(x=95, y=50)
square_canvas20.place(x=50, y=50)

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
square_canvas11.configure(background=interpolate_color(nominal_capacitance[10], 10))
square_canvas12.configure(background=interpolate_color(nominal_capacitance[11], 11))
square_canvas13.configure(background=interpolate_color(nominal_capacitance[12], 12))
square_canvas14.configure(background=interpolate_color(nominal_capacitance[13], 13))
square_canvas15.configure(background=interpolate_color(nominal_capacitance[14], 14))
square_canvas16.configure(background=interpolate_color(nominal_capacitance[15], 15))
square_canvas17.configure(background=interpolate_color(nominal_capacitance[16], 16))
square_canvas18.configure(background=interpolate_color(nominal_capacitance[17], 17))
square_canvas19.configure(background=interpolate_color(nominal_capacitance[18], 18))
square_canvas20.configure(background=interpolate_color(nominal_capacitance[19], 19))

square_tag1 = square_canvas1.create_text(125, 75, text=str(data[0]))
square_tag2 = square_canvas2.create_text(60, 30, text=str(data[1]))
square_tag3 = square_canvas3.create_text(60, 30, text=str(data[2]))
square_tag4 = square_canvas4.create_text(20, 75, text=str(data[3]))
square_tag5 = square_canvas5.create_text(20, 75, text=str(data[4]))
square_tag6 = square_canvas6.create_text(20, 75, text=str(data[5]))
square_tag7 = square_canvas7.create_text(20, 75, text=str(data[6]))
square_tag8 = square_canvas8.create_text(20, 75, text=str(data[7]))
square_tag9 = square_canvas9.create_text(35, 35, text=str(data[8]))
square_tag10 = square_canvas10.create_text(35, 35, text=str(data[9]))
square_tag11 = square_canvas11.create_text(35, 35, text=str(data[10]))
square_tag12 = square_canvas12.create_text(40, 100, text=str(data[11]))
square_tag13 = square_canvas13.create_text(40, 100, text=str(data[12]))
square_tag14 = square_canvas14.create_text(40, 100, text=str(data[13]))
square_tag15 = square_canvas15.create_text(15, 15, text=str(data[14]))
square_tag16 = square_canvas16.create_text(15, 15, text=str(data[15]))
square_tag17 = square_canvas17.create_text(15, 15, text=str(data[16]))
square_tag18 = square_canvas18.create_text(15, 15, text=str(data[17]))
square_tag19 = square_canvas19.create_text(15, 15, text=str(data[18]))
square_tag20 = square_canvas20.create_text(15, 15, text=str(data[19]))

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