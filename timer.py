import kivy
from kivy.app import App
from kivy.uix.button import Label,Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
import time
import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
import sqlite3
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import win32gui
import win32con
class newButton(Button):
    def __init__(self,**kargs):
        Button.__init__(kargs)
        self.a = 0
class HelloKivy(App):
    #a = NumericProperty(5)
    l1 = Label(text = "timer1",font_size='40sp')
    count = 60
    mins = 45
    def callback(self,instance):
            
            self.df = pd.read_csv('logs.csv',index_col = 0)
            self.a = NumericProperty(5)
            Animation.cancel_all(self)  # stop any current animations
            self.anim = Animation( duration=45*60.,opacity = 1)
            
            def finish_callback(animation, incr_crude_clock):
                incr_crude_clock.text = "FINISHED"
                incr_crude_clock.text = "Start Again"
                i = len(self.df)
                sub = self.txt1.text
                self.df = self.df.append({"time_end":pd.Timestamp.now(),'subject': sub,"duration":45}, ignore_index=True)
                self.df.to_csv("logs.csv")
            self.anim.bind(on_complete=finish_callback)
            self.anim.start(instance)
            self.event = Clock.schedule_interval(self.my_callback, 1)
    def my_callback(self,instance):
        HelloKivy.l1.text = str(HelloKivy.mins)+":"+str(HelloKivy.count)
        HelloKivy.count -= 1
        if HelloKivy.mins == 0:
            self.event.cancel()
            #self.popup.close()
            HelloKivy.l1.text = "time up"
            HelloKivy.count = 60
            HelloKivy.mins = 45
        if HelloKivy.count == 0:
            HelloKivy.mins -= 1
            HelloKivy.count = 60
    def on_text(self,instance,value):
        print(instance.text,"value",value)
        conna = sqlite3.connect('test.db')
        conn = conna.cursor()
        try:
            conn.execute('''CREATE TABLE TIMELOG
             (ID INT PRIMARY KEY     NOT NULL,
             NAME           TEXT    NOT NULL,
             DURATION            INT     NOT NULL)''')
        except:
            pass
        conn.execute("INSERT INTO TIMELOG (ID,NAME,DURATION) \
      VALUES (100, 'PYTHON',45)");
        #conn.save()
        conna.commit()
        conna.close()
    def get_data(self,instance):
        df = pd.read_csv('logs.csv',index_col=0)
        self.data.text  = str(df.iloc[len(df)-3:len(df)]['time_end'])
        d = {}
        df['time_end'] = pd.to_datetime(df.time_end)
        df1 = df.loc[df['time_end'].dt.day==(datetime.datetime.now()).day]
        for el in df.loc[df['time_end'].dt.day==(datetime.datetime.now()).day]['subject']:
            if el not in d:
                d[el] = df1.loc[df1.subject == el]['duration'].sum()
        plt.figure(1)
        plt.bar(d.keys(),d.values())
        plt.ylabel('duration in minutes for the current day')
        plt.figure(2)
        temp = df.loc[df['time_end'].dt.day==(datetime.datetime.now()).day]['time_end'].dt.time
        temp = [x.strftime("%H : %M") for x in temp]
        plt.scatter(df.loc[df['time_end'].dt.day==(datetime.datetime.now()).day]['subject'],temp)
        plt.ylabel('time_end for each session for the current day')
        plt.ylim((0,24))
        plt.show()
    def clear_screen(self,instance):
        self.data.text = "your data"
    def minimize(self,instance):
        w = win32gui.FindWindow(None, "HelloKivy")
        win32gui.SetWindowPos(w,win32con.HWND_TOPMOST,0,0,200,200,0)
    def build(self):
        self.a = 0
        cnt = BoxLayout(orientation = 'vertical')
        #cnt = GridLayout()
        enter = Button(text='enter')
        self.data = Label(text = "Your Data",font_size = '27sp')
        #cnt.add_widget(self.data)
        cnt.add_widget(HelloKivy.l1)
        #l.bind(on_ref_press=callback)
        enter.bind(on_press = self.callback)
        cnt.add_widget(enter)
        self.txt1 = TextInput(text='Enter subject Here', multiline=False)
        cnt.add_widget(self.txt1)
        getData = Button(text='getData',size = (80,80))
        getData.bind(on_press = self.get_data)
        cnt.add_widget(getData)
        clear = Button(text="clear screen")
        clear.bind(on_press = self.clear_screen)
        #cnt.add_widget(clear)
        #self.popup = Popup(title='Test popup',
        #content=Label(text="pop pop 123"),
        #size_hint=(None, None), size=(150,150))
        #self.popup.open()
        Window.mimium_height = 150.
        Window.mimium_width = 150.
        Window.size = (300, 300)
        #Window.borderless = True
        #Window.minimize()
        #Window.grab_mouse()
        #Window.raise_window()
        #Window.allow_screensaver = True
        mini = Button(text = "minimize")
        mini.bind(on_press = self.minimize)
        cnt.add_widget(mini)
        return cnt

hk = HelloKivy()
hk.run()
