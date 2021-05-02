#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from flask import  Flask,request,abort
app = Flask(__name__)
messages = []
@app.route('/email', methods =["GET"])
def index3():

    try:
        user_server_addr = request.url.strip('http://')
        i = user_server_addr.index('/')
        user_server_addr = user_server_addr[:i]
        j = user_server_addr.index(':')
        #user_server_addr_ip = user_server_addr[:j]
        #user_server_addr_port = int(user_server_addr[j + 1:])

        from_addr = request.args.get("from")
        index = from_addr.index(':')
        from_addr_ip = from_addr[:index]
        from_addr_port = int(from_addr[index + 1:])

        #BU_ip = user_server_addr_ip
        #BU_port = user_server_addr_port
        BE_ip = from_addr_ip
        BE_port = from_addr_port

        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((BE_ip, BE_port))


        listCommand = "list"
        tcp_socket.send(listCommand.encode())

        recv1 = tcp_socket.recv(1024).decode()
        if recv1 == "[]":
            messages = []
        else:
            print(recv1) #size and end point

            if recv1.count("\n") <=1:
                mes = recv1
                inde2 = mes.index(" ")
                mes_len = int(mes[:inde2])#length of messages
            else:
                mes = recv1[:-2]
                inde1 = len(mes)-mes[::-1].index("\n")
                inde2 = len(mes)-mes[::-1].index(" ")-1
                mes_len = int(mes[inde1:inde2]) #length of messages

            messages = []
            for i in range(1, mes_len + 1):
                retrCommand = "retr " + str(i)
                tcp_socket.send(retrCommand.encode())
                recv_i = tcp_socket.recv(1024).decode()
                print(recv_i)
                messages.append(recv_i)

                deleCommand = "dele"
                tcp_socket.send(deleCommand.encode())
                recv_k = tcp_socket.recv(1024).decode()

        quitCommand = "quit"
        tcp_socket.send(quitCommand.encode())
        print("success")
        recv2 = tcp_socket.recv(1024).decode()

        print(recv2)

        tcp_socket.close()

        return str(messages), 200

    except:
        return "URL wrong", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083, debug=True)