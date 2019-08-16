# Import some funtions from TkInter
from tkinter import *
import tkinter.font
import tkinter.ttk

# Import some functions from Pillow
from PIL import ImageTk, Image

# Import the PyQRCode library
import pyqrcode

# Imports some Python Date/Time functions
import time
import datetime

# Imports the PyOTA library
from iota import Iota
from iota import Address

# Define the Exit function
def exitGUI():

    root.destroy()


# URL to IOTA fullnode used when checking balance
iotaNode = "https://nodes.thetangle.org:443"


# Create an IOTA object
api = Iota(iotaNode, "")


# String representation of IOTA address to be rendered as QR code 
addr = 'GTZUHQSPRAQCTSQBZEEMLZPQUPAA9LPLGWCKFNEVKBINXEXZRACVKKKCYPWPKH9AWLGJHPLOZZOYTALAWOVSIJIYVZ'

# IOTA address to be checked for new light funds 
# IOTA addresses can be created using the IOTA Wallet
address = [Address(b'GTZUHQSPRAQCTSQBZEEMLZPQUPAA9LPLGWCKFNEVKBINXEXZRACVKKKCYPWPKH9AWLGJHPLOZZOYTALAWOVSIJIYVZ')]



# Define main form as root 
root = Tk()

# Set the form background to white
root.config(background="white")

# TkInter font to be used in GUI
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

# Set main form to full screen
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())


# Define mainFrame
mainFrame = tkinter.Frame(root)
mainFrame.config(background="white")
mainFrame.place(relx=0.5, rely=0.5, anchor=CENTER)


# Create and render the QR code
code = pyqrcode.create(addr)
code_xbm = code.xbm(scale=3)
qrframe = tkinter.Frame(mainFrame)
qrframe.grid(row=0,column=0,rowspan=3)
code_bmp = tkinter.BitmapImage(data=code_xbm)
code_bmp.config(background="white")
qrcode = tkinter.Label(qrframe, image=code_bmp)
qrcode.grid(row=0, column=0)


# Create and render logo
# Make sure you download and place the "iota_logo75.jpg" file in the same folder as your python file.
# The logofile can be dowloaded from: https://github.com/huggre/pay_the_light_gui/blob/master/iota_logo75.jpg
path = "iota_logo75.jpg"
img = ImageTk.PhotoImage(Image.open(path))
iotalogo = tkinter.Label(mainFrame, image = img, borderwidth = 0)
iotalogo.grid(row=0,column=1)


# Create and render timer
timeText = tkinter.Label(mainFrame, text="", font=("Helvetica", 50))
timeText.config(background='white')
timeText.grid(row=1,column=1)


# Create and render Exit button
exitButton = Button(mainFrame, text='Exit', font=myFont, command=exitGUI, bg='white', height=1, width=10)
exitButton.grid(row=2,column=1)


# Create and render balance text
balanceTextFrame = tkinter.Frame(mainFrame)
balanceTextFrame.grid(row=3,column=0,columnspan=2)
balanceText = tkinter.Label(balanceTextFrame, text="", font=("Helvetica", 12))
balanceText.config(background='white')
balanceText.grid(row=3,column=0)


# Create and render progress bar
progFrame = tkinter.Frame(mainFrame)
progFrame.grid(row=4,column=0,columnspan=2)
mpb = tkinter.ttk.Progressbar(progFrame,orient ="horizontal",length = 435, mode ="determinate")
mpb.grid(row=4,column=0)
mpb["maximum"] = 30
mpb["value"] = 0


# Create and render light status text
statusTextFrame = tkinter.Frame(mainFrame)
statusTextFrame.grid(row=5,column=0,columnspan=2)
statusText = tkinter.Label(statusTextFrame, text="Light is OFF", font=("Helvetica", 9))
statusText.config(background='white')
statusText.grid(row=5,column=0)



# Define function for checking address balance on the IOTA tangle. 
def checkbalance():

    gb_result = api.get_balances(address)
    balance = gb_result['balances']
    return (balance[0])


# Define funtion to display current IOTA balance in GUI
def displaybalance(currentbalance):
    baltext = "Current address balance = " + str(currentbalance) + " IOTA"
    balanceText.configure(text=baltext)



# Get current address balance at startup and use as baseline for measuring new funds being added.   
currentbalance = checkbalance()
displaybalance(currentbalance)
lastbalance = currentbalance


# Define some variables
lightbalance = 0
balcheckcount = 0
lightstatus = False


# Main loop that executes every 1 second
def maintask(balcheckcount, lightbalance, lightstatus, lastbalance):


    # Check for new funds and add to lightbalance when found.
    if balcheckcount == 30:
        currentbalance = checkbalance()
        displaybalance(currentbalance)
        if currentbalance > lastbalance:
            lightbalance = lightbalance + (currentbalance - lastbalance)
            lastbalance = currentbalance
        balcheckcount = 0

    # Manage light balance and light ON/OFF
    if lightbalance > 0:
        if lightstatus == False:
            statusText.config(text="Light is ON")
            lightstatus=True
        lightbalance = lightbalance -1       
    else:
        if lightstatus == True:
            statusText.config(text="Light is OFF")
            lightstatus=False

    # Print remaining light balance     
    strlightbalance = datetime.timedelta(seconds=lightbalance)
    timeText.config(text=strlightbalance)


    # Increase balance check counter
    balcheckcount = balcheckcount +1


    # Update progress bar
    mpb["value"] = balcheckcount


    # Run maintask function after 1 sec.
    root.after(1000, maintask, balcheckcount, lightbalance, lightstatus, lastbalance)


# Run maintask function after 1 sec.
root.after(1000, maintask, balcheckcount, lightbalance, lightstatus, lastbalance)


root.mainloop()
