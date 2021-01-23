import tkinter

# create main frame
top = tkinter.Tk()

# displaying frame built on top of `top`
f1 = tkinter.Frame(top)
# key frame built on top of `top`
f2 = tkinter.Frame(top)
# define the variable to be showed on the displaying frame
var = tkinter.StringVar()
# initializing
var.set("0")

# define a function to update the displaying value
def SetValue():
    Screen = tkinter.Label(f1, textvariable = var, width=20, height=5).grid(row = 0, column = 1)
# define a function to catch clicking signals
def Click(x):
    string = var.get()
    # beautifying what would by showed on the displaying frame
    if string != "0":
        if string[-1] in "+-x/" or (string[-1] in "0123456789" and x in "+-x/"):
            string += " "
            if len(string) > 3:
                if string[-3] in "+-x/" and string[-1] == '-':
                    string.pop(-1)
        string += x
    else:
        string = x
    var.set(string)
    SetValue()
# define a function to reset the value
def Clear():
    var.set("0")
    SetValue()
# define a function to calcuate the value
def Calculate():
    llist = "".join(var.get().split())
    #print(llist)
    result = 0
    operator = ""
    try:
        # use the built-in function `eval` would ease all the pain coding the rules yourself
        # since the multiplying sign in the programming is different from the one used in the function
        # thus we have to replace the sign from `x` to `*`
        result = eval(llist.replace('x', "*"))
    # raise error if encouter error(divided by zero)
    except ZeroDivisionError:
        result = "error"
    #for i in range(0, len(llist)):
    #    if llist[i].strip("-").isnumeric():
    #        if operator != "":
    #            result = operate(operator, llist[i], result)
    #            if result == "error":
    #                break
    #        else:
    #            result = llist[i]
    #    else:
    #        operator = llist[i]
    var.set(result)
    SetValue()
# translate the signs from string to numerical definition
def operate(sign, value, result):
    value = int(value)
    result = int(result)
    if sign == "+":
        result += value
    elif sign == "-":
        result -= value
    elif sign == "x":
        result *= value
    elif sign == "/":
        if value == 0:
            return "error"
        else:
            result /= value
    return result

SetValue()
# allocating the location, defining the size and linking the command when pressed for the buttons
# link : numeric --> Click(), btnClear --> Clear(), btnEqual --> Calculate(), operator --> Click()
btn7 = tkinter.Button(f2,text = "7",borderwidth = 5,width = 5,height = 5, command = lambda : Click("7")).grid(row = 0,column = 0)
btn8 = tkinter.Button(f2,text = "8",borderwidth = 5,width = 5,height = 5, command = lambda : Click("8")).grid(row = 0,column= 1)
btn9 = tkinter.Button(f2,text = "9",borderwidth = 5,width = 5,height = 5, command = lambda : Click("9")).grid(row = 0,column= 2)
btnPlus = tkinter.Button(f2,text = "+",borderwidth = 5,width = 5,height = 5, command = lambda : Click("+")).grid(row = 0,column= 3)
btn4 = tkinter.Button(f2,text = "4",borderwidth = 5,width = 5,height = 5, command = lambda : Click("4")).grid(row = 1,column= 0)
btn5 = tkinter.Button(f2,text = "5",borderwidth = 5,width = 5,height = 5, command = lambda : Click("5")).grid(row = 1,column= 1)
btn6 = tkinter.Button(f2,text = "6",borderwidth = 5,width = 5,height = 5, command = lambda : Click("6")).grid(row = 1,column= 2)
btnMinus = tkinter.Button(f2,text = "-",borderwidth = 5,width = 5,height = 5, command = lambda : Click("-")).grid(row = 1,column= 3)
btn1 = tkinter.Button(f2,text = "1",borderwidth = 5,width = 5,height = 5, command = lambda : Click("1")).grid(row = 2,column= 0)
btn2 = tkinter.Button(f2,text = "2",borderwidth = 5,width = 5,height = 5, command = lambda : Click("2")).grid(row = 2,column= 1)
btn3 = tkinter.Button(f2,text = "3",borderwidth = 5,width = 5,height = 5, command = lambda : Click("3")).grid(row = 2,column= 2)
btnX = tkinter.Button(f2,text = "x",borderwidth = 5,width = 5,height = 5, command = lambda : Click("x")).grid(row = 2,column= 3)
btn0 = tkinter.Button(f2,text = "0",borderwidth = 5,width = 5,height = 5, command = lambda : Click("0")).grid(row = 3,column= 0)
btnClear = tkinter.Button(f2,text = "C",borderwidth = 5,width = 5,height = 5, command = lambda : Clear()).grid(row = 3,column= 1)
btnEqual = tkinter.Button(f2,text = "=",borderwidth = 5,width = 5,height = 5, command = lambda : Calculate()).grid(row = 3,column= 2)
btnDiv = tkinter.Button(f2,text = "/",borderwidth = 5,width = 5,height = 5, command = lambda : Click("/")).grid(row = 3,column= 3)
# showing both of the frames established on the main frame
f1.pack()
f2.pack()
# loop the main frame until terminated by user --> could add a listener for signals such as ctrl^c or esc to exit the program smoothly
top.mainloop()
