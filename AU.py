#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 22:42:00 2021

@author: liyunhe
"""
import socket
from datetime import date
from flask import Flask,request,abort
app=Flask(__name__)


@app.route('/email', methods =["GET"])
def index1():
    
    try:
        user_server_addr = request.url.strip('http://')
        i = user_server_addr.index('/')
        user_server_addr = user_server_addr[:i]
        j=user_server_addr.index(':')
        user_server_addr_ip=user_server_addr[:j]
        user_server_addr_port=user_server_addr[j+1:]
        
        from_addr = request.args.get("from")
        index = from_addr.index(':')
        from_addr_ip = from_addr[:index]
        from_addr_port = int(from_addr[index+1:])
        
        to_addr = request.args.get("to")
        index1 = to_addr.index(':')
        to_addr_ip = to_addr[:index1]
        to_addr_port = int(to_addr[index1+1:])
        
        message = request.args.get("message")
        
        sender = user_server_addr_ip
        port = int(user_server_addr_port)
        receiver = from_addr
        
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((from_addr_ip,from_addr_port))
        
        recv = tcp_socket.recv(1024).decode()
        print('message after connection request ' + recv)
        if recv[:3] != '220':
            print('220 reply not received from server1')
            
        heloCommand = 'HELO I am ' + user_server_addr
        tcp_socket.send(heloCommand.encode())
        
        recv1 = tcp_socket.recv(1024).decode()
        # print(heloCommand)
        print(recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server2')
        
        mailFrom = "Mail From: " + from_addr
        tcp_socket.send(mailFrom.encode())
        
        recv2 = tcp_socket.recv(1024).decode()
        # print(mailFrom)
        print(recv2)
        if recv2[:3] != '250':
            print('250 Reply not received from server3')
            
        rcptTo = "RCPT TO: " + to_addr
        tcp_socket.send(rcptTo.encode())
        
        recv3 = tcp_socket.recv(1024).decode()
        # print(rcptTo)
        print(recv3)
        if recv3[:3] != '250':
            print('250 Reply not received from server4')
        
        
        data = "DATA\r\n"
        tcp_socket.send(data.encode())
        recv4 = tcp_socket.recv(1024).decode()
        # print(data)
        print(recv4)
        if recv4[:3] != '354':
            print('250 Reply not received from server5')
            
        tcp_socket.send((message).encode())
        rec = tcp_socket.recv(1024)
        
        endLine = '.'
        tcp_socket.send(endLine.encode('utf-8'))
        
        recv6 = tcp_socket.recv(1024).decode('utf-8')
        # print(recv6)
        # # print('.')
        print(recv6)
        if recv6[:3] != '250':
           print('250 Reply not received from server7')
        
        
        q = 'QUIT'
        
        tcp_socket.send(q.encode())
        recv7 = tcp_socket.recv(1024).decode()
        # # print(q)
        print(recv7)
        if recv7[:3] != '221':
             print('250 Reply not received from server9')
            
        
        # tcp_socket.send(message.encode())
        # data = tcp_socket.recv(1024)
        # print('Received', data)                          
        
        tcp_socket.close()
                
        return  "successfully", 200
    except:
        return "URL wrong", 400



@app.route('/date')
def index2():
    today = date.today()
    today = str(today)
    # return '<p> {} {} <p>'.format(today, 'HTTP 200')
    return today, 200



    
    
if __name__=="__main__":
    
    app.run(host="0.0.0.0",port = 8080, debug=True)   