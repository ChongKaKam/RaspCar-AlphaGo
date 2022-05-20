import socket
import threading
import time
from multiprocessing import Process

import cv2
import numpy
from pynput import keyboard

class AlphaGoClient:
    def __init__(self, ServerAddr) -> None:
        self.AlphaServer = ServerAddr
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.VideoState = False


    def __on_press(self, key):
        try:
            char = key.char
            self.TCP.send(char.encode(encoding='utf-8'))
            if char == 'v':
                self.OpenVideoStream()
        except AttributeError:
            pass

    def __on_release(self, key):
        try:
            char = key.char
            if char == 'q':
                self.TCP.send(char.encode(encoding='utf-8'))
                self.TCP.close()
                return False
            elif char=='w' or char=='s' or char=='a' or char=='d':
                char = 'stop'
                self.send(char.encode(encoding='utf-8'))
            else:
                print('key release')
            
        except AttributeError:
            if key==keyboard.Key.esc:
                return False

    def __recvall(self,sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def RecvVideoStream(self):
        host = ('',9999)
        VideoStream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        VideoStream.bind(host)
        VideoStream.listen(1)
        self.conn, self.conAddr = VideoStream.accept()
        print('connect from:', str(self.conAddr))
        font = cv2.FONT_HERSHEY_COMPLEX
        self.VideoState = True
        while self.VideoState:
            start = time.time()
            length = self.__recvall(self.conn, 16)
            if length == None: break
            stringData = self.__recvall(self.conn, int(length))
            data = numpy.frombuffer(stringData, numpy.uint8)
            ImgDec = cv2.imcode(data, cv2.IMREAD_COLOR)
            end = time.time()
            fps_time = end-start
            fps = 1/fps_time
            cv2.putText(ImgDec, 'FPS: '+str(int(fps)), (10,30), font, 1, (0,255,0), 2, cv2.LINE_AA )
            cv2.imshow('VideoStream', ImgDec)
            k = cv2.waitKey(10)
            if k == ord('q'):
                break
        self.conn.close()
        VideoStream.close()
        print('VideoStream Close'.center(20,'-'))
        cv2.destroyAllWindows()
    
    def OpenVideoStream(self):
        
        self.VideoProcess = Process(target=self.RecvVideoStream)
        self.VideoProcess.start()


    def Connect(self):
        self.TCP.connect(self.AlphaServer)
        self.keyboard = keyboard.Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.keyboard.start()

if __name__=="__main__":
    IP = '192.168.3.13'
    Port = 9997
    Addr = (IP, Port)
    Client = AlphaGoClient(Addr)
    Client.conn()
    Client.keyboard.join()
    if Client.VideoProcess.is_alive():
        Client.VideoProcess.join()