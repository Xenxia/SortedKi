from tkinter import *
from tkinter import ttk
from typing import Any
from func.ui import SCROLL_ALL, Custom_TitleBar_up, Tk_up, Toplevel_up, Treeview_up
from PIL import Image, ImageTk, ImageDraw
import json

root = Tk_up()
root.title('Codemy.com - TreeView')
# root.iconbitmap('c:/gui/codemy.ico')
root.overrideredirect(True)

root.geometry("500x900")
style = ttk.Style(root)

Custom_TitleBar_up(root)


title_bar = Frame(root, bg='black', relief='raised', bd=2)
close_button = Button(root, text='X', command=root.destroy)

old=[None, None]

def clic(event):
    old[0]=event.x
    old[1]=event.y

def glisser(event):
    # x, y = root.winfo_pointerxy()
    # root.geometry(f"+{x}+{y}")
    root.geometry(f"+{event.x_root-old[0]}+{event.y_root-old[1]}")
    # old[0]=event.x
    # old[1]=event.y

title_bar.bind('<B1-Motion>', glisser)
title_bar.bind('<Button-1>', clic)

title_bar.pack(side='top', expand=1, fill=X)
close_button.pack(side=RIGHT)
style.theme_use("default")

# custom indicator images
im_open = Image.new('RGBA', (15, 15), '#00000000')
im_empty = Image.new('RGBA', (15, 15), '#00000000')
draw = ImageDraw.Draw(im_open)
draw.polygon([(0, 4), (14, 4), (7, 11)], fill='#00ff00', outline='black')
im_close= im_open.rotate(90)

img_open = ImageTk.PhotoImage(im_open, name='img_open', master=root)
img_close = ImageTk.PhotoImage(im_close, name='img_close', master=root)
img_empty = ImageTk.PhotoImage(im_empty, name='img_empty', master=root)

# custom indicator
style.element_create('Treeitem.myindicator',
                     'image', 'img_close', ('user1', '!user2', 'img_open'), ('user2', 'img_empty'),
                     sticky='w', width=15)


