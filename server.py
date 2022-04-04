import socket
from tkinter import Tk, Label, Button, Frame, Entry, messagebox
from PIL import ImageTk, Image
import threading

def change_image(image_name):
    return

def send_values():
    try:
        dir_val = int(angle.get())
    except:
        messagebox.showerror("Error", "Data typed in angle is invalid, write an integer please.")
        return

    angle_val = direction.get()

    conn.send((str(dir_val)+"*#@"+str(angle_val)).encode("UTF-8"))

def gui():
    global root
    root = Tk()
    root.geometry("600x500")
    root.resizable(False, False)
    image_name = "no_photo.jpg"
    global text
    text = Label(text="Image name: " + image_name)
    global frame
    frame = Frame(root, width=100, height=100)
    frameB = Frame(root)
    global temp
    temp = Label(master=frameB, text="Temperature: No Data")
    global yaw
    yaw = Label(master=frameB, text="yaw: No Data")
    global angle
    angle = Entry(master=frameB)
    global direction
    direction = Entry(master=frameB)
    submit = Button(master=frameB, text="Submit", command=send_values)
    text.pack()
    frame.pack()
    temp.pack()
    yaw.pack()
    Label(master=frameB, text="Angle:").pack()
    angle.pack()
    Label(master=frameB, text="Direction:").pack()
    direction.pack()
    submit.pack()
    frameB.pack()
    frame.place(anchor='center', relx=0.5, rely=0.35)
    frameB.place(anchor='center', relx=0.5, rely=0.8)

    # Create an object of tkinter ImageTk
    img = Image.open(image_name)
    img = img.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    # Create a Label Widget to display the text or Image
    label = Label(frame, image=img)
    label.pack()
    root.mainloop()

HOST = "0.0.0.0"
PORT = 6969

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Starting server...")
global conn
conn, addr = s.accept()
print("connection accepted")

t1 = threading.Thread(target=gui)
t1.start()

temp_num = ""
yaw_num = ""

while True:
    data = conn.recv(1024).decode("UTF-8")
    if not data:
        break
    print(data)

    splited = data.split("*#@")

    if splited[0] == "1":
        image_name = splited[1]
        size = int(splited[2])
        curr_size = 0
        file = b""
        conn.send("ok".encode("UTF-8"))
        while curr_size < size:
            data = conn.recv(size)
            file += data
            curr_size += data.__sizeof__()
        with open(image_name, "wb+") as file:
            file.write(data)

        text.destroy()
        frame.destroy()

        text = Label(text="Image name: " + image_name)

        frame = Frame(root, width=100, height=100)
        text.pack()
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.35)

        # Create an object of tkinter ImageTk
        img = Image.open(image_name)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        # Create a Label Widget to display the text or Image
        label = Label(frame, image=img)
        label.pack()

    if splited[0] == "2":
        temp_num = splited[1]
        temp.config(text="Temperature: " + temp_num)

    if splited[0] == "3":
        yaw_num = splited[1]
        yaw.config(text="yaw: " + yaw_num)