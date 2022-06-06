from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.QUIT = Button(self, text = "QUIT", fg = "red", command = self.quit, font=("Arial", 14, "bold")).pack({"side": "left"})
        self.hi_there = Button(self, text = "Hello", command = self.say_hi, font=("Arial", 14)).pack({"side": "left"})

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()
root.geometry("400x300")
root.title("Stock Analysis Tool")
app = Application(master=root)
app.mainloop()
root.destroy()

