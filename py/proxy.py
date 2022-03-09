# coding=utf-8
#!/usr/bin/python

import socket
import threading
import time
import select

class my_proxy_server():
    
    def __init__(self):
    
        self.f2pool_ip = '127.65.211.125'
        self.f2pool_port = 6688
        
        self.server_ip = '0.0.0.0'
        self.server_port = 8888
        self.PKT_BUFF_SIZE = 2048
        
    def wait_connect(self):
        
        # 绛夊緟閾炬帴
        local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_server.bind((self.server_ip, self.server_port))
        local_server.listen(100)
        
        while True:
            try:
                print('等待连接')
                (local_conn, local_addr) = local_server.accept()
                print('接到连接')
            except Exception as e:
                print('连接失败')
                continue
            
            # 鏀跺埌閾炬帴  寤虹珛涓巉2pool鐨勯摼鎺

            threading.Thread(target=self.request_work, args=(local_conn,)).start()
        
    def request_work(self,local_conn):
        
        #鏀跺埌閾炬帴  寤虹珛涓巉2pool鐨勯摼鎺

        local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('连接bn')
            local_server.connect((self.f2pool_ip,self.f2pool_port))
        except Exception as e:
            print('连接失败')
            local_conn.close()
            return 
        #璁╀袱涓摼鎺ュ紑濮嬮€氫俊
        threading.Thread(target=self.nonblocking, args=(local_server, local_conn)).start()
        
    def nonblocking(self,client,target):
    
        #涓や釜閾炬帴鐩存帴鐨勯€氫俊
        with open('data.txt', 'a') as f:
   
            inputs=[client,target]
            while True:
                readable,writeable,errs=select.select(inputs,[],inputs,3)
                if errs:
                    break
                for soc in readable:
                    data=soc.recv(self.PKT_BUFF_SIZE)
                    if data:
                        if soc is client:
                            target.send(data)
                        elif soc is target:
                            client.send(data)
                        f.write(data)  #文件的写操作
                        f.write('\n')
                    else:
                        break
            client.close()
            target.close()
        
proxy = my_proxy_server()
proxy.wait_connect()