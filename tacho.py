# Panie wężu proszę o program do tacho
from tkinter import *


def calc(evt):
    e.delete(0,END)
    e.focus()

def clearbox(evt):
    e.delete(0,END)
    e.focus()


win = Tk()
#win.geometry("775x325")
win.wm_title("Tacho 0.0.1")
win.resizable(width=FALSE, height=FALSE)

pFrame = Frame(win)
pFrame.grid(row=1,column=1)

v = StringVar()
e = Entry(pFrame,textvariable=v,font = "Helvetica 20 bold", width=15, justify=RIGHT)
e.grid(row=0, column=0, columnspan=6)
e.bind('<Button-1>', clearbox)
e.focus()

win.bind("<Return>", calc)
win.bind("<KP_Enter>", calc)



def num_press(num):
        if num == "C":
            e.delete(0,END)
            e.focus()
        elif num == ",":
            e.insert(END,".")
        else:

            e.insert(END, num)
            e.focus()
bttn = []
numbers="HMS789456123C0."
i = 0
for j in range(1,6):
    for k in range(3):
        bttn.append(Button(pFrame, text = numbers[i], font = "Helvetica 15 bold", height = 1, width = 1))
        bttn[i].grid(row = j, column = k, pady = 2, padx = 2)
        bttn[i]["command"] = lambda x = numbers[i]: num_press(x)
        i += 1



cbutton = Button(pFrame, text = "=", font = "Helvetica 10 bold", height = 9, width = 9)
cbutton.grid(row = 2, column = 5, columnspan = 4, rowspan = 4, pady = 2, padx=2)
cbutton.bind('<Button-1>', calc)

pbutton = Button(pFrame, text = "+", font = "Helvetica 10 bold", height = 4, width = 9)
pbutton.grid(row = 0, column = 5, columnspan = 4, rowspan = 4, pady = 2, padx=2)
pbutton.bind('<Button-1>', calc)


win.mainloop()
