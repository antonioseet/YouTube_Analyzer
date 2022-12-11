# pip install customtkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
import DatabaseConnection as dbc

def topKResults():
    count = 1
    topKResultsBox.delete(0,END)
    for item in dbc.getTopKResults(kEntryBox.get(),comboBox.current()):
        topKResultsBox.insert(count, str(count) + ') ' + item)
        count = count + 1

def frequencyResult():
    freqResultsBox.delete(0,END)

    #separate the view count
    viewCounts = viewEntryBox.get()

    if viewCounts:
        viewCountsList = viewCounts.split()
        minViewCount = int(viewCountsList[0])
        maxViewCount = int(viewCountsList[1])
    else:
        minViewCount = 0
        maxViewCount = 0

    #separate the length
    lengthCounts = lengthEntryBox.get()

    if lengthCounts:
        lengthCountsList = lengthCounts.split()
        minLength = int(lengthCountsList[0])
        maxLength = int(lengthCountsList[1])
        minRate = int(lengthCountsList[2])
        maxRate = int(lengthCountsList[3])
        if maxRate == 0:
            maxRate = 5
    else:
        minLength = 0
        maxLength = 0
        minRate = 0
        maxRate = 5

    categoryStr = comboBox2.get()

    count = dbc.getFrequencyResults(minViewCount, maxViewCount, minLength, maxLength, minRate, maxRate, categoryStr)
    freqResultsBox.insert(1, count)

def videoResults():
    rb.delete(0,END)

    viewCounts = ve.get()
    if viewCounts:
        viewCountsList = viewCounts.split()
        minViewCount = int(viewCountsList[0])
        maxViewCount = int(viewCountsList[1])
    else:
        minViewCount = 0
        maxViewCount = 0

    #separate the length
    lengthCounts = eb.get()
    if lengthCounts:
        lengthCountsList = lengthCounts.split()
        minLength = int(lengthCountsList[0])
        maxLength = int(lengthCountsList[1])
        minRate = int(lengthCountsList[2])
        maxRate = int(lengthCountsList[3])
        if maxRate == 0:
            maxRate = 5
    else:
        minLength = 0
        maxLength = 0
        minRate = 0
        maxRate = 5

    categoryStr = cb.get()

    res = dbc.getVideoResults(minViewCount, maxViewCount, minLength, maxLength, minRate, maxRate, categoryStr)

    count = 1
    for item in res:
        rb.insert(count, str(count) + ') ' + item)
        count = count + 1

width = 1000
height = 900
geoString = str(width)+"x"+str(height)

root = Tk()
root.title = "CPTS 415 - Big Data"
root.geometry(geoString)

notebook = ttk.Notebook(root)
notebook.pack()

################################################### FRAME 1 ##########################################
frame1 = Frame(master=notebook, width=width, height=height, bg="gray")
frame1.pack(fill="both", expand=1)

topKLabel = Label(frame1, text="Enter Top K integer below:", bg="gray")
topKLabel.place(relx=0.01, rely=0.02, anchor=tk.NW)

kEntryBox = Entry(frame1)
kEntryBox.place(relx=0.01, rely=0.05, anchor=tk.NW)

optionLabl = Label(frame1, text="Choose an option:", bg="gray")
optionLabl.place(relx=0.01, rely=0.08, anchor=tk.NW)

items = ['Top Categories', 'Most popular (Views)', 'Top Rated']
comboBox = ttk.Combobox(frame1, values=items)
comboBox.place(relx=0.01, rely=0.11, anchor=tk.NW)

searchButton = Button(frame1, text="Search", command=topKResults)
searchButton.place(relx=0.01, rely=0.14, anchor=tk.NW)

topKResultsBox = Listbox(frame1, width=100, height=25)
topKResultsBox.place(relx=0.01, rely=0.17, anchor=tk.NW)

notebook.add(frame1, text="Top K Queries")

############################### FRAME 2 #############################################

frame2 = Frame(notebook, width=width, height=height, bg="gray")
frame2.pack(fill="both", expand=1)


label1 = Label(frame2, text="Enter numbers in the form x y: x = min View count; y = max view count", bg="gray")
label1.place(relx=0.01, rely=0.02, anchor=tk.NW)

viewEntryBox = Entry(frame2)
viewEntryBox.place(relx=0.01, rely=0.05, anchor=tk.NW)

label1 = Label(frame2, text="Enter numbers in the form w x y z: w = minLength, x = maxLength, y = min rating, z = max rating", bg="gray")
label1.place(relx=0.01, rely=0.08, anchor=tk.NW)

lengthEntryBox = Entry(frame2)
lengthEntryBox.place(relx=0.01, rely=0.11, anchor=tk.NW)

viewLabel = Label(frame2, text="Choose a category to search:", bg="gray")
viewLabel.place(relx=0.01, rely=0.14, anchor=tk.NW)

items = dbc.getCategoriesList()
comboBox2 = ttk.Combobox(frame2, values=items)
comboBox2.place(relx=0.01, rely=0.17, anchor=tk.NW)

searchButton2 = Button(frame2, text="Search", command=frequencyResult)
searchButton2.place(relx=0.01, rely=0.2, anchor=tk.NW)

freqResultsBox = Listbox(frame2, width=20, height=1, bg='gray')
freqResultsBox.place(relx=0.01, rely=0.23, anchor=tk.NW)
notebook.add(frame2, text="Categorization")

##################################### FRAME 3 ##########################################

frame3 = Frame(notebook, width=width, height=height, bg="gray")
frame3.pack(fill="both", expand=1)


label2 = Label(frame3, text="Enter numbers in the form x y: x = min View count; y = max view count", bg="gray")
label2.place(relx=0.01, rely=0.02, anchor=tk.NW)

ve = Entry(frame3)
ve.place(relx=0.01, rely=0.05, anchor=tk.NW)

l = Label(frame3, text="Enter numbers in the form w x y z: w = minLength, x = maxLength, y = min rating, z = max rating", bg="gray")
l.place(relx=0.01, rely=0.08, anchor=tk.NW)

eb = Entry(frame3)
eb.place(relx=0.01, rely=0.11, anchor=tk.NW)

cl = Label(frame3, text="Choose a category to search:", bg="gray")
cl.place(relx=0.01, rely=0.14, anchor=tk.NW)

cats = dbc.getCategoriesList()
cb = ttk.Combobox(frame3, values=cats)
cb.place(relx=0.01, rely=0.17, anchor=tk.NW)

sb = Button(frame3, text="Search", command=videoResults)
sb.place(relx=0.01, rely=0.2, anchor=tk.NW)

rb = Listbox(frame3, width=100, height=25)
rb.place(relx=0.01, rely=0.23, anchor=tk.NW)
notebook.add(frame3, text="Range Q")

root.mainloop()
