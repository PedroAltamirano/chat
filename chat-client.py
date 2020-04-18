import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('192.168.0.19', 4000))
print("Connected to host: " + ip_address)

def send():
  while True:
    msg = raw_input('\nMe > ')
    server.send(msg)

def receive():
  while True:
    message = server.recv(1024)
    print('\n' + message.decode())

thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()