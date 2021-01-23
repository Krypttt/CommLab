from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import random
import time
import logging
import queue

logger = logging.getLogger(__name__)

class MainFrame:
    def __init__(self):
        self.master = Tk()
        self.master.geometry("800x600")
        self.master.title("Number Guessing Game")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # panes && frames
        vertical_pane = ttk.PanedWindow(self.master, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky=N+S+E+W)
        ## time_frame
        time_frame = ttk.Labelframe(vertical_pane, text="Time")
        vertical_pane.add(time_frame, weight=1)
        ## input_frame
        input_frame = ttk.Labelframe(vertical_pane, text="Input")
        input_frame.columnconfigure(0, weight=1)
        vertical_pane.add(input_frame, weight=1)
        ## log_frame
        log_frame = ttk.Labelframe(vertical_pane, text="Log")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        vertical_pane.add(log_frame, weight=1)
        ## option_frame
        option_frame = ttk.Labelframe(vertical_pane, text="Options")
        vertical_pane.add(option_frame, weight=1)

        # init all frames
        self.new_game()
        self.time = Time(time_frame)
        self.input = Input(input_frame)
        self.log = Log(log_frame)
        self.options = Options(option_frame, self.master)
        # labels
        #self.label_hint = Label(self.master, text="Welcome to the Number Guessing Game")
        #self.label_hint.place(relx=0.5, rely=0.1, anchor=CENTER)
        # frame
        #self.log_frame = Scrollbar(self.master, orient="horizontal", width=800)
        #self.log_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        #self.log_frame = Frame(self.master, bg="#ffffff", height=300, width=800)
        #self.log_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        # text inside the frame
        #self.text_log_frame = Text(self.log_frame, height=300, width=800)
        # start game
        ######
        self.master.mainloop()

    def new_game(self):
        self.count = 1
        self.duplicate_list = []
        self.generate_number()

    def generate_number(self):
        ret = ''
        numbers = list('0123456789')
        for i in range(4):
            tmp = random.choice(numbers)
            ret += tmp
            numbers.pop(numbers.index(tmp))

        self.answer = ret

    def getinput(self, handler):
        value = handler.get()
        handler.delete(0, 'end') # clear
        if value != '':
            ret_val = self.is_valid(value)
            if ret_val == True:
                self.check_answer(value)
                self.count += 1
            else:
                logger.log(ret_val)

    def check_answer(self, value):
        a_cnt = b_cnt = 0
        for i in range(len(value)):
            b_cnt += self.answer.count(value[i])
            if self.answer[i] == value[i]:
                a_cnt += 1
        b_cnt -= a_cnt
        congrats = "\nYou win!! Congratulations!!" if a_cnt == 4 else ""
        logger.log(f"Round:{self.count} {value} {a_cnt}A{b_cnt}B"+congrats)

    def is_valid(self, value):
        if not value.isnumeric:
            return "Invalid input!!(character error) Try again!!"
        elif len(value) != 4:
            return "Invalid input!!(length error) Try again!!"
        elif len(value) != len(set(value)):
            return "Invalid input!!(duplicate characters) Try again!!"
        elif value in self.duplicate_list:
            return "Invalid input!!(duplicate answer) Try again!!"
        else:
            self.duplicate_list.append(value)
            return True

    def show_answer(self):
        self.logger(f"The answer is {self.answer}")

    def exit(self):
        self.master.destroy()

    def logger(self, text):
        print(text)
        #self.text_log_frame.configure(state='normal')
        #self.text_log_frame.insert(END, text+"\n")
        #self.text_log_frame.configure(state='disabled')
        #self.text_log_frame.yview(END)
        #self.text_log_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        #self.text_log_frame.after(0, append)

class Time:
    def __init__(self, frame):
        self.frame = frame

class Input(MainFrame):
    def __init__(self, frame):
        self.frame = frame
        self.duplicate_list = MainFrame.duplicate_list
        # input box
        self.input = Entry(self.frame)
        self.input.grid(column=0, row=0, sticky=N+W+S+E)
        #self.input.place(relx=0.5, rely=0.15, anchor=CENTER)
        self.input.bind("<Return>", lambda x: self.getinput(self.input))

class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
    def emit(self, text):
        self.log_queue.put(text)

class Log:
    def __init__(self, frame):
        self.frame = frame

        self.scrolled_text = ScrolledText(frame, state="disabled", height=12)
        # sticky -> what to do if the cell is larger than widget
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font="TkFixedFont")
        # queue -> logging handler
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        logger.addHandler(self.queue_handler)
        # msg --> formatted_msg
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        # start checking queue
        self.frame.after(0, self.check_queue)

    def push(self, text):
        # pushing messages into the frame
        msg = self.queue_handler.format(text)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg+'\n')
        self.scrolled_text.configure(state='disabled')
        self.scrolled_text.yview(END)

    def check_queue(self):
        # check queue under 500ms frequency
        while True:
            try:
                text = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.push(text)
        self.frame.after(500, self.check_queue)

class Options(MainFrame):
    def __init__(self, frame, master):
        self.frame = frame
        self.master = master
        # buttons
        self.show_button = Button(self.frame, text="Show Answer", command=lambda:self.show_answer())
        self.new_button = Button(self.frame, text="New Game", command=lambda:self.new_game())
        self.exit_button = Button(self.frame, text="Exit", command=lambda:self.exit())
        self.show_button.grid(column=0, row=0, sticky=W)
        self.new_button.grid(column=1, row=0, sticky=W)
        self.exit_button.grid(column=2, row=0, sticky=W)

if __name__ == "__main__":
    MainFrame()
