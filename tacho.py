# -*- encoding: utf8 -*-
# Panie wężu proszę o program do tacho

from tkinter import *
import re, datetime, Pmw, time

entries = []
#total_info = ""

def add_entry(evt):  # For calculation button
    Entry()
'''
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

'''
def clear_all(evt):  # clear top_frame_input
    top_frame_input.delete(0, END)
    top_frame_input.focus()


def clear_one(evt):  # clear last digit from top_frame_input
    entry = top_frame_input.get()[:-1]
    top_frame_input.delete(0, END)
    top_frame_input.insert(0, entry)


def num_press(num):  # num pad button action
    if top_frame_input.get() == '00:00:00':
        clear_all("C")
    if num == "C":
        clear_all("C")
    elif num == ".":  # doesn't work because counter doesn't allow insert other thinks than numbers and ":"
        top_frame_input.insert(END, ":")
    else:

        top_frame_input.insert(END, num)
        top_frame_input.focus()

'''
def entries_update():
    entries_list.delete(0, END)
    for sec in entries:
        converted_seconds = "%d:%02d:%02d" % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
        entries_list.insert(0, converted_seconds)
        if sec == 1:
            entries_list.itemconfig(0, {'bg': 'green'})  # it is going to be useful later,
            # for marking different types of entries
            # print(entries_list.get(0, END))
'''

# =======tkinter window===========
win = Tk()
# win.geometry("775x325") # Force window size
win.wm_title("Tacho 0.0.3")
win.resizable(width=FALSE, height=FALSE)

Pmw.initialise(win)


'''
topFrame = Frame(win)
# topFrame.pack(fill=BOTH)
topFrame.grid(row=0, column=0, columnspan=2)
'''
topLeftFrame = Frame(win)
topLeftFrame.grid(row=0, column=0)

topRightFrame = Frame(win)
topRightFrame.grid(row=0, column=1)

rightFrame = Frame(win)
rightFrame.grid(row=1, column=1)

leftFrame = Frame(win)
# middleFrame.pack(fill=BOTH)
leftFrame.grid(row=1, column=0)

bottomFrame = Frame(win)
bottomFrame.grid(row=2, columnspan=2)

# -------keys actions-----
#win.bind("<Return>", add_entry)
win.bind("<KP_Enter>", add_entry)
win.bind("<KP_Add>", add_entry)
win.bind("KP_Decimal", num_press)

# ==========input entry===========
'''
top_frame_input = Entry(topFrame, textvariable=StringVar(),
                        font="Helvetica 20 bold", width=18, justify=RIGHT)
top_frame_input.grid(column=8)
# top_frame_input.pack(fill=X, expand=True, side=RIGHT, ipady=10)
top_frame_input.bind('<Button-1>', clear_all)
top_frame_input.focus()
'''
top_frame_input = Pmw.Counter(topRightFrame,
                              #labelpos = 'w',
                              # label_text = 'Time:',
                              entry_font="Helvetica 20 bold",
                              entry_width = 12,
                              autorepeat = True, datatype = 'time',
                              entryfield_validate = {'validator' : 'time'},
                              entryfield_value = '00:00:00',
                              increment = 60)
top_frame_input.grid(column = 0)

top_frame_input.component('entry').focus_set()
top_frame_input.select_range(3,5)
top_frame_input.icursor(5)


# ======top icons==========

top_frame_icons = []

for i in range(0, 5):
    top_frame_icons.append(

        Button(topLeftFrame, text='X',

               font="Helvetica 15 bold", height=1, width=2)

    )

    top_frame_icons[i].grid(row=0, column=i, sticky = W,ipadx = 10, ipady=1)


