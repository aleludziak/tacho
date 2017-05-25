from tkinter import *
import re
import datetime
import Pmw
# import time

# sec_now = time.time()
# now = time.localtime(sec_now)


def start():
    global current_data
    current_data = Data()
    current_data.update()
    # current_data.info()


def add_entry():
    current_data.add(top_frame_input.get(), select_mode.getvalue())

'''
def set_daily_rest():
    current_data.delete_item(True)

    current_data.add(daily_rest.get(), 'R', True)
'''


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


topFrame = Frame(win)
# topFrame.pack(fill=BOTH)
topFrame.grid(row=0, column=0, columnspan=2)

'''
topLeftFrame = Frame(win)
topLeftFrame.grid(row=0, column=0)

topRightFrame = Frame(win)
topRightFrame.grid(row=0, column=1)
'''
leftFrame = Frame(win)
leftFrame.grid(row=1, column=0)

middleFrame = Frame(win)
middleFrame.grid(row=1, column=1)

rightFrame = Frame(win)
rightFrame.grid(row=1, column=2)

bottomFrame = Frame(win)
bottomFrame.grid(row=2, columnspan=3)

# -------keys actions-----
win.bind("<Return>", lambda a: add_entry())
win.bind("<KP_Enter>", lambda a: add_entry())
win.bind("<KP_Add>", lambda a: add_entry())
# win.bind("<KP_Decimal>", lambda a: num_press(":"))

# ==========input entry===========

top_frame_input = Pmw.Counter(middleFrame,
                              entry_font="Helvetica 20 bold",
                              entry_width=12,
                              autorepeat=True, datatype='time',
                              entryfield_validate={'validator': 'time'},
                              entryfield_value='00:00:00',
                              increment=60)
top_frame_input.grid(row=0, column=0, columnspan=5)

top_frame_input.component('entry').focus_set()
top_frame_input.select_range(3, 5)
top_frame_input.icursor(5)

'''
set_date = Pmw.Counter(leftFrame, labelpos='w',
                       label_text='Shift date:',
                       entry_width=10,
                       entryfield_value=time.strftime('%d/%m/%Y', now),
                       datatype = {'counter' : 'date', 'format' : 'dmy', 'yyyy' : 1})

set_date.grid(row=0, column=1, stick=W)
'''
dialog1 = Pmw.MessageDialog(win, title='Info', defaultbutton=0,
                            message_text='To change daily break use update button',
                            iconpos='w', icon_bitmap='warning')
#dialog1.iconname('Please set daily break')
dialog1.withdraw()

balloon = Pmw.Balloon(win)
'''
daily_rest = Pmw.Counter(leftFrame, labelpos='w',
                         label_text='Set daily rest: ',
                         entry_width=9,
                         entryfield_validate={'validator': 'time'},
                         entryfield_value='11:00:00',  # time.strftime('%H:%M:%S', now),
                         datatype = {'counter' : 'time', 'time24' : 1},
                         increment=60)

daily_rest.grid(row=0, column=0, stick=W, pady=1, padx=1)
'''
'''
set_time_button = Button(leftFrame, text='Update', command=set_daily_rest)
set_time_button.grid(row=0, column=1, pady=1, padx=1, stick=W)
balloon.bind(set_time_button, 'Update daily rest')
'''
# ===========Listbox with scrollbar=================

entries_list = Pmw.ScrolledListBox(leftFrame, hscrollmode='none', vscrollmode='static',
                                   usehullsize=1, hull_height=250, hull_width=350)
                                   #listbox_height=15, listbox_width=40)
'''
entries_list = Pmw.ComboBox(leftFrame, dropdown = 0, scrolledlist_vscrollmode = 'static',
                            scrolledlist_hscrollmode = 'none', scrolledlist_listbox_height = 15,
                            scrolledlist_listbox_width=40,
                            entryfield_validate = {'validator' : 'time'},
                            entryfield_value = '00:00:00',
                            )
'''

entries_list.grid(row=0, column=0, columnspan=4)


# =======buttons===========
# -------num pad-----------
keyboard = []
keys = "789456123C0:"
i = 0
for j in range(2, 6):
    for k in range(3):
        keyboard.append(Button(middleFrame, text=keys[i], font="Helvetica 15 bold", height=1, width=2))
        keyboard[i].grid(row=j, column=k, pady=2, padx=2)
        keyboard[i]["command"] = lambda x=keys[i]: num_press(x)
        i += 1

# --------other buttons in num pad---------
add_entry_button = Button(middleFrame, text='+', font="Helvetica 15 bold", height=6, width=7, command=add_entry)
add_entry_button.grid(row=2, column=3, rowspan=4, columnspan=2, pady=2, padx=2)

clear_one_button = Button(middleFrame, text="←", font="Helvetica 15 bold", height=1, width=2, command=clear_one)
clear_one_button.grid(row=1, column=4, pady=2, padx=2)

