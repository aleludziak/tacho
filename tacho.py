from tkinter import *
import re
import datetime
import Pmw


def start():
    global current_data
    current_data = Data()
    current_data.update()
    current_data.info()


def add_entry(evt):
    current_data.add()


def clear_all(evt):  # clear top_frame_input
    top_frame_input.delete(0, END)
    top_frame_input.focus()


def clear_one(evt):  # clear last digit from top_frame_input
    user_input = top_frame_input.get()[:-1]
    top_frame_input.delete(0, END)
    top_frame_input.insert(0, user_input)


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

# =======tkinter window===========
win = Tk()
# win.geometry("775x325") # Force window size
win.wm_title("Tacho 0.0.4")
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

leftFrame = Frame(win)
leftFrame.grid(row=1, column=0)

rightFrame = Frame(win)
rightFrame.grid(row=1, column=1)

bottomFrame = Frame(win)
bottomFrame.grid(row=2, columnspan=2)

# -------keys actions-----
win.bind("<Return>", add_entry)
win.bind("<KP_Enter>", add_entry)
win.bind("<KP_Add>", add_entry)
win.bind("<KP_Decimal>", num_press)

# ==========input entry===========

top_frame_input = Pmw.Counter(topRightFrame,
                              entry_font="Helvetica 20 bold",
                              entry_width=12,
                              autorepeat=True, datatype='time',
                              entryfield_validate={'validator': 'time'},
                              entryfield_value='00:00:00',
                              increment=60)
top_frame_input.grid(column=0)

top_frame_input.component('entry').focus_set()
top_frame_input.select_range(3, 5)
top_frame_input.icursor(5)

# ===========Listbox with scrollbar=================

entries_list = Pmw.ScrolledListBox(leftFrame, hscrollmode='none', vscrollmode='static',
                                   listbox_height=15, listbox_width=40)
'''
entries_list = Pmw.ComboBox(leftFrame, dropdown = 0, scrolledlist_vscrollmode = 'static',
                            scrolledlist_hscrollmode = 'none', scrolledlist_listbox_height = 15,
                            scrolledlist_listbox_width=40,
                            entryfield_validate = {'validator' : 'time'},
                            entryfield_value = '00:00:00',
                            )
'''

entries_list.grid(row=0, column=0)


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
# ------buttons to change mode of entry-------
select_mode = Pmw.RadioSelect(rightFrame, Button_height=1, Button_width=2,
                              Button_font="Helvetica 15 bold", pady=2, padx=2)

select_mode.grid(row=0, column=0, columnspan=4)

# Add some buttons to the horizontal RadioSelect.
for text in ('D', 'W', 'P', 'R'):
    select_mode.add(text)
select_mode.invoke('R')

# ======top left buttons==========

top_left_buttons = Pmw.ButtonBox(topLeftFrame, Button_height=1,  # Button_width=2,
                                 Button_font="Helvetica 15 bold", pady=1, padx=1)

top_left_buttons.grid(row=0, column=0, columnspan=2)

# Add some buttons to the horizontal RadioSelect.
top_left_buttons.add('Delete', command=lambda: current_data.delete_item())
top_left_buttons.add('Edit')
top_left_buttons.add('Save')
top_left_buttons.add('Clear', command=start)


# =====bottom status=============
status = StringVar()
bottom_status_total = Label(bottomFrame, textvariable=status, bd=1, relief=SUNKEN,
                            font="Helvetica 15 bold", width=54)
status.set("")
bottom_status_total.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

# ============================================


class Data:

    def __init__(self):
        self.records = []

    def converter(self, sec):
        conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
        return conversion

    def add(self):
        index = 0
        entry = Entry(select_mode.getvalue(), top_frame_input.get())
        try:
            index = entries_list.curselection()[0]
        except:
            pass

        self.records.insert(index, entry)
        top_frame_input.setentry('00:00:00')
        top_frame_input.select_range(3, 5)
        top_frame_input.icursor(5)
        self.info()
        self.update()

    def delete_item(self):
        # delete a selected line from the listbox and from entries
        # print('It works')
        try:
            # get selected line index
            index = entries_list.curselection()[0]
            entries_list.delete(index)
            self.records.pop(index)
            self.update()
            self.info()

        except IndexError:
            pass

    def sum(self, v):
        total = 0

        if v == 'total':

            for v in self.records:
                total += v.get_value()
            return total
        else:

            summary = 0
            for x in self.records:
                if v == x.get_mode():
                    summary += x.get_value()
            return summary

    def update(self):
        entries_list.delete(0, END)
        line_number = len(self.records)
        for record in self.records:
            entries_list.insert(END, str(line_number) + ') ' + str(record))
            if record.get_mode() == 'R':
                entries_list.itemconfig(END, {'bg': 'blue'}, foreground='white')
            elif record.get_mode() == 'P':
                entries_list.itemconfig(END, {'bg': 'yellow'})
            elif record.get_mode() == 'W':
                entries_list.itemconfig(END, {'bg': 'cyan'})
            elif record.get_mode() == 'D':
                entries_list.itemconfig(END, {'bg': 'green'}, foreground='white')

            line_number -= 1

    def info(self):
        status.set('Total time: ' + str(self.converter(self.sum('total')))+'\n' +
                   str(self.sum('total'))+' seconds'+'\n' +
                   'Resting in total: '+str(self.converter(self.sum('R')))+'\n' +
                   'Driving in total: '+str(self.converter(self.sum('D')))+'\n' +
                   'Working in total: '+str(self.converter(self.sum('W')))+'\n' +
                   'POA in total: '+str(self.converter(self.sum('P')))
                   )


class Entry:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value
        self.cleaner()

    def cleaner(self):
        user_input = str(self.value)
        self.value = re.sub('[^0-9:]', '', user_input)  # leaves only digits and ":" into input
        try:
            h, m, s = re.split(':', user_input)
            self.value = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
        except:
            try:
                m, s = re.split(':', user_input)
                self.value = int(datetime.timedelta(minutes=int(m), seconds=int(s)).total_seconds())
            except:
                self.value = re.sub('\D', '', user_input)  # clean input from non-digit characters
                self.value = int(datetime.timedelta(minutes=int(self.value)).total_seconds())

        # self.input = self.input.replace("+", "") # simplest method (replace just one character)
            # in case this one above will make a troubles
    def get_value(self):
        return self.value

    def get_mode(self):
        return self.mode

    def __str__(self):
        mode_names = {'D': 'Driving', 'W': 'Work', 'P': 'POA/availability', 'R': 'Rest/Break'}
        sec = self.value
        conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
        return conversion + ' ' + mode_names[self.mode]

start()
win.mainloop()
