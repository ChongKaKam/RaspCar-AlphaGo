from ast import Add
import socket
import threading
import time
from multiprocessing import Process

import cv2
import numpy
from pynput import keyboard

def __recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
VideoProcess = None
ifOpenVideo = False
def CreateVideoStream():
    global ifOpenVideo
    global VideoProcess
    if ifOpenVideo: return
    ifOpenVideo = True
    VideoProcess = Process(target=ReceiveVideo)
    VideoProcess.start()

def ReceiveVideo():
    address = ('', 9999)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected from:' + str(addr))
    while True:
        start = time.time()
        length = __recvall(conn, 16)
        if length == None: break
        stringData = __recvall(conn, int(length))
        data = numpy.frombuffer(stringData, numpy.uint8)
        decimg = cv2.imdecode(data,cv2.IMREAD_COLOR)
        end = time.time()
        fps_time = end - start
        fps = 1/fps_time
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(decimg, 'FPS: '+str(int(fps)),(10,30), font,1 , (0,255,0), 2, cv2.LINE_AA)
        cv2.imshow('SERVER', decimg)
        k = cv2.waitKey(10)
        if k==ord('q'):
            break
    sock.close()
    print('server close')
    cv2.destroyAllWindows()



class AlphaGoClient:
    def __init__(self, AlphaAddr) -> None:
        self.AlphaAddr = AlphaAddr
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keyboard = keyboard.Listener(on_press=self.__on_press, on_release=self.__on_release)
    def __on_press(self,key):
        try:
            char = key.char
            self.TCP.send(char.encode(encoding='utf-8'))
            if char == 'v':
                CreateVideoStream()
            if char == 'b':
                global ifOpenVideo
                ifOpenVideo = False
        except AttributeError:
            pass
        
    def __on_release(self, key):
        try:
            char = key.char
            if char=='q':
                self.TCP.send(char.encode(encoding='utf-8'))
                self.TCP.close()
                return False
            elif char=='w' or char=='s' or char=='a' or char=='d':
                char = 'stop'
                self.TCP.send(char.encode(encoding='utf-8'))
            else:
                print('release')
        except AttributeError:
            if key==keyboard.Key.esc:
                return False
    def run(self):
        self.TCP.connect(self.AlphaAddr)
        self.keyboard.start()

if __name__=='__main__':
    IP = '192.168.3.13'
    Port = 9997
    Addr = (IP, Port)
    sys = AlphaGoClient(Addr)
    sys.run()
    sys.keyboard.join()
    sys.keyboard.is_alive
    if VideoProcess != None:
        if VideoProcess.is_alive():
            VideoProcess.join()
    