# ------buttons to change mode of entry-------
select_mode = Pmw.RadioSelect(middleFrame, Button_height=1, Button_width=2,
                              Button_font="Helvetica 15 bold", pady=2, padx=2)

select_mode.grid(row=1, column=0, columnspan=4)

# Add some buttons to the horizontal RadioSelect - mode selection buttons.
for name, balloon_info, symbol, background in (('D', 'Driving', u'\u2609', 'green'),
                                               ('W', 'Work', u'\u2692', 'blue'),
                                               ('P', 'POA', u'\u26DD', 'yellow'),
                                               ('R', 'Rest/Break', u'\u29E6', 'red')):
    button = select_mode.add(name, text=symbol, background=background)
    balloon.bind(button, balloon_info)

select_mode.invoke(3)  # select break/rest as default

# ------listbox buttons-------
listbox_buttons = Pmw.ButtonBox(leftFrame,  # Button_height=1,  # Button_width=2,
                                # pady=1, padx=1,
                                Button_font="Helvetica 12")

listbox_buttons.grid(row=2, column=0, columnspan=2, stick=W)

# Add some buttons to the horizontal RadioSelect.
listbox_buttons.add('Delete Entry', command=lambda: current_data.delete_item())
# listbox_buttons.add('Edit')
# listbox_buttons.add('Save')
listbox_buttons.add('Clear All', command=start)


# =====bottom status=============
right_status_info = StringVar()
right_status_total = Label(rightFrame, textvariable=right_status_info, bd=1, relief=SUNKEN,
                           font="Helvetica 15 bold", width=42, height=11)
right_status_info.set("")
right_status_total.pack(fill=X, expand=True, side=TOP, ipady=10, ipadx=10)

# ====infringements status on right=================
bottom_infringements_status = StringVar()

infringements_status = Label(bottomFrame, textvariable=bottom_infringements_status, bd=1, relief=SUNKEN,
                             font="Helvetica 15 bold", width=100)
bottom_infringements_status.set("")
infringements_status.pack(fill=BOTH, expand=True, side=TOP, ipady=10, ipadx=10)


