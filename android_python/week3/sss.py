import tkinter as tk

def create_window():
    window = tk.Toplevel(root)
    T = tk.Text(window, height=5, width=25, state="normal")
    T.configure(font="tkFixedFont")
    T.insert(tk.END, "asd")
    T.configure(state='disabled')
    T.pack()

root = tk.Tk()
b = tk.Button(root, text="Create new window", command=create_window)
b.pack()

root.mainloop()
