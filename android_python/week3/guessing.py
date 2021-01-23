from tkinter.ttk import *
from tkinter import *
import tkinter
import random
import time
import threading


#class Game:
#    def __init__(self):
#        pass
#
#    def _generate_random_number():
#        ret = ''
#        numbers = list('0123456789')
#        for i in range(4):
#            tmp = random.choice(numbers)
#            ret += tmp
#            numbers.pop(numbers.index(tmp))
#        return ret
#
#    def _show_answer():
#        print(self.answer)
#
#    def _start():
#        #start timer
#        self.answer = self._generate_random_number()

def _run():
    value = guessString.get()

master = Tk()
master.geometry("800x600")
## log
#st = tkinter.scrolledtext.ScrolledText(master, width=600, height=300)
#st.grid(column=0, pady=10, padx=10)

## input
guessString = tkinter.StringVar()
guessEntry  = tkinter.Entry(master, width=20, textvariable=guessString)
guessEntry.place(relx=.5, rely=.1, anchor=CENTER)

## timer
def timer():
    cnt = 0
    while True:
        time.sleep(1)
        cnt += 1
        _min = cnt / 60
        _sec = cnt % 60
        time_str = "time : {}:{}".format(_min, _sec)
        time_label = Label(master, text=time_str)

##guess
def guess(event):
    value = guessString.get()
    if (value != ''):

    
master.bind('<Return>', guess)
time_label = Label(master, text="time : 0:00")
#welcome_label = Label(master, text="Welcome to the Number Guessing Game")
show_button = Button(master, text="Show Answer", command=lambda:_show_answer())
new_button = Button(master, text="New Game", command=lambda:_new_game())
exit_button = Button(master, text="Exit", command=lambda:exit())
#run_button = Button(master, text="RUN", command=lambda:_run())
time_label.place(relx=.5, rely=.04, anchor=CENTER)
#welcome_label.pack(pady=10)
show_button.place(bordermode=OUTSIDE, height=30, width=100, relx=0.2, rely=0.95, anchor=CENTER)
new_button.place(bordermode=OUTSIDE, height=30, width=90, relx=0.5, rely=0.95, anchor=CENTER)
exit_button.place(bordermode=OUTSIDE, height=30, width=60, relx=0.8, rely=0.95, anchor=CENTER)
#run_button.place(bordermode=OUTSIDE, height=35, width=60, relx=0.47, rely=0.9)

master.mainloop()
