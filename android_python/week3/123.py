from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import random
import time
import logging
import queue
import datetime
import threading
import pickle
import os

# define the logger 
logger = logging.getLogger(__name__)
# define the mainframe
master = Tk()
# define and initialize the timer
clock = StringVar()
clock.set("Time: 00:00")

# define the timer class
class Time:
    def __init__(self):
        self.stop_event = threading.Event()

    def start(self):
        self.start_time = datetime.datetime.now()
        while not self.stop_event.is_set():
            now = datetime.datetime.now()
            time_int = now - self.start_time
            #clock.set(now.strftime("%H:%M:%S"))
            clock.set("Time: {:02d}:{:02d}".format(time_int.seconds//60, time_int.seconds))
            time.sleep(0.1)

    def stop(self):
        self.stop_event.set()

    def clear(self):
        self.stop_event.clear()

# queuehandler for logging, response for the emission of the text
class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, text):
        self.log_queue.put(text)

class Log:
    def __init__(self, frame):
        self.frame = frame
        self.scrolled_text = ScrolledText(frame, state="disabled", height=23)
        # sticky -> what to do if the cell is larger than widget
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font="TkFixedFont")
        # queue -> logging handler
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        logger.addHandler(self.queue_handler)
        # msg --> formatted_msg
        formatter = logging.Formatter(fmt='%(asctime)s: %(message)s', datefmt="%H:%M:%S")
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
    # check queue constantly
    def check_queue(self):
        while True:
            try:
                text = self.log_queue.get(block=False) # block=False --> don't wait for items
            except queue.Empty:
                break
            else:
                self.push(text) # push the text to the frame if the queue was not empty
        # check queue under 100ms frequency(human reaction 200~250ms)
        self.frame.after(100, self.check_queue)

