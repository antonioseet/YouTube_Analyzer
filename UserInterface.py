# pip install customtkinter
import tkinter as tk
from tkinter import *
from tkinter import ttk
import DatabaseConnection as dbc

def topKResults():
    count = 1
    for item in dbc.getTopKResults(kEntryBox.get(),comboBox.current()):
        topKResultsBox.insert(count, item)
        count = count + 1

width = 1000
height = 1000
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
topKLabel.grid(row=0, column=0, padx=5, pady=5)

kEntryBox = Entry(frame1)
kEntryBox.grid(row=1, column=0, padx=5, pady=5)

optionLabl = Label(frame1, text="Choose an option:", bg="gray")
optionLabl.grid(row=2, column=0, padx=5, pady=5)

items = ['Top Categories', 'Most popular (Views)', 'Top Rated']
comboBox = ttk.Combobox(frame1, values=items)
comboBox.grid(row=3, column=0, padx=5, pady=5)

searchButton = Button(frame1, text="Search", command=topKResults)
searchButton.grid(row=4, column=0, padx=5, pady=5)

topKResultsBox = Listbox(frame1)

topKResultsBox.grid(padx=50, pady=30)

notebook.add(frame1, text="Top K Queries")

####################################################################################################

frame2 = Frame(notebook, width=width, height=height, bg="gray")
frame2.pack(fill="both", expand=1)
notebook.add(frame2, text="Second Tab")

root.mainloop()
