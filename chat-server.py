import socket
import sys
import threading

#server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('192.168.0.19', 4000))
server.listen(5) #clients max number

print("Server ready, waiting for incoming connections...")

list_of_clients = []
names = {}

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def broadcast(message, connection):
    for client in list_of_clients:
        if client!=connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)

def clientthread(conn, addr):
    print('Client thread created')
    name = conn.recv(1024)
    names[addr] = name.decode()
    conn.send('Welcome to Yachay chatroom %s!, type [bye] to exit'.encode() % names[addr].encode())
    while True:
            try:
                message = conn.recv(1024)
                if message.decode() != '[bye]':
                    print (names[addr] + " > " + message.decode())
                    message_to_send = names[addr] + " > " + message.decode()
                    broadcast(message_to_send, conn)
                else:
                    conn.send('[bye]'.encode())
                    remove(conn)
                    conn.close()
                    msg = names[addr] + ' > has left the chat'
                    print(msg)
                    broadcast(msg, conn)
                    break
            except:
                continue
    return 1

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print ("Client: " + addr[0] + " connected")
    threading.Thread(target=clientthread, args=(conn,addr)).start()


server.close()