# -*- encoding: utf8 -*-
# Panie wężu proszę o program do tacho

from tkinter import *

entries = []
total_info = ""


def add_entry(evt):  # For calculation button
    global total_info, entries
    entry = top_frame_input.get()
    entry = entry.replace("+", "")

    try:
        int(entry)
        # entries_list.insert(0,entry)
        entries.append(int(entry))
        total_info = "Total: " + str(sum(entries))
        status.set(total_info)
        entries_update()
        top_frame_input.delete(0, END)

    except:
        top_frame_input.focus()


def clear_all(evt):  # clear top_frame_input
    top_frame_input.delete(0, END)
    top_frame_input.focus()


def clear_one(evt):  # clear last digit from top_frame_input
    entry = top_frame_input.get()[:-1]
    top_frame_input.delete(0, END)
    top_frame_input.insert(0, entry)


def num_press(num):  # num pad button action
    if num == "C":
        clear_all("C")
    elif num == ",":  # yeah, I found it quite useful for my keyboard
        top_frame_input.insert(END, ".")
    else:

        top_frame_input.insert(END, num)
        top_frame_input.focus()


def entries_update():
    entries_list.delete(0, END)
    for sec in entries:
        converted_seconds = "%d:%02d:%02d" % (sec / 3600, sec / 60 % 60, sec % 60) # convert to HH:MM:SS
        entries_list.insert(0, converted_seconds)
        if sec == 1:
            entries_list.itemconfig(0, {'bg': 'green'})  # it is going to be useful later,
            # for marking different types of entries
    # print(entries_list.get(0, END))

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

# -------keys actions-----
win.bind("<Return>", add_entry)
win.bind("<KP_Enter>", add_entry)
win.bind("<KP_Add>", add_entry)

# ==========input entry===========
top_frame_input = Entry(topFrame, textvariable=StringVar(),
                        font="Helvetica 20 bold", width=18, justify=RIGHT)
top_frame_input.grid(column=8)
# top_frame_input.pack(fill=X, expand=True, side=RIGHT, ipady=10)
top_frame_input.bind('<Button-1>', clear_all)
top_frame_input.focus()

# ======top icons==========
top_frame_icons = []

for i in range(0, 7):

    top_frame_icons.append(

        Button(topFrame, text='X',

               font="Helvetica 15 bold", height=1, width=2)

    )

    top_frame_icons[i].grid(row=0, column=i)

# ===========Listbox with scrollbar=================
entries_list = Listbox(leftFrame, exportselection=0, height=15, width=40)
entries_list.pack(side=LEFT, fill=BOTH, expand=True)

entries_list_scrollbar = Scrollbar(leftFrame, orient=VERTICAL)  # scrollbar
entries_list_scrollbar.pack(side=LEFT, fill=BOTH)

entries_list_scrollbar.configure(command=entries_list.yview)
entries_list.configure(yscrollcommand=entries_list_scrollbar.set)

# entries_list.bind('<<ListboxSelect>>', select) #action for selected line

# =======num pad==========
keyboard = []
keys = "HMS789456123C0:"
i = 0
for j in range(1, 6):
    for k in range(3):
        keyboard.append(Button(rightFrame, text=keys[i], font="Helvetica 15 bold", height=1, width=2))
        keyboard[i].grid(row=j, column=k, pady=2, padx=2)
        keyboard[i]["command"] = lambda x=keys[i]: num_press(x)
        i += 1

# --------other buttons---------
add_entry_button = Button(rightFrame, text="+", font="Helvetica 15 bold", height=6, width=7)
add_entry_button.grid(row=1, column=4, rowspan=4, columnspan=2, pady=2, padx=2)
add_entry_button.bind('<Button-1>', add_entry)

clear_one_button = Button(rightFrame, text="←", font="Helvetica 15 bold", height=1, width=2)
clear_one_button.grid(row=5, column=4, pady=2, padx=2)
clear_one_button.bind('<Button-1>', clear_one)

modulo_button = Button(rightFrame, text="M24", font="Helvetica 15 bold", height=1, width=2)
modulo_button.grid(row=5, column=5, pady=2, padx=2)
modulo_button.bind('<Button-1>', add_entry)

# =====bottom status=============
status = StringVar()
bottom_status_total = Label(bottomFrame, textvariable=status, bd=1, relief=SUNKEN,
                            font="Helvetica 15 bold", width=54)
status.set(total_info)
bottom_status_total.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

# ============================================

win.mainloop()
