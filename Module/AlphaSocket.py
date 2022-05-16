import socket
import time
import cv2
import numpy
import threading

# class AlphaPortList:
#     MainControlPort = 9990
#     VideoPort = 9991

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
        self.conn, addr = self.socket.accept()
        print('conneted from: '+str(addr))
        # send cmd to system
        # system read Buf[0] to run cmd
        while self.state:
            recv = self.conn.recv(self.RECVSIZE)
            recv = str(recv, encoding='utf-8').replace(' ','')
            # print('recv:',recv+'<')
            if recv=='quit':
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
        return 'quit'

class AlphaSocket:

    PortList = {
        'Control':9997,
        'Video': 9999,
    }
    ServerAddr = ('', PortList['Control'])

    def __init__(self, camera, lock) -> None:
        # create a main control TCP server
        self.Control = TCPControl(self.ServerAddr,lock)
        # create a VedioSocket
        self.Video = VideoStream(camera, self.PortList['Video'])
        
    def OpenVideo(self, IP, Gray=1, quality=50):
        self.Video.OpenVideo(IP, Gray, quality)
        # you need to call start() to start this Thread

    def CloseVideo(self):
        self.Video.close()
    
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



# def UDP_SERVER():
#     address = ('', 9999)
#     try:
#         udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         udp_server.bind(address)
#     except socket.error as msg:
#         print(msg)
#         sys.exit(1)
#     print('waiting for connection...')
#     print('client need to send \'start\' to set up vedio stream')
#     while True:
#         Signal, Addr = udp_server.recvfrom(1024)
#         if Signal.decode(encoding='utf-8') == 'start':
#             break
#     # data, addr = udp_server.recvfrom(1024)
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
#     while ret:
#         time.sleep(0.01)
#         result, img_encode = cv2.imencode('.jpg', frame, encode_param)
#         data = numpy.array(img_encode)
#         stringData = data.tostring()
#         _length = str(len(stringData)).ljust(16)
#         SendData = _length+stringData
#         udp_server.sendto(SendData.encode(encoding='utf-8'), Addr)
#         ret, frame = cap.read()
#         if cv2.waitKey(3) == ord('q'):
#             break
#     udp_server.close()
# class VideoSocket_TCP:

#     def __init__(self, cap) -> None:
#         self.camera = cap
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # FSM: ready -> start -> close -> ready
#         self.video_on = False
#     def start(self, Addr):
#         # try to connect server
#         self.ServerAddr = Addr
#         try:
#             self.socket.connect(Addr)
#         except socket.error as msg:
#             print(msg)
#             return 1
#         self.VideoStream_TCP()

#         # close
#         self.close()
    
#     def close(self):
#         print('\n--- Close VideoSokect ---\n')
#         self.video_on = False
#         pass
    
#     def VideoStream_TCP(self, Gray=1 ,quality=50):
#         ret, frame = self.camera.read()
#         encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
#         try:
#             while ret:
#                 time.sleep(0.01)
#                 # t1 = time.time()
#                 if Gray:
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#                 result, EncodeImg = cv2.imencode('.jpg', frame, encode_param)
#                 NPData = numpy.array(EncodeImg)
#                 Data = NPData.tobytes()
#                 Length = len(Data)
#                 self.socket.send(str.encode(str(Length).ljust(16)))
#                 self.socket.send(Data)
#                 ret, frame = self.camera.read()
#         except KeyboardInterrupt:
#             return         