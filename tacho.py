# Panie wężu proszę o program do tacho
# -*- encoding: utf8 -*-
from tkinter import *
timeEntries = []
info = ""
def calc(evt): #For calculation button
    global info, timeEntries
    entry = entry_field.get()
    entry = entry.replace("+","")

    try:
        int(entry)
        #list_one.insert(0,entry)
        timeEntries_update()
        timeEntries.append(int(entry))
        info = "Total: " + str(sum(timeEntries))
        stat.set(info)
        entry_field.delete(0, END)

    except:
        #entry_field.delete(0, END)
        entry_field.focus()

def clearbox(evt): # clear entry box
    entry_field.delete(0, END)
    entry_field.focus()

def clearone(evt):
    entry = entry_field.get()[:-1]
    entry_field.delete(0, END)
    entry_field.insert(0,entry)

def num_press(num):
        if num == "C":
            clearbox("C")
        elif num == ",": # yeah, I found it quite usefull for my keyboard
            entry_field.insert(END, ".")
        else:

            entry_field.insert(END, num)
            entry_field.focus()

def timeEntries_update():
    for i in timeEntries:
        list_one.insert(0,i)

#=======tkinter window===========
win = Tk()
#win.geometry("775x325") # Force window size
win.wm_title("Tacho 0.0.2")
win.resizable(width=FALSE, height=FALSE)

topFrame = Frame(win)
#topFrame.pack(fill=BOTH)
topFrame.grid(row=0, column=1, columnspan=2)

rightFrame = Frame(win)
rightFrame.grid(row=1, column=1) # This puts item on place

leftFrame = Frame(win)
#middleFrame.pack(fill=BOTH)
leftFrame.grid(row=1, column=0)

downFrame = Frame(win)
downFrame.grid(row=2, columnspan=2)

entry_field = Entry(topFrame, textvariable=StringVar(), font ="Helvetica 20 bold", width=18, justify=RIGHT)
#entry_field.grid(sticky=E)
entry_field.pack(fill=X, expand=True, side=RIGHT, ipady=10)
entry_field.bind('<Button-1>', clearbox)
entry_field.focus()

#-------set what happens if you press Enter-----
win.bind("<Return>", calc)
win.bind("<KP_Enter>", calc)
win.bind("<KP_Add>", calc)

#=========================================

list_one = Listbox(leftFrame, exportselection=0, height=15, width=40)
list_one.pack(side=LEFT, fill=BOTH, expand=True)

sb1 = Scrollbar(leftFrame, orient=VERTICAL) #scrollbar
sb1.pack(side=LEFT,fill=BOTH)

sb1.configure(command=list_one.yview)
list_one.configure(yscrollcommand=sb1.set)

# lb1.bind('<<ListboxSelect>>', firstselect) #action for selected line

stat = StringVar()
status = Label(downFrame, textvariable=stat, bd=1, relief=SUNKEN, font = "Helvetica 15 bold",width=54)
stat.set(info)
status.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

#=======Numpad==========
bttn = []
numbers="HMS789456123C0:"
i = 0
for j in range(1,6):
    for k in range(3):
        bttn.append(Button(rightFrame, text = numbers[i], font ="Helvetica 15 bold", height = 1, width = 2))
        bttn[i].grid(row = j, column = k, pady = 2, padx = 2)
        bttn[i]["command"] = lambda x = numbers[i]: num_press(x)
        i += 1

#other buttons

cbutton = Button(rightFrame, text ="+", font ="Helvetica 15 bold", height = 6, width = 7)
cbutton.grid(row = 1, column = 4, rowspan = 4, columnspan=2, pady = 2, padx=2)
cbutton.bind('<Button-1>', calc)

otherbutton = Button(rightFrame, text ="←", font ="Helvetica 15 bold", height = 1, width = 2)
otherbutton.grid(row = 5, column = 4, pady = 2, padx=2)
otherbutton.bind('<Button-1>', clearone)

modulobutton = Button(rightFrame, text ="M24", font ="Helvetica 15 bold", height = 1, width = 2)
modulobutton.grid(row = 5, column = 5, pady = 2, padx=2)
modulobutton.bind('<Button-1>', calc)



#============================================

win.mainloop()
