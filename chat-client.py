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
  #msg = str(input('Me > ')) #get from terminal
  msg = my_msg.get()
  my_msg.set('')
  server.send(msg.encode())
  msg_list.insert(tkinter.END, 'Me > '+msg)

def receive():
  while True:
    try:
      message = server.recv(1024)
      #print('\n'+message.decode()) #print on terminal
      if message.decode() == '[bye]':
        server.close()
        top.quit()
        sys.exit()
    except OSError:
      break

def on_closing(event=None):
  my_msg.set("[bye]")
  send()

top = tkinter.Tk()
top.title("Yachay Chatroom")
messages_frame = tkinter.Frame(top)

scrollbar = tkinter.Scrollbar(messages_frame)

#incomming messages box
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_frame.pack()

#message to send box and rturn event
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.TRUE)

#send button
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack(side=tkinter.RIGHT)


top.protocol("WM_DELETE_WINDOW", on_closing)

thread_receive = threading.Thread(target = receive).start()

tkinter.mainloop()