class GuessingGame():
    def __init__(self, master):
        # get master frame from the argument
        self.master = master
        # set the size of the mainframe
        self.master.geometry("800x600")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.title("Number Guessing Game")
        # panes && frames
        # define and cut the mainframe into pieces
        vertical_pane = ttk.PanedWindow(self.master, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky='nsew')
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        input_frame = ttk.Labelframe(horizontal_pane, text="Input", height=75)
        input_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(input_frame, weight=1)
        time_frame = ttk.Labelframe(horizontal_pane, text="Time", width=100)
        time_frame.columnconfigure(0, weight=1)
        time_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(time_frame)
        log_frame = ttk.Labelframe(vertical_pane, text="Log")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        option_frame = ttk.Labelframe(vertical_pane, text="Options")
        option_frame.columnconfigure(2, weight=1)
        option_frame.rowconfigure(0, weight=1)
        vertical_pane.add(log_frame)
        vertical_pane.add(option_frame)
        ## labels
        # define positions and text for labels
        Label(time_frame, textvariable=clock).place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(input_frame, text="Guess a Number").place(relx=0.5, rely=0.1, anchor=CENTER)
        Label(input_frame, text="Name").place(relx=0.8, rely=0.1, anchor=CENTER)
        # input box
        # set the position of the entries
        self.name_entry = Entry(input_frame)
        self.name_entry.place(relx=0.8, rely=0.7, anchor=CENTER)
        self.input = Entry(input_frame)
        self.input.place(relx=0.5, rely=0.7, anchor=CENTER)
        # bind the return to the input for convenience
        self.input.bind("<Return>", lambda x: self.getinput(self.input))
        # buttons
        # set the attribution of the buttons(frames, text, command)
        self.show_button = Button(option_frame, text="Show Answer", command=lambda:self.show_answer())
        self.new_button = Button(option_frame, text="New Game", command=lambda:self.new_game())
        self.rank_button = Button(option_frame, text="Rank", command=lambda:self.show_rank())
        self.exit_button = Button(option_frame, text="Exit", command=lambda:self.exit())
        # set the position of the buttons
        self.show_button.place(relx=0.2, rely=0.5, anchor=CENTER)
        self.new_button.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.rank_button.place(relx=0.6, rely=0.5, anchor=CENTER)
        self.exit_button.place(relx=0.8, rely=0.5, anchor=CENTER)
        # frame
        # assign self.log to catch the instance of Log with log_frame as argument
        self.log = Log(log_frame)
        # start game
        # assign self.time to catch the instance of Time
        self.time = Time()
        self.new_game()
        # loading rank
        try:
            with open(".guess_rank.pkl", 'rb') as f:
                self.rank_list = pickle.load(f)
        # if the file doesn't exist, create a empty list
        except:
            self.rank_list = []
        # loop through the mainframe
        self.master.mainloop()

    def getinput(self, handler):
        # the timer starts when the first input occurs
        if self.first_input:
            threading.Thread(target=self.time.start, daemon=True).start()
            self.first_input = False
        value = handler.get()
        # clear the input entry
        handler.delete(0, 'end')
        # take action only when the input entry is not empty
        if value != '':
            # check if the input is valid
            ret_val = self.is_valid(value)
            # valid
            if ret_val == True:
                self.check_answer(value)
                self.count += 1
            # invalid
            else:
                # display error message
                logger.log(level=logging.INFO, msg=ret_val)
    # show answer function called by SHOW ANSWER BUTTON
    def show_answer(self):
        logger.log(level=logging.INFO, msg=f"The answer is {self.answer}")
    # function called at the beginning of the game or whenever the NEW GAME BUTTON is pressed
    def new_game(self):
        # reset the first_input
        self.first_input = True
        if not self.time.stop_event.is_set():
            self.time.stop()
            # sleep due to racing condition
            time.sleep(0.1)
        # reset the timer, counter and the duplicated number list
        clock.set("Time: 00:00")
        self.time.clear()
        self.count = 1
        self.duplicate_list = []
        # generate a new number for a new round
        self.generate_number()
        logger.log(level=logging.INFO, msg=f"-----Starting a new round-----")
    # low level function called by function `new game`
    def generate_number(self):
        ret = ''
        numbers = list('0123456789')
        for i in range(4):
            tmp = random.choice(numbers)
            ret += tmp
            numbers.pop(numbers.index(tmp))
        self.answer = ret
    # low level function called by function `input`
    def check_answer(self, value):
        a_cnt = b_cnt = 0
        for i in range(len(value)):
            # loop through the input to check how many of them is inside the answer
            b_cnt += self.answer.count(value[i])
            # check for the precision
            if self.answer[i] == value[i]:
                a_cnt += 1
        # get the final number of b's and a's
        b_cnt -= a_cnt
        # display round information
        logger.log(level=logging.INFO, msg=f"Round:{self.count} {value} {a_cnt}A{b_cnt}B")
        # congratulation message
        if a_cnt == 4:
            logger.log(level=logging.INFO, msg="You win!! Congratulations!!")
            # get time
            self.time.stop()
            elapsed = clock.get()[6:]
            logger.log(level=logging.INFO, msg=f"Time elapsed: {elapsed}")
            #seconds = int(elapsed[:2])*60 + int(elapsed[-2:])
            # get name player name for HALL OF FAME
            self.player_name = ''
            if len(self.rank_list) != 0:
                # check if the record is good enough to be on the hall of fame
                if not (self.count > self.rank_list[-1]["Rounds"] and elapsed > self.rank_list[-1]["Time"]) or len(self.rank_list <= 10):
                    self.player_name = self.name_entry.get()
                    self.name_entry.delete(0, 'end')
                    if self.player_name == '':
                        self.player_name = "Anonymous"
                    self.rank_list.append({"Name": self.player_name, "Rounds" : self.count, "Time" : elapsed})
            # if the rank_list is empty
            else:
                    self.player_name = self.name_entry.get()
                    self.name_entry.delete(0, 'end')
                    if self.player_name == '':
                        self.player_name = "Anonymous"
                    self.rank_list.append({"Name": self.player_name, "Rounds" : self.count, "Time" : elapsed})
            # sort the rank_list based on the rounds then the time
            self.rank_list = sorted(self.rank_list, key=lambda l: (l["Rounds"], l["Time"]))[:10]
        # lose if round count is 10
        if self.count == 10:
            logger.log(level=logging.INFO, msg=f"You lose!! Answer: {self.answer}")
            self.retry()
    # low level function called by function `input`
    def is_valid(self, value):
        # if the input is not numeric
        if not value.isnumeric():
            return "Invalid input!!(character error) Try again!!"
        # if the length of the input is not 4
        elif len(value) != 4:
            return "Invalid input!!(length error) Try again!!"
        # if the input got duplicated numers
        elif len(value) != len(set(value)):
            return "Invalid input!!(duplicate characters) Try again!!"
        # if the input has been guessed
        elif value in self.duplicate_list:
            return "Invalid input!!(duplicate answer) Try again!!"
        else:
            # valid
            self.duplicate_list.append(value)
            return True
    # to be add into the game, expectation --> pop a window for the player to input information if the record is good enough
    def get_player_name(self):
        window = Toplevel(self.master)
        window.title("Congrats")
        Label(window, text="Please enter your name").place(relx=.5, rely=.2, anchor=CENTER)
        user_in = Entry(window)
        user_in.place(relx=0.5, rely=0.7, anchor=CENTER)
        submit_but = Button(window, text="Submit", command=lambda:[self.get_player_name_return(user_in), window.destroy()])
        submit_but.place(relx=.5, rely=.9, anchor=CENTER)
    # same as the above
    def get_player_name_return(self, handler):
        name = handler.get()
        handler.delete(0, 'end') # clear
        if name != '':
            self.player_name = name
        else:
            self.player_name = "Anonymous"
    # function called by SHOW RANK BUTTON
    def show_rank(self):
        window = Toplevel(self.master)
        window.title("Hall of Fame")
        T = Text(window, width=40, height=30, font="tkFixedFont")
        for i in range(len(self.rank_list)):
            T.insert(END, f"Name: {self.rank_list[i]['Name']} | Rounds: {self.rank_list[i]['Rounds']} | Time: {self.rank_list[i]['Time']}\n")
        T.configure(state='disabled')
        T.pack()
    # retry window
    def retry(self):
        window = Toplevel(self.master)
        window.title("Retry")
        new_game_but = Button(window, width=10, height=5, text="New Game", command=lambda:[self.new_game(), window.destroy()])
        exit_but = Button(window, width=10, height=5, text="Exit", command=lambda:self.exit())
        new_game_but.place(relx=0.5, rely=0.25, anchor=CENTER)
        exit_but.place(relx=0.5, rely=0.75, anchor=CENTER)
    # save the rank_list
    def save_data(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    # exit function
    def exit(self):
        # save the rank list when exiting
        self.save_data(self.rank_list, ".guess_rank.pkl")
        self.master.destroy()

if __name__ == "__main__":
    # set the logging level to INFO
    logging.basicConfig(level=logging.INFO)
    # throw the mainframe into the GuessingGame class to start the game
    # Since some of the classes such as timer is not include in the GuessGame class
    # it's much more convenient to define the main frame outside of the class
    GuessingGame(master)
