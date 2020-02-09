from tkinter import *
import requests

global commandUuid
window = Tk()
window.title("Bot controller")
window.geometry('1000x200')
lbl = Label(window, text="UUID: ")
lbl.grid(column=0, row=0)
txt = Entry(window, width=30)
txt.grid(column=1, row=0)
def clicked():
    global commandUuid
    commandUuid = txt.get()
    print(commandUuid)
    lbl.configure(text='connected')
def keyPressed(event):
    if event.keysym == 'Up':
        sendCmd("go forward")
    if event.keysym == 'Down':
        sendCmd("go backwards")
    if event.keysym == 'Left':
        sendCmd("go left")
    if event.keysym == 'Right':
        sendCmd("go right")
    if event.keysym == 'space':
        sendCmd("stop")
def sendCmd(cmd):
    print(commandUuid)
    if commandUuid != '':
        requests.post('https://botcontroller-267620.appspot.com/commands/' + commandUuid, data=cmd)
btn = Button(window, text="connect", command=clicked)
btn.grid(column=2, row=0)
window.bind('<KeyPress>', keyPressed)
window.mainloop()