class Data:

    def __init__(self):
        self.records = []

        self.reduced_break = False

        if not self.records:

            self.records = []
            self.records.insert(0, Entry('R', '678:00:00'))

    @staticmethod  # this let this method be called in class or outside
    def converter(sec):
        # Conversion from seconds to HH:MM:SS, to be more readable for user
        if sec < 0:  # This is temporary solution, there is a problem with negative modulo
            sec *= -1
            conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)
            return '-'+str(conversion)
        else:
            conversion = '%d:%02d:%02d' % (sec / 3600, sec / 60 % 60, sec % 60)  # convert to HH:MM:SS
            return conversion

    def add(self, user_input, mode, access=False):
        # Check if user trying to add first item on list,
        # Only function set_daily_rest can do it to update first break
        if str(user_input) != '00:00:00':

            entry = Entry(mode, user_input)

            try:
                index = entries_list.curselection()[0]  # try get position where entry should be added
                if index == 0 and access is True:
                    self.records.insert(0, entry)
                elif index == 0 and access is False:
                    pass  # dialog1.activate(geometry = 'first+100+100')
                else:
                    self.records.insert(index, entry)
            except IndexError:
                if access is True:
                    self.records.insert(0, entry)
                else:
                    self.records.append(entry)

            # self.records.insert(index, entry)
            top_frame_input.setentry('00:00:00')
            top_frame_input.select_range(3, 5)  # entry field should be focus on minutes
            top_frame_input.icursor(5)

            self.update()

    def delete_item(self, access=False):
        # delete a selected line from the listbox and from entries
        # Check if user trying to delete first item on list,
        # Only function set_daily_rest can do it to update first break

        try:
            # get selected line index
            index = entries_list.curselection()[0]
            if index == 0 and access is True:

                entries_list.delete(0)  # delete item from listbox in GUI
                self.records.pop(0)  # delete item from data list
                self.update()
            elif index == 0 and access is False:
                pass
            else:

                entries_list.delete(index)  # delete item from listbox in GUI
                self.records.pop(index)  # delete item from data list
                self.update()

        except IndexError:
            if access is True:
                entries_list.delete(0)  # delete item from listbox in GUI
                self.records.pop(0)  # delete item from data list
                self.update()
            else:
                pass

    def sum(self, v):
        total = 0

        if v == 'total':

            for x in self.records:
                if x.get_mode() == 'R' and x.get_value() >= 32400:
                    total = 0
                else:
                    total += x.get_value()
            return total
        else:  # sum for mode

            summary = 0
            for x in self.records:
                if v == x.get_mode():

                    summary += x.get_value()
                if x.get_mode() == 'R' and x.get_value() >= 32400:
                    summary = 0

            return summary

    def time_remaining(self, v):
        total_remaining = 54000  # 15h = 54000 seconds
        driving_remaining = 36000  # 10h

        # This doesn't work very well yet!!!
        if count['exceeded_daily_driving'] >= 2:
            driving_remaining = 32400  # 9h

        if count['reduced_daily_rest'] >= 3:
            total_remaining = 46800  # 13h

        if v == 'total':

            total_remaining -= self.sum('total')

            return total_remaining

        # remaining time for modes
        elif v == 'D':
            driving_remaining -= self.sum('D')

            return driving_remaining

        elif v == 'break':

            time = 0
            for x in self.records:

                if x.get_mode() == 'R' and x.get_value() >= 32400:  # >=9h
                    # sum time of entries bigger than 13 h or daily break less than 11h
                    if (time > 46800 and x.get_value() < 86400) or 32400 <= x.get_value() < 39600:
                        break_info = 'Reduced daily break'

                    elif 39600 <= x.get_value() < 86400:
                        break_info = 'Full daily break taken'
                    elif 86400 <= x.get_value() < 162000 :  # between 24h and 45h
                        break_info = 'Reduced weekly rest'
                    else:
                        break_info = 'Full weekly rest taken'

                    time = 0



                else:
                    time += x.get_value()
            return break_info

    def infringements(self):
        global weekly_total_time_info, fortnight_driving_time_info, infringements_list, count

        driving_time = 0  # can't be more than 4,5h before break
        working_time = 0  # it's time of work or driving and can't be more than 6h
        daily_driving_time = 36000  # 10h
        count = {'exceeded_daily_driving': 0, 'reduced_daily_rest': 0}
        daily_total_time = 54000  # 15h
        weekly_total_time = 518400  # 6x24h
        weekly_driving_time = 201600  # 56h

        fortnight_driving_time = 324000  # 90h
        fortnight = True  # because first item on records is break

        reduced_weekly_rest = False
        first_break = False
        second_break = False
        infringements_list = []
        for x in self.records:
            daily_total_time -= x.get_value()
            weekly_total_time -= x.get_value()

            # driving
            if x.get_mode() == 'D':
                driving_time += x.get_value()
                daily_driving_time -= x.get_value()
                if daily_driving_time < 3600:  # less than 1h so more than 9h driving
                    count['exceeded_daily_driving'] += 1
                weekly_driving_time -= x.get_value()
                fortnight_driving_time -= x.get_value()

            # driving or work
            if x.get_mode() == 'D' or x.get_mode() == 'W':
                working_time += x.get_value()

            if x.get_mode() == 'R' and (900 <= x.get_value() < 1800):
                first_break = True

            # First break must be at least 15 minutes and second 30 minutes.
            if x.get_mode() == 'R' and (1800 <= x.get_value() < 2700):
                if first_break is True:
                    second_break = True
                else:
                    first_break = True

            # break 45 minutes or more (also can be split to 15min and 30min)
            if (x.get_mode() == 'R' and x.get_value() >= 2700) or (second_break is True):
                '''
                if driving_time > 16200:

                    info = "Break after 4,5h driving needed"
                    infringements_list.append(info)
                driving_time = 0

                if working_time > 21600:
                    info_break = "Break after 6h work needed"
                    infringements_list.append(info_break)
                '''
                driving_time = 0
                working_time = 0
                first_break = False
                second_break = False

                if x.get_value() >= 32400:  # >=9h
                    daily_total_time += x.get_value()  # do not count last break for daily_total_time

                    # reduced daily break - more than 13h of work or rest between 9h and 11h
                    if (daily_total_time < 7200 and x.get_value() < 86400) or 32400 <= x.get_value() < 39600:

                        count['reduced_daily_rest'] += 1

                    # full daily break between 11h and 24h
                    elif 39600 <= x.get_value() < 86400:
                        pass
                    # weekly break between 24h and 45h
                    elif x.get_value() >= 86400 :  # more than 24h

                        if reduced_weekly_rest is True:

                        # you can't take two reduced rests one after another,
                        # but you can skip day at work during week - it must be fixed

                            # infringements_list.append("Second reduced weekly break taken")
                            reduced_weekly_rest = False
                        else:
                            reduced_weekly_rest = True

                        weekly_total_time = 518400
                        weekly_driving_time = 201600

                        if fortnight is False:
                            fortnight = True

                        else:
                            fortnight_driving_time = 324000
                            fortnight = False

                        count['exceeded_daily_driving'] = 0
                        count['reduced_daily_rest'] = 0

                    # full weekly rest more than 45h
                        if x.get_value() >= 162000:  # more than 45h
                            reduced_weekly_rest = False

                    daily_total_time = 54000
                    daily_driving_time = 36000

            if driving_time > 16200:
                info_driving_break = "Break after 4,5h driving needed"
                infringements_list.append(info_driving_break)
                driving_time = 0

            if working_time > 21600:
                info_break = "Break after 6h work needed"
                infringements_list.append(info_break)
                working_time = 0

            if daily_total_time < 0:
                infringements_list.append('Available daily shift time exceeded')
                daily_total_time = 54000

            if daily_driving_time < 0:
                infringements_list.append('Available daily driving time exceeded')
                daily_driving_time = 36000

            if weekly_total_time < 0:
                infringements_list.append('Available weekly total time of work exceeded')
                weekly_total_time = 518400

            if weekly_driving_time < 0:
                infringements_list.append('Available weekly total driving time exceeded')
                weekly_driving_time = 201600

            if fortnight_driving_time < 0:
                infringements_list.append('Fortnight total driving time exceeded')
                fortnight_driving_time = 324000

            # if more than two times between two weekly rests driving time is more than 9h
            if count['exceeded_daily_driving'] > 2:
                infringements_list.append('Exceeded daily driving time already used')
                count['exceeded_daily_driving'] = 0

            if count['reduced_daily_rest'] > 3:
                infringements_list.append('Too many reduced daily breaks between 2 weekly rest periods')
                count['reduced_daily_rest'] = 0



        '''
        if self.time_remaining('total') < 0:
            infringements_list.append('TOTAL TIME OUT')
        if self.time_remaining('D') < 0:
            infringements_list.append('DRIVING TIME OUT')

        try:  # When first break is update firstly has to be deleted and then index error occurs

            if self.records[0].get_value() < 32400:
                infringements_list.append('Not enough daily break')

        except IndexError:
            pass
        '''
        fortnight_driving_time_info = str(self.converter(fortnight_driving_time))
        weekly_total_time_info = str(self.converter(weekly_total_time))
        # return infringements_list

    def lineup_infringements(self, items_list):
        # Takes list of infringements and change it to readable string
        if not items_list:
            info_infringements = 'No infringements found'
            return info_infringements
        else:
            all_infringements = ''
            for x in set(items_list):
                if items_list.count(x) == 1:
                    all_infringements += "{0}\n".format(x, items_list.count(x))

                else:
                    all_infringements += "{0}: {1}\n".format(x, items_list.count(x))
            info_infringements = "Infringements:\n"+all_infringements
            return info_infringements

    def update(self):
        self.infringements()
        entries_list.delete(0, END)

        for (index, record) in enumerate(self.records):
            if index == 0:
                entries_list.insert(index, 'List of Entries:')

            elif record.get_mode() == 'R':
                if record.get_value() >= 32400:
                    entries_list.insert(index, ('DAILY/WEEKLY REST: '+str(record)[:-11]))
                    entries_list.itemconfig(END, {'bg': 'white'}, foreground='black')
                else:
                    entries_list.insert(index, (str(index)+') '+str(record)))
                    entries_list.itemconfig(END, {'bg': 'red'}, foreground='white')
            else:
                entries_list.insert(index, (str(index)+') '+str(record)))
                if record.get_mode() == 'P':
                    entries_list.itemconfig(END, {'bg': 'yellow'})
                if record.get_mode() == 'W':
                    entries_list.itemconfig(END, {'bg': 'blue'}, foreground='white')
                if record.get_mode() == 'D':
                    entries_list.itemconfig(END, {'bg': 'green'}, foreground='white')

        self.info()
        entries_list.see(END)  # Keep focus on last item on listbox

    def info(self):
        right_status_info.set(str(self.time_remaining('break')) + '\n' + '\n' +
                              'Total day time: ' + str(self.converter(self.sum('total'))) + ' / time remaining: ' +
                              str(self.converter(self.time_remaining('total'))) + '\n' + '\n' +
                              'Driving: ' + str(self.converter(self.sum('D'))) +
                              ' / time remaining: ' + str(self.converter(self.time_remaining('D'))) + '\n' +
                              'Work: ' + str(self.converter(self.sum('W'))) + ' | ' +
                              'POA: ' + str(self.converter(self.sum('P'))) + ' | ' +
                              'Rest: ' + str(self.converter(self.sum('R'))) + '\n'
                              'Exceeded daily driving time this week: ' + str(count['exceeded_daily_driving']) + '\n'
                              'Reduced daily rests this week: ' + str(count['reduced_daily_rest'])+ '\n' + '\n' +
                              'Fortnight driving remain: ' + fortnight_driving_time_info + '\n' +
                              'Time left before weekly rest: ' + weekly_total_time_info


                              )

        bottom_infringements_status.set(self.lineup_infringements(infringements_list))


class Entry:
    def __init__(self, mode, value):
        self.mode = mode
        self.value = value
        self.cleaner()

    # Before entry will be added it has to be cleaned from user mistakes and converted from HH:MM:SS to seconds
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
