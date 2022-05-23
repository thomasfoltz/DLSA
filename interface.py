from tkinter import *

root = Tk()

# root window title and dimension
root.title("Stock Analysis Tool")
# Set geometry (widthxheight)
root.geometry('350x200')
 
# all widgets will be here
lbl = Label(root, text = "Work in progress")
lbl.grid()

def close():
    root.quit()

button = Button(root, text = "Close the Window", font=("Calibri", 14, "bold"))

# Execute Tkinter
root.mainloop()

