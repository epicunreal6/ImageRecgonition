# -*- coding=utf-8 -*-
import socket
import threading
import sys
import os
import struct


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    while True:
        fileinfo_size = struct.calcsize('128sl')  # linux 和 windows 互传 128sl 改为 128sq  机器位数不一样，一个32位一个64位
        buf = conn.recv(fileinfo_size)
        print('收到的字节流：', buf, type(buf))
        if buf:
            print(buf, type(buf))
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.strip(str.encode('\00'))
            new_filename = os.path.join(str.encode('./'), str.encode('new_') + fn)
            print('file new name is {0}, filesize if {1}'.format(new_filename, filesize))
            recvd_size = 0  # 定义已接收文件的大小
            with open(new_filename, 'wb') as fp:
                print("start receiving...")
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(filesize - recvd_size)
                        recvd_size = filesize

                    fp.write(data)
            print("end receive...")
        conn.close()
        break


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 4096)) # 这里换上自己的ip和端口
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


if __name__ == '__main__':
    socket_service()