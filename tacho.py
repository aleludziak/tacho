from tkinter import *
import re
import datetime
import Pmw


def start():
    global current_data
    current_data = Data()
    current_data.update()
    current_data.info()


def add_entry():
    current_data.add()


def clear_all():  # clear top_frame_input
    top_frame_input.delete(0, END)
    top_frame_input.focus()


def clear_one():  # clear last digit from top_frame_input
    user_input = top_frame_input.get()[:-1]
    top_frame_input.delete(0, END)
    top_frame_input.insert(0, user_input)


def num_press(num):  # num pad button action
    if top_frame_input.get() == '00:00:00':
        clear_all()
    if num == "C":
        clear_all()
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
win.bind("<Return>", lambda a: add_entry())
win.bind("<KP_Enter>", lambda a: add_entry())
win.bind("<KP_Add>", lambda a: add_entry())
# win.bind("<KP_Decimal>", lambda a: num_press(":"))

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

# =======buttons===========
# -------num pad-----------
keyboard = []
keys = "789456123C0:"
i = 0
for j in range(1, 5):
    for k in range(3):
        keyboard.append(Button(rightFrame, text=keys[i], font="Helvetica 15 bold", height=1, width=2))
        keyboard[i].grid(row=j, column=k, pady=2, padx=2)
        keyboard[i]["command"] = lambda x=keys[i]: num_press(x)
        i += 1

# --------other buttons in num pad---------
add_entry_button = Button(rightFrame, text='+', font="Helvetica 15 bold", height=6, width=7, command=add_entry)
add_entry_button.grid(row=1, column=3, rowspan=4, columnspan=2, pady=2, padx=2)

clear_one_button = Button(rightFrame, text="←", font="Helvetica 15 bold", height=1, width=2, command=clear_one)
clear_one_button.grid(row=0, column=4, pady=2, padx=2)

# ------buttons to change mode of entry-------
select_mode = Pmw.RadioSelect(rightFrame, Button_height=1, Button_width=2,
                              Button_font="Helvetica 15 bold", pady=2, padx=2)

select_mode.grid(row=0, column=0, columnspan=4)

# Add some buttons to the horizontal RadioSelect - mode selection buttons.
for name, symbol, background in (('D', u'\u2609', 'green'), ('W', u'\u2692', 'blue'),
                                 ('P', u'\u26DD', 'yellow'), ('R', u'\u29E6', 'red')):
    select_mode.add(name, text=symbol, background=background)

select_mode.invoke(3)  # select break/rest as default

# ------top left buttons-------
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

    @staticmethod  # this let this method be called in class or outside
    def converter(sec):
        if sec < 0:  # This is temporary solution, there is a problem with negative modulo
            sec *= -1
            conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)
            return '-'+str(conversion)
        else:
            conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
            return conversion

    def add(self):
        if str(top_frame_input.get()) != '00:00:00':
            index = 0
            entry = Entry(select_mode.getvalue(), top_frame_input.get())
            try:
                index = entries_list.curselection()[0]  # try get position where entry should be added
            except IndexError:
                pass

            self.records.insert(index, entry)
            top_frame_input.setentry('00:00:00')
            top_frame_input.select_range(3, 5)  # entry field should be focus on minutes
            top_frame_input.icursor(5)
            self.info()
            self.update()

    def delete_item(self):
        # delete a selected line from the listbox and from entries
        try:
            # get selected line index
            index = entries_list.curselection()[0]
            entries_list.delete(index)  # delete item from listbox in GUI
            self.records.pop(index)  # delete item from data list
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
        else:  # sum for mode

            summary = 0
            for x in self.records:
                if v == x.get_mode():
                    summary += x.get_value()
            return summary

    def time_remaining(self, v):

        if v == 'total':
            total_remaining = 54000  # 15h = 54000 seconds
            total_remaining -= self.sum('total')

            if total_remaining < 0:
                total_remaining = self.converter(total_remaining)
                return str(total_remaining)+' TIME OUT!'
            return self.converter(total_remaining)

        # remaining time for modes
        elif v == 'D':
            driving_remaining = 36000  # 10h
            driving_remaining -= self.sum('D')
            if driving_remaining < 0:
                return str(self.converter(driving_remaining))+' TIME OUT!'
            else:
                return self.converter(driving_remaining)

# __________This is in progress, doesn't work very well yet__________
    def was_break(self):
        driving_time = 0
        info_list = []

        for x in self.records:

            if x.get_mode() == 'D':
                driving_time += x.get_value()

            if (x.get_mode() == 'R' and x.get_value() >= 2700) or driving_time > 16200:  # 4,5h:
                if driving_time > 16200:

                    info = "Break after 4,5h driving needed"

                    info_list.append(info)
                driving_time = 0

        if not info_list:
            return "No infringements found"

        else:
            for x in set(info_list):
                return "Infringements: "+"{0}: {1}".format(x,info_list.count(x))

# ______________________________________________

    def update(self):
        entries_list.delete(0, END)
        line_number = len(self.records)
        for record in self.records:
            entries_list.insert(END, str(line_number) + ') ' + str(record))
            # color lines:
            if record.get_mode() == 'R':
                entries_list.itemconfig(END, {'bg': 'red'}, foreground='white')
            elif record.get_mode() == 'P':
                entries_list.itemconfig(END, {'bg': 'yellow'})
            elif record.get_mode() == 'W':
                entries_list.itemconfig(END, {'bg': 'blue'}, foreground='white')
            elif record.get_mode() == 'D':
                entries_list.itemconfig(END, {'bg': 'green'}, foreground='white')

            line_number -= 1

    def info(self):
        status.set('Driving: '+str(self.converter(self.sum('D'))) +
                   ' / time remaining: '+str(self.time_remaining('D'))+'\n' +
                   'Work: '+str(self.converter(self.sum('W')))+'\n' +
                   'POA: '+str(self.converter(self.sum('P')))+'\n' +
                   'Rest: '+str(self.converter(self.sum('R')))+'\n' +
                   'Total time: ' + str(self.converter(self.sum('total')))+' / day time remaining: ' +
                   str(self.time_remaining('total'))+'\n' +
                   str(self.was_break())
                   )


class Entry:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value
        self.cleaner()

    def cleaner(self):
        user_input = str(self.value)
        user_input = re.sub('[^0-9:]', '', user_input)  # leaves only digits and ":" into input
        try:
            h, m, s = re.split(':', user_input)
            self.value = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
        except ValueError:
            try:
                m, s = re.split(':', user_input)
                self.value = int(datetime.timedelta(minutes=int(m), seconds=int(s)).total_seconds())
            except ValueError:
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
        conversion = Data().converter(self.value)  # call static method from class Data
        # sec = self.value
        # conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
        return conversion + ' ' + mode_names[self.mode]

start()
win.mainloop()
