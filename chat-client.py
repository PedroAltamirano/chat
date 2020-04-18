import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('192.168.0.19', 4000))
print("Connected to host: 192.168.0.19")
name = str(input('Type your user name: '))
server.send(name.encode())

def send():
  while True:
    msg = str(input('Me > '))
    server.send(msg.encode())

def receive():
  while True:
    message = server.recv(1024)
    print(message.decode())

thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()