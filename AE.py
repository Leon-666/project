#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:16:05 2021

@author: liyunhe
"""

import socket
from flask import  Flask,request,abort
# app=Flask(__name__)  
  
tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
tcp_socket.bind(('0.0.0.0',8081))

tcp_socket.listen(10)   

# client_socket,addr=tcp_socket.accept() 
while True:
    client_socket,addr=tcp_socket.accept() 
    # print("connected ", addr)
    
    initial = '220 0.0.0.0:8081'
    client_socket.send(initial.encode())
    recv1=client_socket.recv(1024).decode()
    print(recv1)
    response1 = '250 Hello' + recv1[9:] + ' Pleased to meet you'
    
    client_socket.send(response1.encode())   
    recv2 = client_socket.recv(1024).decode()
    print(recv2)
    response2 = '250 '+recv2[10:] + ' Sender ok'
    from_addr = recv2[10:]
    left_from_addr = recv2.find(':')
    right_from_addr = recv2.rfind(':')
    from_addr_ip = recv2[left_from_addr+1:right_from_addr].strip()
    from_addr_port = int(recv2[right_from_addr+1:].strip())
    print(from_addr_ip)
    print(from_addr_port)
    
    
    client_socket.send(response2.encode())
    recv3 = client_socket.recv(1024).decode()
    print(recv3)
    response3 = '250 '+ recv3[8:] + ' Recipient ok'
    to_addr = recv3[8:]
    left_to_addr = recv3.find(':')
    right_to_addr = recv3.rfind(':')
    to_addr_ip = recv3[left_to_addr+1:right_to_addr].strip()
    to_addr_port = int(recv3[right_to_addr+1:].strip())
    print(to_addr_ip)
    print(to_addr_port)
    
    
    client_socket.send(response3.encode())
    recv4 = client_socket.recv(1024).decode()
    print(recv4)
    response4 = "354 Enter mail, end with '.' on a line by itself"
    
    client_socket.send(response4.encode())
    message = client_socket.recv(1024).decode()

    
    print(message)
    client_socket.send('received!'.encode())
    # print(from_addr)
    # print(to_addr)
    #response5 = '250 Message accepted for delivery'
    
    #client_socket.send(response5.encode())
    recv5 = client_socket.recv(1024).decode('utf-8')
    print(recv5)
         
    response5 = '250 Message accepted for delivery'
    client_socket.send(response5.encode('utf-8'))
    
        
    recv6 = client_socket.recv(1024).decode('utf-8')
    print(recv6)
    
    
    # if recv6 == 'QUIT':
    #     response6 = '221 0.0.0.0:8081 is closing connection'  
    #     client_socket.send(response6.encode())
    #     client_socket.close()
        
    
    


#send message to Bob's email server
    tcp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket1.connect((to_addr_ip,to_addr_port))
    # receiver = to_addr#to_addr
    
    #recv = tcp_socket1.recv(1024).decode()
    #print('message after connection request ' + recv)
    #if recv[:3] != '220':
            #print('220 reply not received from server1')
    
    heloCommand = 'HELO I am ' + from_addr
    tcp_socket1.send(heloCommand.encode())
    
    recv1 = tcp_socket1.recv(1024).decode()
    # print(heloCommand)
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server2')
    
    mailFrom = "Mail From: " + from_addr
    tcp_socket1.send(mailFrom.encode())
    
    recv2 = tcp_socket1.recv(1024).decode()
    # print(mailFrom)
    print(recv2)
    if recv2[:3] != '250':
        print('250 Reply not received from server3')
        
    rcptTo = "RCPT TO: " + to_addr
    tcp_socket1.send(rcptTo.encode())
    
    recv3 = tcp_socket1.recv(1024).decode()
    # print(rcptTo)
    print(recv3)
    if recv3[:3] != '250':
        print('250 Reply not received from server4')
    
    
    data = "DATA\r\n"
    tcp_socket1.send(data.encode())
    recv4 = tcp_socket1.recv(1024).decode()
    # print(data)
    print(recv4)
    if recv4[:3] != '354':
        print('250 Reply not received from server5')
        
    tcp_socket1.send((message).encode())
    rec = tcp_socket1.recv(1024)
    
    
    endLine = '.'
    tcp_socket1.send(endLine.encode())
    
    recv6 = tcp_socket1.recv(1024).decode()
    # print(recv6)

    print(recv6)
    if recv6[:3] != '250':
          print('250 Reply not received from server7')
    
    
    q = 'QUIT'
    
    tcp_socket1.send(q.encode())
    recv7 = tcp_socket1.recv(1024).decode()
    # # print(q)
    print(recv7)
    if recv7[:3] != '221':
        print('250 Reply not received from server9')
    else:
        response6 = '221 Sent successfully! 0.0.0.0:8081 is closing connection'  
        client_socket.send(response6.encode())
        client_socket.close()
        
    
    tcp_socket1.close()


# if __name__=="__main__":
#     app.run(host="0.0.0.0",port = 8081, debug=True) 


    