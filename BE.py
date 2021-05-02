#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 20:38:48 2021

@author: liyunhe
"""
import uuid
import socket
import pickle
import os
from flask import Flask, request, abort
app = Flask(__name__)
  
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('0.0.0.0', 8082))

tcp_socket.listen(3)
messages = []

while True:
    server_socket, addr = tcp_socket.accept()
    # print("connected ", addr)
    # initial = '220 0.0.0.0:8082'
    # server_socket.send(initial.encode())
    recv1 = server_socket.recv(1024).decode()
    print(recv1)
    if recv1[:4] == "HELO":
        response1 = '250 Hello' + recv1[9:] + ' Pleased to meet you'

        server_socket.send(response1.encode())
        recv2 = server_socket.recv(1024).decode()
        print(recv2)
        response2 = '250 ' + recv2[10:] + ' Sender ok'

        server_socket.send(response2.encode())
        recv3 = server_socket.recv(1024).decode()
        print(recv3)
        response3 = '250 ' + recv3[8:] + ' Recipient ok'

        server_socket.send(response3.encode())
        recv4 = server_socket.recv(1024).decode()
        print(recv4)
        response4 = "354 Enter mail, end with '.' on a line by itself"

        server_socket.send(response4.encode())

        message = server_socket.recv(1024).decode()
        messages.append(message)
        # uuid_str = uuid.uuid4().hex
        # file_name = 'email_%s.txt' % uuid_str
        if os.path.exists("messages.pickle"):
            os.remove("messages.pickle")
        message_file = open('messages.pickle', 'wb')
        pickle.dump(messages, message_file)
        message_file.close()
        print(message)

        server_socket.send('received!'.encode())
        recv5 = server_socket.recv(1024).decode('utf-8')
        print(recv5)

        response5 = '250 Message delivery'
        server_socket.send(response5.encode())

        recv6 = server_socket.recv(1024).decode()
        print(recv6)

        if recv6 == 'QUIT':
            response6 = '221 Email received successfully! 0.0.0.1:8081 is closing connection and '
            server_socket.send(response6.encode())
            server_socket.close()


    if recv1 == "list":
        if not os.path.exists('messages.pickle'):
            server_socket.send("[]".encode())
        else:
            list_file = open('messages.pickle', 'rb')
            list2 = pickle.load(list_file)
            mes_size = ""
            for i in range(0, len(list2)):
                mes_size += str(i + 1) + " " + str(len(list2[i])) + "\n"
            mes_size += "."
            server_socket.send(mes_size.encode())

            mes_len = len(list2)
            for i in range(1, mes_len + 1):
                recv_i = server_socket.recv(1024).decode()
                if recv_i[:4] == "retr":
                    print(recv_i)
                    server_socket.send(list2[i - 1].encode())
                recv_k = server_socket.recv(1024).decode()
                if recv_k[:4] == "dele":
                    print(recv_k)
                server_socket.send("1".encode())

        recv_2 = server_socket.recv(1024).decode()
        print(recv_2)
        if recv_2 == "quit":
            messages = []
            if os.path.exists('messages.pickle'):
                os.remove("messages.pickle")
            response_q = "+OK POP3 server signing off"
            server_socket.send(response_q.encode())
            server_socket.close()


# if __name__=="__main__":
#     app.run(host="0.0.0.0",port = 8082, debug=True)