# replace Treeitem.indicator by custom one
style.layout('Treeview.Item',
[('Treeitem.padding',
  {'sticky': 'nswe',
   'children': [('Treeitem.myindicator', {'side': 'left', 'sticky': ''}),
    ('Treeitem.image', {'side': 'left', 'sticky': ''}),
    ('Treeitem.focus',
     {'side': 'left',
      'sticky': '',
      'children': [('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})]
)

# Add some style
#Pick a theme
# style = ttk.Style()

# style.theme_use("default")
# Configure our treeview colors

style.configure("Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3",
    indent=10,
)
# Change selected color
style.map('Treeview', 
    background=[('selected', '#555555')])

# Create Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

def handle_click(event):
    if my_tree.identify_region(event.x, event.y) == "separator":
        return "break"

# Create Treeview
my_tree = Treeview_up(tree_frame, scroll=SCROLL_ALL, iid=True, child=True, show="tree headings", height=300, width=500)
# my_tree.bind('<Button-1>', handle_click)
# Pack to the screen
my_tree.pack()

# Define Our Columns

# Formate Our Columns
# my_tree.column("#0", width=100, anchor=W, stretch=NO)
# my_tree.column("Name", anchor=W, width=140)
# my_tree.column("ID", anchor=CENTER, width=100)
# my_tree.column("Favorite Pizza", anchor=W, width=140)

# Create Headings 
# my_tree.heading("#0", text="", anchor=W)
# my_tree.heading("Name", text="Name", anchor=W)
# my_tree.heading("ID", text="ID", anchor=CENTER)
# my_tree.heading("Favorite Pizza", text="Favorite Pizza", anchor=W)

# Add Data
# data = [
#     ["John", 1, "Pepperoni"],
#     ["Mary", 2, "Cheese"],
# ]

data = {
    "1": {
        "parent": None,
        "values": ["John", 1, "Pepperoni"]
    },
    "2": {
        "parent": "1",
        "values": ["Mary", 2, "Cheese"]
    },
    "3": {
        "parent": None,
        "values": ["Mary", 3, "Cheese"]
    },
    "4": {
        "parent": None,
        "values": ["Mary", 4, "Cheese"]
    },
    "5": {
        "parent": "3",
        "values": ["Mary", 5, "Cheese"]
    },
    "6": {
        "parent": "5",
        "values": ["Mary", 6, "Cheese"]
    },
}
my_tree.setColumns(["Name", "ID", "Favorite Pizza"], [100, 100, 100])
print(my_tree.addElements(data))
print(my_tree.addElement(iid="5", values=["Mary", 40, "Cheese"]))

# Create striped row tags

# global count
# count=0

# for record in data:
#     my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]))
#     count += 1

# my_tree.insert(parent="0", index='end', iid=99, text="", values=("test1", "test", "test"), tags=('evenrow',))
# my_tree.insert(parent="0", index='end', iid="test", text="", values=("test2", "test", "test"), tags=('evenrow',))
# my_tree.insert(parent="0", index='end', iid=97, text="", values=("test3", "test", "test"), tags=('evenrow',))
# my_tree.insert(parent="97", index='end', iid=90, text="", values=("test4", "test", "test"), tags=('evenrow',))

'''
my_tree.insert(parent='', index='end', iid=0, text="", values=("John", 1, "Peperroni"))
my_tree.insert(parent='', index='end', iid=1, text="", values=("Mary", "2", "Cheese"))
my_tree.insert(parent='', index='end', iid=2, text="", values=("Tina", "3", "Ham"))
my_tree.insert(parent='', index='end', iid=3, text="", values=("Bob", "4", "Supreme"))
my_tree.insert(parent='', index='end', iid=4, text="", values=("Erin", "5", "Cheese"))
my_tree.insert(parent='', index='end', iid=5, text="", values=("Wes", "6", "Onion"))
'''
# add child
#my_tree.insert(parent='', index='end', iid=6, text="Child", values=("Steve", "1.2", "Peppers"))
#my_tree.move('6', '0', '0')

add_frame = Frame(root)
add_frame.pack(pady=20)

windows2 = Toplevel_up(root)
windows2.title("New Window")

# sets the geometry of toplevel
windows2.geometry("500x100")

windows2.hide()






#Labels
nl = Label(windows2, text="Name")
nl.grid(row=0, column=0)

il = Label(windows2, text="ID")
il.grid(row=0, column=1)

tl = Label(windows2, text="Topping")
tl.grid(row=0, column=2)

#Entry boxes
name_box = Entry(windows2)
name_box.grid(row=1, column=0)

id_box = Entry(windows2)
id_box.grid(row=1, column=1)

topping_box = Entry(windows2)
topping_box.grid(row=1, column=2)

add = Button(windows2, text="add")
add.grid(row=2, column=0)



child: dict

def showwindows2(title, command):
    windows2.title(title)

    add.config(command=command)

    windows2.show()


# Add Record
def add_record():

    print(my_tree.addElement(values=[name_box.get(), id_box.get(), topping_box.get()]))

    # Clear the boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    windows2.hide()

# Remove all records
def remove_all():
    for record in my_tree.get_children():
        my_tree.delete(record)

# Remove one selected
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)

# Remove many selected
def remove_many():
    x = my_tree.selection()
    for record in x:
        my_tree.delete(record)

# Select Record
def select_record():
    # Clear entry boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    # Grab record number

    values = my_tree.getSelectedElement()

    #temp_label.config(text=values[0])

    print(values)

    # output to entry boxes
    # name_box.insert(0, valuest)
    name_box.insert(0, values[0])
    id_box.insert(0, values[1])
    topping_box.insert(0, values[2])


# Save updated record
def update_record():
    # Save new data
    my_tree.editSelectedElement(text=name_box.get(), values=(id_box.get(), topping_box.get()))

    # Clear entry boxes
    name_box.delete(0, END)
    id_box.delete(0, END)
    topping_box.delete(0, END)

    windows2.hide()

# Create Binding Click function
def clicker(e):
    select_record()

# Move Row up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Row Down
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

def get_child():
    dict = my_tree.getAllChildren()
    print(json.dumps(dict, indent=2))


# def get_sub_children(tree, item=""):
#     children = tree.get_children(item)
#     for child in children:
#         children += get_sub_children(tree, child)
#     return children

# def get_all_childs(tree: ttk.Treeview):

#     childs_list = get_sub_children(tree)
#     child_dict = {}

#     for iid in childs_list:

#         temp_dict = {}

#         item = tree.item(iid)

#         temp_dict["values"] = item["values"]
#         temp_dict["text"] = item["text"]
#         temp_dict["image"] = item["image"]
#         temp_dict["open"] = item["open"]
#         temp_dict["tags"] = item["tags"]
#         temp_dict["childs"] = None

#         parentIID = tree.parent(iid)

#         if parentIID != "":
#             temp_dict["childs"] = parentIID
        
#         child_dict[iid] = (temp_dict)

#     return child_dict

# child = get_all_childs(tree=my_tree)

#Buttons
move_up = Button(root, text="Move Up", command=my_tree.moveUpSelectedElement)
move_up.pack(pady=20)

move_down = Button(root, text="Move Down", command=my_tree.moveDownSelectedElement)
move_down.pack(pady=10)

select_button = Button(root, text="Select Record", command=select_record)
select_button.pack(pady=10)

update_button = Button(root, text="Edit Record", command=lambda: showwindows2("Edit record", update_record))
update_button.pack(pady=10)

addRecord = Button(root, text="Add Record", command=lambda: showwindows2("Add record", add_record))
addRecord.pack(pady=10)

# Remove all
removeall = Button(root, text="Remove All Records", command=my_tree.removeAllElement)
removeall.pack(pady=10)

# Remove One
removeone = Button(root, text="Remove One Selected", command=my_tree.removeSelectedElement)
removeone.pack(pady=10)

testWindows = Button(root, text="test", command=get_child)
testWindows.pack(pady=10)

temp_label = Label(root, text="")
temp_label.pack(pady=20)

# Bindings
# my_tree.bind("<Double-1>", clicker)
my_tree.bind("<ButtonRelease-1>", clicker)

# Custom_TitleBar_up(root)

root.update()
root.run()

#==============================================================================================

# from PIL import Image, ImageTk, ImageDraw
# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()

# style = ttk.Style(root)

# # custom indicator images
# im_open = Image.new('RGBA', (15, 15), '#00000000')
# im_empty = Image.new('RGBA', (15, 15), '#00000000')
# draw = ImageDraw.Draw(im_open)
# draw.polygon([(0, 0), (10, 10)], fill='#55ff55', outline='black')
# im_close= im_open.rotate(90)

# img_open = ImageTk.PhotoImage(im_open, name='img_open', master=root)
# img_close = ImageTk.PhotoImage(im_close, name='img_close', master=root)
# img_empty = ImageTk.PhotoImage(im_empty, name='img_empty', master=root)

# # custom indicator
# style.element_create('Treeitem.myindicator',
#                      'image', 'img_close', ('user1', '!user2', 'img_open'), ('user2', 'img_empty'),
#                      sticky='w', width=15)
# # replace Treeitem.indicator by custom one
# style.layout('Treeview.Item',
# [('Treeitem.padding',
#   {'sticky': 'nswe',
#    'children': [('Treeitem.myindicator', {'side': 'left', 'sticky': ''}),
#     ('Treeitem.image', {'side': 'left', 'sticky': ''}),
#     ('Treeitem.focus',
#      {'side': 'left',
#       'sticky': '',
#       'children': [('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})]
# )


# tree = ttk.Treeview(root)
# tree.pack()
# tree.insert('', 'end', text='item 1', open=True)
# tree.insert('', 'end', text='item 2')
# tree.insert('I001', 'end', text='item 11', open=False)
# tree.insert('I001', 'end', text='item 12', open=False)
# tree.insert('I004', 'end', text='item 121', open=False)

# root.mainloop()