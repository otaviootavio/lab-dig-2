from tkinter import *
from main import *
import serial

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.ser = serial.Serial('COM5', 115200, timeout=0, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_TWO, parity=serial.PARITY_EVEN) 
        
        self.master = master
        
        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        exitButton = Button(self, text="Exit", command=self.clickExitButton)

        # place button at (0,0)
        exitButton.place(x=0, y=0)
        
        openButton = Button(self, text="Open", command=self.connectButton)
        openButton.place(x=0, y=50)
        
        closeButton = Button(self, text="Close", command=self.closeButton)
        closeButton.place(x=0, y=100)
        
        closeButton = Text(self, text="Ola mundo!")
        closeButton.place(x=0, y=150)

    def clickExitButton(self):
        exit()
    
    def connectButton(self):
        abre_cofre(ser = self.ser)

    def closeButton(self):
        fecha_cofre(ser = self.ser)

root = Tk()
app = Window(root)

# set window title
root.wm_title("Tkinter window")

# Geometry size
root.geometry("320x200")

# show window
root.mainloop()