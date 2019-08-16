# Integrating physical devices with IOTA — Adding a user interface

The third part in a series of beginner tutorials on integrating physical devices with the IOTA protocol.

![img](https://miro.medium.com/max/700/1*xucMv3pEzQuQRWsCjJ3X-Q.jpeg)

## Introduction

This is the third part in a series of beginner tutorials on integrating physical devices with the IOTA protocol. In this tutorial we will be using an Liquid Crystal Display (LCD) to provide a simple Graphical User Interface (GUI) for our IOTA payment system.

If you haven’t read the [first tutorial](https://medium.com/@hugogregersen/integrating-physical-devices-with-iota-83f4e00cc5bb) in this series, you should read it before continuing as it forms the foundation for the project we are building on in this tutorial.

------

## The Use Case

Now that we have our new IOTA powered refrigerator payment system up and running as described in the [first tutorial](https://medium.com/@hugogregersen/integrating-physical-devices-with-iota-83f4e00cc5bb), we should take a step back and look at any improvements that could be made to our system. If we look at it from the user (hotel guest) point of view, one problem that stand out is that there is no indicator telling him the current status of his refrigerator service, and thereby no indication as to if or when he needs to add additional funds in case he wants to prolong the service. We also have some issues related to the printed QR Code. In case the hotel owners wants to change the IOTA payment address for one or more refrigerators he would have to physically replace the printed QR code for each refrigerator in his hotel. Another problem related to the printed QR code is that a bad actor in theory could replace the official printed QR code with a fake QR code, sending any future refrigerator payments to the wrong address. We also have an issue related to managing the price of the refrigerator service. How can the hotel owner display an up-to-date price of his refrigerator service with respect to the volatile IOTA market price? A logical solution to these problems would be to provide the guest with some type of dynamic user interface where he could interact and get real time information from the system. In this tutorial we will be adding a simple LCD display to our project to provide such an interface.

*Note!
Using an LCD for dynamically displaying our QR code could solve another issue related to the reuse of IOTA addresses, also known as the Winternitz one-time signature* scheme*. This is a protection mechanism that gives IOTA its quantum resistance properties. As long as the hotel owner do not spend any funds from his refrigerator addresses they are completely safe, however, as soon as he spends any funds from one of the addresses, the address is no longer safe and must be replaced by a new IOTA payment address. A better option might be to automatically generate a new address (and QR code) for every payment so that we could ignore this problem all together. This is where our LCD comes in handy. I will leave the topic of auto generating IOTA addresses for a future tutorial. For now, lets just focus on displaying our static QR code on the LCD.*

------

## Components

I will not be discussing the basic components (except the LCD) and wiring of the project in this tutorial as it can be seen as an add-on to the [first tutorial](https://medium.com/@hugogregersen/integrating-physical-devices-with-iota-83f4e00cc5bb) in this series.

**The LCD**
There are a large number of different Raspberry PI compatible LCD’s on the market. You could typically get them of Ebay or Amazon for about 15 USD and upwards, depending on model and size. In my case i’m using this 3.5" TFT LCD Touch Display that snaps directly on to the GIO pins of my Raspberry PI. In case you want the LCD placed separately from the PI, or require easy access to the PI’s additional GIO pins, you may want get an additional cable for connecting the LCD. I will not go into details on how to connect and install drivers for the LCD as this varies depending on the type and model. For this information i suggest you confront the documentation for your particular model.

![img](https://miro.medium.com/max/238/1*a_LgdwxyUeqkuL47F8-tig.png)

## The GUI

Next, lets have a look at the GUI itself and how it was built. In my example i’m using the popular [TkInter](https://wiki.python.org/moin/TkInter) toolkit for creating the GUI. There are other toolkit’s that can be used for creating GUI’s with Python but TkInter is the most commonly used. Another great thing about TkInter is that it is already included with Python. There are a lot of examples and tutorials on using TkInter out there so i suggest you check out these resources when building your own version of the GUI. What information and functionality you want to include in your GUI is of course up to you, in my example i have chosen to include the following elements:

![img](https://miro.medium.com/max/592/1*bDYQH61gNW0ff2H8QHniXg.png)

My IOTA payment GUI

1. QR Code of the IOTA payment address to be scanned when using the service.
2. “Pay With IOTA” logo to clearly identify that this is an IOTA payment service.
3. The remaining time of any active service.
4. The current balance of the selected IOTA payment address.
   (This would typically not be relevant for any real life implementation of the project but might be useful when debugging the system)
5. Progress bar to indicate the interval between checking the IOTA tangle for new funds.
6. Status label indicating if the light is ON or OFF.
   (I don’t have the physical relay and LED wired up when writing this tutorial so i use this label to identify when the LED is ON or OFF)
7. Exit button to exit the Python program.
   (It would probably not make sense to include this button in a real life implementation of the project as we don’t want the user to exit the system by him self. However, it was included in my example to provide a convenient way of closing down the Python program while testing and debugging)

*Note!*
*I have decided to exclude any information related to the price of the service in my GUI as i plan for a future tutorial where we take a deeper look at this topic.*

------

## Required Software and libraries

Before we can start writing our Python code for this project we need to make sure that we have all the required software and libraries installed on our Raspberry PI.

First of all, we need to have an OS installed on our Raspberry PI. Any Raspberry PI supported Linux distribution should work. In my example I’m using the Raspbian distro as it already have Python and several Python editors (IDE) included. The Raspbian distro with installation instructions can be found here: https://www.raspberrypi.org/downloads/raspbian/

In case you need to install Python separately, you will find it here: https://www.python.org/downloads/

We also need to install a couple of libraries used by the GUI

1. PyQRCode
   The PyQRCode library is used to generate and render our QR code on the LCD. The PyQRCode library with installation instructions can be found [here](https://pypi.org/project/PyQRCode/).
2. Pillow
   The Pillow library is used to render our IOTA logo on the LCD. The Pillow library with installation instructions can be found [here](https://pypi.org/project/Pillow/2.2.1/).

Finally, we need to install the PyOTA API library that will allow us to access the IOTA tangle using the Python programming language. The PyIOTA API library with installation instructions can be found here: https://github.com/iotaledger/iota.lib.py

------

## The Python Code

Now let’s have a look at the Python code that does the all magic. The main difference from the [first tutorial](https://medium.com/@hugogregersen/integrating-physical-devices-with-iota-83f4e00cc5bb) in this series is that we now use a TkInter based graphical user interface instead of writing some text to the console. Notice how we force the GUI to take the up the full screen by setting some properties for the root object. Another important aspect is of course scaling of the individual elements in the GUI so that they fit correctly on the display . In my example i’m using a 3.5" LCD and have adjusted my scaling accordingly. Also notice that i have removed all references to the GPIO library together with any functions related to the GIO pins as i do not have my relay hooked up while writing this tutorial. This also allows me to create and test my GUI on any computer before moving it to the PI.

*Tip!
One issue i faced when connecting my LCD to the Raspberry PI was that; when the LCD was active, the PI no longer sent any signal to the HDMI port. This quickly became a problem when testing and debugging my GUI as i could only use one monitor at the time, the LCD or my HDMI monitor. To solve this problem i ended up installing* [*Real VNC*](https://www.realvnc.com/en/) *on both the PI and my home PC. Now i could leave the PI in LCD mode and do the coding on my PC. So whenever i want to test my GUI on the LCD, i simply use the file transfer function in* [*Real VNC*](https://www.realvnc.com/en/) *and execute the code on the PI.

```python
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
```

You can download the Python source code from [here](https://gist.github.com/huggre/67efefd75a5fa2571446d3b7c9d58e0b).

------

## Running the project

To run the project, you first need to save the code in the previous section as a text file on your Raspberry PI.

Notice that Python program files uses the .py extension, so let’s save the file as **let_there_be_light_gui.py** on the Raspberry PI.

To execute the program, simply start a new terminal window, navigate to the folder where you saved *let_there_be_light_gui.py* and type:

**python let_there_be_light_gui.py**

You should now see the GUI appear on your LCD/Monitor, showing a QR code for your IOTA payment address together with the other elements as described earlier. To exit the Python program you simply press the Exit button.

*Note!
Make sure you download and place the “iota_logo75.jpg” file in the same folder as your python file before executing the program, otherwise you will get an error. The logo file can be downloaded from* [*here*](https://github.com/huggre/pay_the_light_gui/blob/master/iota_logo75.jpg)*.*

------

## Pay the light

To turn on the LED (or in my case, set the **Light is ON** status) you simply use your favorite IOTA wallet and transfer some IOTA’s to your selected IOTA address. As soon as the transaction is confirmed by the IOTA tangle, the LED should light up (or in my case, set the **Light is ON** status), and stay on until the light balance is empty depending on the amount of IOTA’s you transferred. In my example I have set the IOTA/light ratio to be 1 IOTA for 1 second of light.

------

## Donations

If you like this tutorial and want me to continue making others, feel free to make a small donation to the IOTA address used in the Python code. Also, feel free to use the same IOTA address when building and testing your version of this project, so that whenever my LED (and yours) lights up it gives me (us) a nice reminder that someone else is using this tutorial.

![img](https://miro.medium.com/max/400/1*kV_WUaltF4tbRRyqcz0DaA.png)

> GTZUHQSPRAQCTSQBZEEMLZPQUPAA9LPLGWCKFNEVKBINXEXZRACVKKKCYPWPKH9AWLGJHPLOZZOYTALAWOVSIJIYVZ
