import socket
import threading
import time

import cv2
import numpy


class VideoStream(threading.Thread):
    def __init__(self, cap, port) -> None:
        super(VideoStream, self).__init__()
        self.camera = cap
        self.Port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.state = False

    def run(self):
        self.state = True
        self._VideoSend()
        print('close VideoStream')

    def OpenVideo(self, IP, Gray=1, quality=50):
        self.ServerAddr = (IP, self.Port)
        self.Gray = Gray
        self.quality = quality

    def _VideoSend(self):
        time.sleep(1)
        try:
            self.socket.connect(self.ServerAddr)
        except socket.error as msg:
            print(msg)
            return 1
        print('Video: connect server!')
        ret, frame = self.camera.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
        while (ret and self.state):
            if self.Gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result, EncodeImg = cv2.imencode('.jpg', frame, encode_param)
            NPData = numpy.array(EncodeImg)
            Data = NPData.tobytes()
            Length = len(Data)
            self.socket.send(str.encode(str(Length).ljust(16)))
            self.socket.send(Data)
            ret, frame = self.camera.read()
        self.socket.close()
        return 0    

    def close(self):
        print('close video stream'.center(20,'-'))
        self.state = False

class TCPControl(threading.Thread):

    RECVSIZE = 32
    BUFSIZE = 8
    def __init__(self, Addr, lock) -> None:
        super(TCPControl, self).__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.state = False
        self.connection = False
        self.Addr = Addr
        self.TreadLock = lock
        self.Buf = []
        self.VideoIP = ''

    def run(self):
        self.state = True
        self._StartServer()
        print('close TCP')

    def _StartServer(self):
        self.socket.bind(self.Addr)
        print('-- start TCP control --')
        self.socket.listen(1)
        self.conn, self.ip = self.socket.accept()
        print('conneted from: '+str(self.ip))
        self.connection = True
        # send cmd to system
        # system read Buf[0] to run cmd
        while self.state:
            recv = self.conn.recv(self.RECVSIZE)
            recv = str(recv, encoding='utf-8').replace(' ','')
            # print('recv:',recv+'<')
            if recv=='q':
                self.state = False
                break
            # if recv=='VSON':
            #     lock.acquire()
            #     ip = self.conn.recv(16)
            #     ip = str(ip, encoding='utf-8').replace(' ','')
            #     self.VideoIP = ip
            #     lock.release()
            # lock
            self.TreadLock.acquire()
            if len(self.Buf) >= self.BUFSIZE:
                # if buff is over, drop this data
                continue
            self.Buf.append(recv)
            # release
            self.TreadLock.release()
            time.sleep(0.001) 
        self.conn.close()
        self.conn = None
        return 0
    
    def close(self):
        self.state = False
        self.socket.close()

    def getData(self):
        if self.state:
            self.TreadLock.acquire()
            if len(self.Buf) > 0:
                data = self.Buf.pop(0)
                self.TreadLock.release()
                return data
            else:
                self.TreadLock.release()
                return None
        return 'already quit'

class AlphaSocket:

    PortList = {
        'Control':9997,
        'Video': 9999,
    }
    ServerAddr = ('', PortList['Control'])

    def __init__(self, camera, lock) -> None:
        # create a main control TCP server
        self.Control = TCPControl(self.ServerAddr,lock)
        self.camera = camera
        self.ifOpenVideo = False
        self.Video = None
        # create a VedioSocket
        # self.Video = VideoStream(camera, self.PortList['Video'])
        
    def OpenVideo(self, IP, Gray=1, quality=50):
        self.ifOpenVideo = True
        self.Video = VideoStream(self.camera, self.PortList['Video'])
        self.Video.OpenVideo(IP, Gray, quality)
        # you need to call start() to start this Thread
        self.Video.start()

    def CloseVideo(self):
        if self.Video == None: return
        self.ifOpenVideo = False
        self.Video.close()
        self.Video = None
        
        
    
    def CloseControl(self):
        self.Control.close()
        
    

if __name__=="__main__":
    # cap = cv2.VideoCapture(0)
    # vs = VedioServer(cap)
    # vs.start()

    IP = "192.168.3.182"
    cap = cv2.VideoCapture(0)
    lock = threading.Lock()
    sockets = AlphaSocket(cap, lock)
    sockets.Control.start()
    try:
        while True:
            time.sleep(0.005)
            #  print('state: running')
            data = sockets.Control.getData()
            if data == None: continue
            print('data:',data+'|')
            if data[:5] == 'VSON:':
                ip = data[5:]
                print('IP:', ip)
                sockets.OpenVideo(ip)
                print('open video')
                if sockets.Video.state==False:
                    time.sleep(1)
                    sockets.Video.start()
            if data =='VSONOFF':
                pass
            if data == 'quit':
                print('close control')
                sockets.Control.join()
                sockets.CloseControl()
                break
    except KeyboardInterrupt:
        sockets.Control.close()


    # cap = cv2.VideoCapture(0)
    # IP = "192.168.3.182"
    # # vs = VideoSocket_TCP(cap)
    # #  vs.start(Addr)
    # t = VideoStream(cap, 9991)
    # t.OpenVideo(IP)
    # t.start()
    # try:
    #     while True:
    #         print('main running')
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     t.close()
        
    
    # while True:
    #     time.sleep(0.01)
    #     t1 = time.time()
    #     cap.read()
    #     t2 = time.time()
    #     print('t:', t2-t1)
    
    # pass