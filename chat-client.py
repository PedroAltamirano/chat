import socket
import threading
import tkinter
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  server.connect(('192.168.0.19', 4000))
except:
  print('Server unavailable')
  sys.exit()

print("Connected to host: 192.168.0.19")
name = str(input('Type your user name: '))
server.send(name.encode())

def send(event=None):
  while True:
    #msg = str(input('Me > ')) #get from terminal
    msg = my_msg.get()
    my_msg.set('')
    server.send(msg.encode())
    if msg == '[bye]':
      server.close()
      break

def receive():
  while True:
    message = server.recv(1024)
    #print('\n'+message.decode()) #print on terminal
    msg_list.insert(tkinter.END, message)

def on_closing(event=None):
  my_msg.set("[bye]")
  send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

thread_receive = threading.Thread(target = receive).start()
tkinter.mainloop()