# ===========Listbox with scrollbar=================
'''
entries_list = Listbox(leftFrame, exportselection=0, height=15, width=40)
entries_list.pack(side=LEFT, fill=BOTH, expand=True)

entries_list_scrollbar = Scrollbar(leftFrame, orient=VERTICAL)  # scrollbar
entries_list_scrollbar.pack(side=LEFT, fill=BOTH)

entries_list_scrollbar.configure(command=entries_list.yview)
entries_list.configure(yscrollcommand=entries_list_scrollbar.set)

# entries_list.bind('<<ListboxSelect>>', select) #action for selected line
'''
entries_list = Pmw.ScrolledListBox(leftFrame, hscrollmode = 'none', vscrollmode = 'static', listbox_height = 15, listbox_width=40)
'''
entries_list = Pmw.ComboBox(leftFrame, dropdown = 0, scrolledlist_vscrollmode = 'static',
                            scrolledlist_hscrollmode = 'none', scrolledlist_listbox_height = 15,
                            scrolledlist_listbox_width=40,
                            entryfield_validate = {'validator' : 'time'},
                            entryfield_value = '00:00:00',
                            )
'''
#entries_list.pack(side=LEFT, fill=BOTH, expand=True)
entries_list.grid(row = 0, column = 0, columnspan = 40)
# =======num pad==========
keyboard = []
keys = "789456123C0:"
i = 0
for j in range(1, 5):
    for k in range(3):
        keyboard.append(Button(rightFrame, text=keys[i], font="Helvetica 15 bold", height=1, width=2))
        keyboard[i].grid(row=j, column=k, pady=2, padx=2)
        keyboard[i]["command"] = lambda x=keys[i]: num_press(x)
        i += 1

# --------other buttons---------

add_entry_button = Button(rightFrame, text="+", font="Helvetica 15 bold", height=6, width=7)
add_entry_button.grid(row=1, column=3, rowspan=4, columnspan=2, pady=2, padx=2)
add_entry_button.bind('<Button-1>', add_entry)

clear_one_button = Button(rightFrame, text="←", font="Helvetica 15 bold", height=1, width=2)
clear_one_button.grid(row=0, column=4, pady=2, padx=2)
clear_one_button.bind('<Button-1>', clear_one)
'''
modulo_button = Button(rightFrame, text="M24", font="Helvetica 15 bold", height=1, width=2)
modulo_button.grid(row=5, column=5, pady=2, padx=2)
modulo_button.bind('<Button-1>', add_entry)
'''
icons = Pmw.RadioSelect(rightFrame, Button_height=1, Button_width=2, Button_font = "Helvetica 15 bold", pady = 2, padx = 2)
                        # labelpos = 'w',
                        # command = self.callback,
                        # label_text = 'Horizontal',
                        # frame_borderwidth = 2,
                        # frame_relief = 'ridge'

icons.grid(row = 0, column = 0, columnspan = 4)

# Add some buttons to the horizontal RadioSelect.
for text in ('D', 'W', 'P', 'R'):
    icons.add(text)
icons.invoke('R')

# =====bottom status=============
status = StringVar()
bottom_status_total = Label(bottomFrame, textvariable=status, bd=1, relief=SUNKEN,
                            font="Helvetica 15 bold", width=54)
status.set("")
bottom_status_total.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

# ============================================

class Entry:

    def __init__(self):
        self.input = top_frame_input.get()
        self.cleaner()
        self.seconds = int(self.input)
        self.add()
        self.update()
        status.set('Total time: '+str(self.converter(self.sum()))+'\n'+str(self.sum())+' seconds')
        top_frame_input.setentry('00:00:00')
        #top_frame_input.delete(0, END)
        print(self.seconds)
        print(self.converter(self.seconds))
        top_frame_input.select_range(3,5)
        top_frame_input.icursor(5)

    def cleaner(self):
        self.input = re.sub("[^0-9:]", "", self.input) # leaves only digits and ":" into input
        try:
            h,m,s = re.split(':',self.input)
            self.input = int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
        except:
            try:
                m,s = re.split(':',self.input)
                self.input = int(datetime.timedelta(minutes=int(m),seconds=int(s)).total_seconds())
            except:
                self.input = re.sub("\D", "", self.input) # clean input from non-digit characters
                self.input = int(datetime.timedelta(minutes=int(self.input)).total_seconds())

        # self.input = self.input.replace("+", "") # simplest method (replace just one character)
            # in case this one above will make a troubles

    def converter(self, sec):
        convertion = "%d:%02d:%02d" % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
        return convertion

    def add(self):
        global entries
        index = 0
        try:
            index = entries_list.curselection()[0]
        except:
            pass
        #entries.append(self.seconds)
        entries.insert(index,self.seconds)
        print("Entries: "+str(entries))
        print('index: '+str(index))


    def sum(self):
        global total_info
        total = sum(entries)
        return total


    def update(self):
        entries_list.delete(0, END)
        for e in entries:
            converted_entry = self.converter(e)
            #entries_list.insert(0, converted_entry)
            entries_list.insert(END, converted_entry)

win.mainloop()
