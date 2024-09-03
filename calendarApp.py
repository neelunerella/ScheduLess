
from datetime import datetime, timedelta
import calendar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from plyer import filechooser
from kivy.graphics import Color
from kivy.graphics import Rectangle


class Appointments():
    def __init__(self):
        self.appts = []
        # appts should be set with appts.append({'date': date, 'time': time, 'place': place, 'note': note, 'priority': priority, 'fixed': fixed})
    
    def addApt(self, date, title, time, place, note, pri, fixed):
        
        self.appts.append({'date':date, 'time': time, 'title':title, 'place': place, 'note': note, 'pri': pri, 'fixed': fixed})
        self.appts.sort(key = lambda x: x['date'])
    
    def remove(self, sel):
        self.appts.remove(sel)
        
    def getApt(self, date=None):
        if date is None:
            return self.appts
        # get it for specific day
        else:
            apt = [d for d in self.appts if d['date']==date]
            return apt
        
class CalendarApp(App):
    def build(self):
        self.currYear = datetime.now().year
        self.currMonth = datetime.now().month
        self.currDay = datetime.now().day
        self.appts = Appointments()
        self.mainlayout = BoxLayout(orientation='vertical')
        self.goHome()
        return self.mainlayout
    def buildCal(self):
        
        self.mainlayout.clear_widgets()
        
        # Set the background color to teal
        with self.mainlayout.canvas.before:
            Color(0, 0.5, 0.5, 1)  # Teal color in RGBA
            self.rect = Rectangle(size=self.mainlayout.size, pos=self.mainlayout.pos)
        
        # Bind size and position updates to the rectangle to match the layout
        self.mainlayout.bind(size=self.update_rect, pos=self.update_rect)
        
        # FloatLayout to hold the menu button in the top left corner
        # top_layout = FloatLayout(size_hint=(1, None), height=75)
        menuB = Button(text="\u2015\n\u2015\n\u2015",
                       background_color=[0, 1.5, 1.5, 1], size_hint=(None, None), size=(50, 50),
                       pos_hint={'x': 0, 'top': 1}, line_height=0.3, on_press=self.getMenu)
        # top_layout.add_widget(menuB)
        self.mainlayout.add_widget(menuB)
        
        # header with month and year
        self.header = BoxLayout(size_hint_y=None, height=40)
        self.header.add_widget(Button(text="<", background_color=[0, 1.5, 1.5, 1], on_press=self.prevMonth))
        self.monthLabel = Label(text=self.getMonthYear())
        self.header.add_widget(self.monthLabel)
        self.header.add_widget(Button(text=">", background_color=[0, 1.5, 1.5, 1], on_press=self.nextMonth))
        print(self.header)
        self.mainlayout.add_widget(self.header)
        
        # Calendar grid
        self.grid = GridLayout(cols=7)
        self.create_calendar_grid()
        self.mainlayout.add_widget(self.grid)
        
        # box to hold appointment list
        self.aptlist = BoxLayout(orientation='vertical', pos_hint={'bottom':1})
        nosel = Label(text="No date selected", size_hint=(0.5, 0.5))
        self.aptlist.add_widget(nosel)
        self.mainlayout.add_widget(self.aptlist)
        
        # + button on bottom
        plus = FloatLayout(size_hint=(1, 1))
        plus.add_widget(Button(text="+", size_hint=(None, None), font_size=50,
                               size=(100, 100), pos_hint={'right':1, 'bottom':1},
                               background_color=[0, 1.5, 1.5, 1], 
                               on_press=self.addAptCal))
        
        
        self.mainlayout.add_widget(plus)
        return self.mainlayout
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def addAptCal(self, instance):
        # this makes it stack on top of each other instead of vertical
        mbox = BoxLayout(orientation='vertical', pos_hint={'right':1, 'bottom':1})
        addEvent = Button(text="Add an Event", on_press=self.addEvent)
        mbox.add_widget(addEvent)
        createEvent = Button(text="Add a Task", on_press=self.addTask)
        mbox.add_widget(createEvent)
        popup = Popup(title="Add to Calendar", content=mbox, size_hint=(0.25, 0.25))
        #popup = Popup(title="Add to Calendar", content=mbox, size_hint=(0.5, 0.5))
        popup.open()
        
    def addEvent(self, instance=None):
        self.mainlayout.clear_widgets()
        # change color to white       
        with self.mainlayout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.mainlayout.size, pos=self.mainlayout.pos)
            
        # Bind size and position updates to the rectangle to match the layout
        self.mainlayout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Menu button on top
        menuB = Button(text="\u2015\n\u2015\n\u2015",
                       background_color=[0, 1.5, 1.5, 1], size_hint=(None, None), size=(50, 50),
                       pos_hint={'x': 0, 'top': 1}, line_height=0.3, on_press=self.getMenu)
        # top_layout.add_widget(menuB)
        self.mainlayout.add_widget(menuB)
        # set buttons to determine 
        fixed = True
        # make a grid layout (3 cols)
        timingLayout = GridLayout(cols=3, padding=10, spacing=10, size_hint_y = None, height=300)
        timingLayout.add_widget(Label(text="Starts", color=[0, 0, 0, 1]))
        # sDate = Button(text=f"{datetime(self.currYear, self.currMonth, self.currDay).strftime('%B %d, %Y')}", color=[0, 0, 0, 1], on_press=self.smallCal(timingLayout))
        # sTime = Button(text=f"{datetime.now().hour}:{datetime.now().minute+5}", color=[0, 0, 0, 1], on_press=self.timeScroll)
        # eDate = Button(text=f"{datetime(self.currYear, self.currMonth, self.currDay).strftime('%B %d, %Y')}", color=[0, 0, 0, 1], on_press=self.smallCal(timingLayout))
        # eTime = Button(text=f"{datetime.now().hour+1}:{datetime.now().minute+5}", color=[0, 0, 0, 1], on_press=self.timeScroll)
        # timingLayout.add_widget(sDate)
        # timingLayout.add_widget(sTime)
        # timingLayout.add_widget(Label(text="Ends:", color=[0, 0, 0, 1]))
        # timingLayout.add_widget(eDate)
        # timingLayout.add_widget(eTime)
        
        # title, location, notes
        dets = GridLayout(cols = 2, padding=10, spacing=10, size_hint_y=None, height=300)
        dets.add_widget(Label(text="Title: ", color=[0, 0, 0, 1]))
        title = TextInput(text="", multiline=False)
        dets.add_widget(title)
        
        dets.add_widget(Label(text="Location: ", color=[0, 0, 0, 1]))
        loc = TextInput(text="", multiline=False)
        dets.add_widget(loc)
        
        dets.add_widget(Label(text="Notes: ", color=[0, 0, 0, 1]))
        notes = TextInput(text="", multiline=True)
        dets.add_widget(notes)
        # 2 buttons at header: Cancel and Done
        header = BoxLayout(orientation='horizontal')
        cancelB = Button(text="Cancel", pos_hint={'top':1, 'left':1}, size_hint=(None, None),size=(100, 50), on_press=self.goHome)
        doneB = Button(text="Done", pos_hint={'top':1, 'right':1}, size_hint=(None, None), size=(100, 50), on_press=self.goHome)
        header.add_widget(cancelB)
        header.add_widget(doneB)
        
        
        self.mainlayout.add_widget(header)
        # self.mainlayout.add_widget(timingLayout)
        self.mainlayout.add_widget(dets)
        
    def smallCal(self, tl):
        # add it into timinglayout
        tl.add_widget(self.create_calendar_grid())
        
    def timeScroll(self, tl):
        # add it into timinglayout
        # make it a scroll bar for time
        tl.add_widget(self.create_calendar_grid())
        
    
    def addTask(self, instance):
        self.mainlayout.clear_widgets()
    
    def create_calendar_grid(self):
        # Clear existing widgets
        self.grid.clear_widgets()
        
        # Add day headers
        for day in ['S', 'M', 'T', 'W', 'Th', 'F', 'S']:
            self.grid.add_widget(Label(text=day))
        
        # get calendar for curr month/year
        cal = calendar.monthcalendar(self.currYear, self.currMonth)
        for week in cal:
            for day in week:
                if day == 0:
                    self.grid.add_widget(Label(text=""))
                else:
                    btn = Button(text=str(day), background_color=[0, 1.5, 1.5, 1], on_press=self.onDayPress)
                    self.grid.add_widget(btn)
    
    def onDayPress(self, instance):
        day = instance.text
        selected = f"{self.currYear}-{str(self.currMonth).zfill(2)}-{str(day).zfill(2)}"
        selapt = self.appts.getApt(date=selected)
        self.aptlist.clear_widgets()
        selapt.sort(key = lambda x: x['time'])
        
        # Need to organize selapt based on time
        
        title = Label(text=f"{self.getMonthDayYear(day)} Selected", size_hint=(0.5, 0.5))
        self.aptlist.add_widget(title)
        if selapt == []:
            label=Label(text="No Scheduled Events")
            self.aptlist.add_widget(label)
        else:
            for sel in selapt:
                # need to put time first, then title of task, place, note?
                label = Label(text=f"| {sel['time']} {sel['title']} at {sel['place']}\n     {sel['note']}")
                self.aptlist.add_widget(label)
        #self.mainlayout.add_widget(aptlist)
        
    def getMonthDayYear(self, day):
        return datetime(self.currYear, self.currMonth, 1).strftime(f"%B {day} %Y")
    
    def getMonthYear(self):
        return datetime(self.currYear, self.currMonth, 1).strftime("%B %Y")
    
    def prevMonth(self, instance):
        if self.currMonth == 1:
            self.currMonth = 12
            self.currYear -= 1
        else:
            self.currMonth -= 1
        self.monthLabel.text = self.getMonthYear()
        self.create_calendar_grid()
    
    def nextMonth(self, instance):
        if self.currMonth == 12:
            self.currMonth = 1
            self.currYear += 1
        else:
            self.currMonth += 1
        self.monthLabel.text = self.getMonthYear()
        self.create_calendar_grid()
        
    def getMenu(self, instance):
        # stick it all in one layer and stick layer in popup
        # find a way to stick popup on left side of screen
        menulayout = BoxLayout(orientation='vertical', pos_hint={'top':1})
        with menulayout.canvas.before:
            Color(1, 1, 1, 1)  # White color in RGBA
            self.rect = Rectangle(size=menulayout.size, pos=menulayout.pos)
    
        # Bind size and position to the rectangle to ensure it resizes with the layout
        menulayout.bind(size=self.update_rect, pos=self.update_rect)
        
        # home button
        homeB = Button(
        size_hint=(1, 0.5),
        size=(100, 100),
        pos_hint={'top': 1},
        on_press=lambda *args:(popup.dismiss(), self.goHome()),
        background_normal='ScheduLess Name.png',  # Image file
        background_down='ScheduLess Name.png',    # Ensures the same image when pressed
                               # Allow the image to stretch to fit the button size
    )
        menulayout.add_widget(homeB)
        
        # add button for Calendar, Profile, and settings at bottom
        # calB = Button(text="Calendar", size_hint=(1, 0.25), 
        #               background_color=[1, 1, 1, 1], color=[0, 0, 0, 1], 
        #               on_press=self.build)
        calB = Button(
            text="Calendar",
            size_hint=(1, 0.25),
            on_press=lambda *args:(popup.dismiss(), self.buildCal()),
            background_normal='white.png',  # White background
            color=[0, 0, 0, 1]  # Black text color
        )
        profileB = Button(
            text="Profile",
            size_hint=(1, 0.25),
            on_press=lambda *args: (popup.dismiss(), self.proBuild(instance)),
            background_normal='white.png',  # White background
            color=[0, 0, 0, 1]  # Black text color
        )
        settingsB = Button(
            text="Settings",
            size_hint=(1, 0.25),
            on_press=self.goSettings,
            background_normal='white.png',  # White background
            color=[0, 0, 0, 1]  # Black text color
        )
        
        menulayout.add_widget(calB)
        menulayout.add_widget(profileB)
        menulayout.add_widget(settingsB)
        
        popup = Popup(title="", content=menulayout,background='white.png', 
                      background_color=(1, 1, 1, 1), pos_hint={'left':1}, 
                      size_hint=(0.5, 1))
        popup.open()
    def proBuild(self, instance):
        self.mainlayout.clear_widgets()
        #popup = Popup(title='Profile Settings', size=self.mainlayout.size, pos=self.mainlayout.pos, background='white.png')
        
        # change background to white
        with self.mainlayout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.mainlayout.size, pos=self.mainlayout.pos)
            
        # Bind size and position updates to the rectangle to match the layout
        self.mainlayout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Menu button on top
        menuB = Button(text="\u2015\n\u2015\n\u2015",
                       background_color=[0, 1.5, 1.5, 1], size_hint=(None, None), size=(50, 50),
                       pos_hint={'x': 0, 'top': 1}, line_height=0.3, on_press=self.getMenu)
        # top_layout.add_widget(menuB)
        self.mainlayout.add_widget(menuB)
        
        # middle is horiz layout for pfp and names where names are in vert layout
        #middle = FloatLayout(orientation='horizontal')
        middle = BoxLayout(orientation='horizontal')
        names = BoxLayout(orientation='vertical', pos_hint={'left':1}, size_hint=(.50, .25))
        
        # pfp section
        pLayout = BoxLayout(orientation='vertical', pos_hint={'top':1})
        self.pfp = Image(source='default pfp.png', size_hint=(None, None), size=(150, 150), pos_hint={'top':1})
        changePfpB = Button(text="Change Picture", size_hint=(None, None), size=(225, 50), on_press=self.changePic)
        pLayout.add_widget(self.pfp)
        pLayout.add_widget(changePfpB)
        middle.add_widget(pLayout)
        
        
        # Names section
        firstInput = TextInput(text="First Name", multiline=False, height=30)
        names.add_widget(firstInput)
        lastInput = TextInput(text="Last Name", multiline=False, height=300)
        names.add_widget(lastInput)
        
        middle.add_widget(names)
        #self.mainlayout.add_widget(middle)
        
        # profile details
        proDetails = GridLayout(cols=2, padding=10, spacing=10, size_hint_y = None, height=300)
        proDetails.add_widget(Label(text="Username:", color=[0, 0, 0, 1]))
        userInput = TextInput(text="Username", multiline=False)
        proDetails.add_widget(userInput)
        
        proDetails.add_widget(Label(text="Password:", color=[0, 0, 0, 1]))
        pwInput = TextInput(text="Password", multiline=False, password=True)
        proDetails.add_widget(pwInput)
        
        proDetails.add_widget(Label(text="Email:", color=[0, 0, 0, 1]))
        emInput = TextInput(text="Email", multiline=False)
        proDetails.add_widget(emInput)
        
        proDetails.add_widget(Label(text="Number:", color=[0, 0, 0, 1]))
        numInput = TextInput(text="Number", multiline=False)
        proDetails.add_widget(numInput)
        
        # header has 2 buttons: X and Save on left and right side
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
        xB = Button(text="X", pos_hint={'top':1,'left':1},size_hint=(0.25, 0.25), on_press= self.goHome, background_color=[0, 1.5, 1.5, 1])
        save = Button(text="Save", pos_hint={'top':1,'right':1}, size_hint=(0.25, 0.25),
                      on_press=lambda *args: self.savePro(firstInput, lastInput, emInput, numInput, userInput, pwInput), background_color=[0, 1.5, 1.5, 1])
        header.add_widget(xB)
        header.add_widget(save)
        self.mainlayout.add_widget(header)
        self.mainlayout.add_widget(middle)
        self.mainlayout.add_widget(proDetails)
        
        
        
    def savePro(self, first, last, email, number, username, password):
        # do the stuff
        self.first = first.text
        self.last = last.text
        self.email = email.text
        self.num = number.text
        self.user = username.text
        self.password = password.text
        
    def changePic(self, instance):
        fileChooser = FileChooserIconView()
        popup = Popup(title="Select Profile Picture", content=fileChooser, size_hint=(0.9, 0.9))
        fileChooser.bind(on_selection=lambda _, selection: self.onPicSel(selection, popup))
        popup.open()
        
    def onPicSel(self, selection, popup):
        if selection:
            import shutil
            from os.path import join, basename
            from kivy.utils import platform
            if platform == 'ios':
                # save to app's sandbox diirectory
                dest_path = join(expanduser("~"), "Documents", basename(selection[0]))
                shutil.copy(selection[0], dest_path)
                self.pfp.source = dest_path
            else:
                self.pfp.source = selection[0]
        popup.dismiss()
    
    def goSettings(self):
        self.mainlayout.clear_widgets()
    def goHome(self, instance=None):
        self.mainlayout.clear_widgets()
        
        # change background to white
        with self.mainlayout.canvas.before:
            Color(1, 1, 1, 1)  # White color in RGBA
            self.rect = Rectangle(size=self.mainlayout.size, pos=self.mainlayout.pos)
        
        # Bind size and position updates to the rectangle to match the layout
        self.mainlayout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Menu button on top
        menuB = Button(text="\u2015\n\u2015\n\u2015",
                       background_color=[0, 1.5, 1.5, 1], size_hint=(None, None), size=(50, 50),
                       pos_hint={'x': 0, 'top': 1}, line_height=0.3, on_press=self.getMenu)
        # top_layout.add_widget(menuB)
        self.mainlayout.add_widget(menuB)
        
        # stick 7 day calendar with dates on top with all scheduled events
        # header with month and year
        self.header = BoxLayout(size_hint_y=None, height=40)
        self.header.add_widget(Button(text="<", background_color=[0, 1.5, 1.5, 1], on_press=self.prevWeek))
        self.weekLabel = Label(text=self.getWeekRange(), color=[0, 0, 0, 1])
        self.header.add_widget(self.weekLabel)
        self.header.add_widget(Button(text=">", background_color=[0, 1.5, 1.5, 1], on_press=self.nextWeek))
        print(self.header)
        self.mainlayout.add_widget(self.header)
        
        # Calendar grid
        self.grid = GridLayout(cols=7)
        self.create_week_grid()
        self.mainlayout.add_widget(self.grid)
        
        # 2 buttons: create for me and add event
        bottom = BoxLayout(orientation='vertical', pos_hint={'center_x':0.5, 'center_y':0.5})
        createForMe = Button(text="Create for Me",
                             background_color=[0.7, 1, 0.7, 1],
                             size_hint=(0.4, 0.2),
                             height=50, pos_hint={'center_x':0.5},
                             on_press=self.addTask)
        addEvent = Button(text="Add an Event",
                          background_color=[0, 1, 1, 1], size_hint=(0.4, 0.2),
                          height=50, pos_hint={'center_x':0.5},
                          on_press=self.addEvent)
        bottom.add_widget(createForMe)
        bottom.add_widget(addEvent)
        self.mainlayout.add_widget(bottom)
        
        
    def create_week_grid(self):
        self.grid.clear_widgets()
        
        # Add day headers
        for day in ['S', 'M', 'T', 'W', 'Th', 'F', 'S']:
            self.grid.add_widget(Label(text=day, color=[0, 0, 0, 1]))
            
        # Get the current weekday and calculate the start of the week
        curr_date = datetime(self.currYear, self.currMonth, self.currDay)
        start_date = curr_date - timedelta(days=curr_date.weekday() % 7)
     
        # Create layouts for each day of the week
        for i in range(7):
            day = start_date + timedelta(days=i)
            dayLayout = BoxLayout(orientation='vertical')
            dayHeader = Label(text=str(day.day), pos_hint={'top':1},
                        color=[0, 0, 0, 1])
            
            # getting selapt
            selected = f"{day.year}-{str(day.month).zfill(2)}-{str(day.day).zfill(2)}"
            selapt = self.appts.getApt(date=selected)
            
            scroll_view = ScrollView(size_hint=(1, None), size=(self.grid.width, 100))
            dayEvents = BoxLayout(orientation='vertical')
            dayEvents.bind(minimum_height=dayEvents.setter('height'))
            # Create a highlighted layout for "No Events Scheduled"
            highlighted_box = BoxLayout(orientation='horizontal')
            
            
            selapt.sort(key = lambda x: x['time'])
            
            if selapt == []:
                label = Label(text="No Scheduled Events", color = [0, 0, 0, 1], font_size='10sp')
                # with highlighted_box.canvas.before:
                #     Color(1, 1, 1, 0.5)  # Grey background with 50% opacity
                #     self.rect = Rectangle(size=highlighted_box.size, pos=highlighted_box.pos)
                # highlighted_box.bind(size=self.update_rect, pos=self.update_rect)
                # highlighted_box.add_widget(label)
                dayEvents.add_widget(label)
            else:
                for sel in selapt:
                    label = Button(text=f"| {sel['time']}: {sel['title']} at {sel['place']}\n     {sel['note']}", color=[0,0,0,1], on_press=self.eventDetails(sel, selapt))
                    dayEvents.add_widget(label)
                    
            dayLayout.add_widget(dayHeader)
            scroll_view.add_widget(dayEvents)
            dayLayout.add_widget(scroll_view)
            self.grid.add_widget(dayLayout)
            
    def eventDetails(self, sel, selapt):
        # floatlayout with label and delete button at bottom
        float = FloatLayout(orientation='vertical')
        details = Label(text=f"| {sel['time']}: {sel['title']} at {sel['place']}\n     {sel['note']}", color=[0,0,0,1])
        deleteB = Button(text="Delete Event", pos_hint={'bottom':1}, on_press=lambda *args: (selapt.remove(sel), popup.dismiss()))
        float.add_widget(details)
        float.add_widget(deleteB)
        popup = Popup(title="Event Details", content=float)
        popup.open()
            
    def getWeekRange(self):
        curr_date = datetime(self.currYear, self.currMonth, self.currDay)
        start_date = curr_date - timedelta(days=curr_date.weekday())
        end_date = start_date + timedelta(days=6)
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
            
    def prevWeek(self, instance):
        curr_date = datetime(self.currYear, self.currMonth, self.currDay)
        new_date = curr_date - timedelta(days=7)
        self.currYear, self.currMonth, self.currDay = new_date.year, new_date.month, new_date.day
        self.weekLabel.text = self.getWeekRange()
        self.create_week_grid()
    
    def nextWeek(self, instance):
        curr_date = datetime(self.currYear, self.currMonth, self.currDay)
        new_date = curr_date + timedelta(days=7)
        self.currYear, self.currMonth, self.currDay = new_date.year, new_date.month, new_date.day
        self.weekLabel.text = self.getWeekRange()
        self.create_week_grid()
        
if __name__ == "__main__":
    CalendarApp().run()

        

            
        
 