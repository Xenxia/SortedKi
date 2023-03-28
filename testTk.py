from tk_up.widgets import Tk_up, Frame_alphaBg_up
from tkinter import BOTH, NW, YES, Button, Canvas, Label
from PIL import Image, ImageColor, ImageTk



root = Tk_up()


f = Frame_alphaBg_up(root, color="#FF00FF", alpha=0.5)
f.packPosSize().show()
# images = []
# def create_rectangle(x1, y1, x2, y2, **kwargs):
#     if 'alpha' in kwargs:
#         alpha = int(kwargs.pop('alpha') * 255)
#         fill = kwargs.pop('fill')
#         fill = ImageColor.getcolor(fill, "RGB") + (alpha,)
#         print(fill)
#         image = Image.new('RGBA', (x2-x1, y2-y1), fill)
#         images = ImageTk.PhotoImage(image)
#         canvas.create_image(x1, y1, image=images, anchor='nw')
#     # canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

# canvas = Canvas(master=root, width=300, height=200)
# canvas.pack()
# label = Label(canvas, text='ABC')
# canvas.create_window(100,220, window=label)
# # create_rectangle(10, 10, 200, 100, fill='blue')
# create_rectangle(50, 50, 250, 150, fill='#00FF00', alpha=.5)
# create_rectangle(80, 80, 150, 120, fill='#FF00FF', alpha=.8)


root.run()