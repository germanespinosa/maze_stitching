from tkinter import *
from PIL import ImageTk
from util import Camera

camera = Camera((800, 800))
camera.load_image(0, "camera_0.png")
camera.load_image(1, "camera_1.png")
camera.load_image(2, "camera_2.png")
camera.load_image(3, "camera_3.png")
camera.draw_all()

cell_coordinates = (0,0)
change = (0,0)
trust = 1

def update_picture():
    global picture #
    camera.draw_all()
    picture = ImageTk.PhotoImage(camera.background)
    canvas.itemconfigure(canvas_image, image=picture)

def callback(event):
    global cell_coordinates
    cell_coordinates_x, cell_coordinates_y = cell_coordinates
    print("coord: ", cell_coordinates_x, cell_coordinates_y)
    c, centroid_x,  centroid_y = camera.get_cxy((event.x,event.y))
    if camera.exists(c, cell_coordinates):
        print("coordinates (" + cell_coordinates_x + "," + cell_coordinates_y + ") already associated for this camera")
        if input("replace(y/N)? ") != "y":
            return
    a =camera.association((centroid_x,centroid_y),cell_coordinates,trust)
    camera.add_association(c,a)
    update_picture()
    change_x, change_y = change
    cell_coordinates = (cell_coordinates_x + change_x, cell_coordinates_y + change_y)
    print("new coordinate: ",cell_coordinates_x,",",cell_coordinates_y)


def callback2(event):
    global cell_coordinates
    global change
    cell_coordinates_x = int(input("x initial value:"))
    change_x = int(input("x step change:"))
    cell_coordinates_y = int(input("y initial value:"))
    change_y = int(input("y step change:"))
    cell_coordinates = (cell_coordinates_x, cell_coordinates_y)
    change = (change_x, change_y)
    print("new coordinate: ",cell_coordinates_x,",",cell_coordinates_y)


def finish(e):
    exit()

def save(e):
    print("save")
    camera.save()

def change_trust(e):
    global trust
    trust = 0 if trust == 1 else 1
    print ("trust:", trust)

def remove_last(e):
    camera.remove_last()
    update_picture()

main = Tk()
canvas = Canvas(main, width=camera.window_size[0], height=camera.window_size[1])
canvas.pack()
picture = ImageTk.PhotoImage(camera.background)
canvas_image = canvas.create_image((0,0),image=picture, anchor="nw")

canvas.bind("<Button-1>", callback)
canvas.bind_all("<p>", callback2)
canvas.bind_all('<q>', finish)
canvas.bind_all('<s>', save)
canvas.bind_all('<t>', change_trust)
canvas.bind_all('<r>', remove_last)
main.mainloop()