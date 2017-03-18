# -*- encoding: utf8 -*-
# Panie wężu proszę o program do tacho

from tkinter import *

timeEntries = []
total_info = ""


def add_entry(evt):  # For calculation button
    global total_info, timeEntries
    entry = top_frame_input.get()
    entry = entry.replace("+", "")

    try:
        int(entry)
        # entries_list.insert(0,entry)
        timeEntries.append(int(entry))
        total_info = "Total: " + str(sum(timeEntries))
        stat.set(total_info)
        top_frame_input.delete(0, END)
        time_entries_update()

    except:
        top_frame_input.focus()


def clear_box(evt):  # clear top_frame_input
    top_frame_input.delete(0, END)
    top_frame_input.focus()


def clear_one(evt):  # clear last digit from top_frame_input
    entry = top_frame_input.get()[:-1]
    top_frame_input.delete(0, END)
    top_frame_input.insert(0, entry)


def num_press(num):
    if num == "C":
        clear_box("C")
    elif num == ",":  # yeah, I found it quite useful for my keyboard
        top_frame_input.insert(END, ".")
    else:

        top_frame_input.insert(END, num)
        top_frame_input.focus()


def time_entries_update():
    entries_list.delete(0, END)
    for ti in timeEntries:
        entries_list.insert(0, ti)


# =======tkinter window===========
win = Tk()
# win.geometry("775x325") # Force window size
win.wm_title("Tacho 0.0.2")
win.resizable(width=FALSE, height=FALSE)

topFrame = Frame(win)
# topFrame.pack(fill=BOTH)
topFrame.grid(row=0, column=0, columnspan=2)

rightFrame = Frame(win)
rightFrame.grid(row=1, column=1)

leftFrame = Frame(win)
# middleFrame.pack(fill=BOTH)
leftFrame.grid(row=1, column=0)

bottomFrame = Frame(win)
bottomFrame.grid(row=2, columnspan=2)

top_frame_input = Entry(topFrame, textvariable=StringVar(),
                        font="Helvetica 20 bold", width=18, justify=RIGHT)
top_frame_input.grid(column=8)
# top_frame_input.pack(fill=X, expand=True, side=RIGHT, ipady=10)
top_frame_input.bind('<Button-1>', clear_box)
top_frame_input.focus()

# ======top icons==========
top_frame_icons = []

for i in range(0, 7):

    top_frame_icons.append(

        Button(topFrame, text='X'.format(i),

               font="Helvetica 15 bold", height=1, width=2)

    )

    top_frame_icons[i].grid(row=0, column=i)

# -------keys actions-----
win.bind("<Return>", add_entry)
win.bind("<KP_Enter>", add_entry)
win.bind("<KP_Add>", add_entry)

# ===========Listbox with scrollbar=================

entries_list = Listbox(leftFrame, exportselection=0, height=15, width=40)
entries_list.pack(side=LEFT, fill=BOTH, expand=True)

entries_list_scrollbar = Scrollbar(leftFrame, orient=VERTICAL)  # scrollbar
entries_list_scrollbar.pack(side=LEFT, fill=BOTH)

entries_list_scrollbar.configure(command=entries_list.yview)
entries_list.configure(yscrollcommand=entries_list_scrollbar.set)

# entries_list.bind('<<ListboxSelect>>', select) #action for selected line

# =====
stat = StringVar()
bottom_status_total = Label(bottomFrame, textvariable=stat, bd=1, relief=SUNKEN, font="Helvetica 15 bold", width=54)
stat.set(total_info)
bottom_status_total.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

# =======Numpad==========
bttn = []
numbers = "HMS789456123C0:"
i = 0
for j in range(1, 6):
    for k in range(3):
        bttn.append(Button(rightFrame, text=numbers[i], font="Helvetica 15 bold", height=1, width=2))
        bttn[i].grid(row=j, column=k, pady=2, padx=2)
        bttn[i]["command"] = lambda x=numbers[i]: num_press(x)
        i += 1

# other buttons

add_entry_button = Button(rightFrame, text="+", font="Helvetica 15 bold", height=6, width=7)
add_entry_button.grid(row=1, column=4, rowspan=4, columnspan=2, pady=2, padx=2)
add_entry_button.bind('<Button-1>', add_entry)

clear_one_button = Button(rightFrame, text="←", font="Helvetica 15 bold", height=1, width=2)
clear_one_button.grid(row=5, column=4, pady=2, padx=2)
clear_one_button.bind('<Button-1>', clear_one)

modulo_button = Button(rightFrame, text="M24", font="Helvetica 15 bold", height=1, width=2)
modulo_button.grid(row=5, column=5, pady=2, padx=2)
modulo_button.bind('<Button-1>', add_entry)

# ============================================

win.mainloop()
