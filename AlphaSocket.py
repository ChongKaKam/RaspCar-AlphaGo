import socket
import time
import cv2
import numpy
import sys

class VideoServer:
    def __init__(self, cap, Port=9990) -> None:
        self.cap = cap
        self.Addr = ('', Port)
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Server.bind(self.Addr)
        # TODO:state recorcd ?
        # ...
        print('---- server init success ---')

    def start(self):
        print('listening...')
        self.Server.listen(1)
        sock, addr = self.Server.accept()
        print('Connect from:', str(addr))
        self.SendVedio(sock)
        pass
    def close(self):
        pass
    
    def SendVedio(self, sock, quality=50):
        ret, frame = self.cap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        while ret:
            time.sleep(0.01)
            result, img_encode = cv2.imencode('.jpg', frame, encode_param)
            data_np = numpy.array(img_encode)
            data = data_np.tobytes()
            length = str.encode(str(len(data)).ljust(16))
            sock.send(length)
            print('length')
            sock.send(data)
            print('data')
            receive = sock.recv(1024)
            if len(receive):
                if str(receive, encoding='utf-8') == 'end':
                    break
            ret, frame = self.cap.read()
        # TODO:state change ?

class VideoSocket:
    def __init__(self, cap, port=9999) -> None:
        self.camera = cap
        self.ServerAddr = ('192.168.3.182', 9999)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        # try to connect server
        try:
            self.socket.connect(self.ServerAddr)
        except socket.error as msg:
            print(msg)
            return 1
        self.VideoStream()

        # close
        self.close()
    
    def close(self):
        pass
    
    def VideoStream(self, quality=95):
        ret, frame = self.camera.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        while ret:
            time.sleep(0.01)
            # t1 = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result, EncodeImg = cv2.imencode('.jpg', frame, encode_param)
            NPData = numpy.array(EncodeImg)
            Data = NPData.tobytes()
            Length = len(Data)
            self.socket.send(str.encode(str(Length).ljust(16)))
            self.socket.send(Data)
            # t2 = time.time()
            # print('cost:', t2-t1)
            # receive = self.socket.recv(1024)
            # if len(receive):
            #     if str(receive, encoding='utf-8')=='E':
            #         return
            ret, frame = self.camera.read()

class ControlSocket:
    
    pass

class AlphaSocketManger:
    pass

if __name__=="__main__":
    # cap = cv2.VideoCapture(0)
    # vs = VedioServer(cap)
    # vs.start()

    cap = cv2.VideoCapture(0)
    vs = VideoSocket(cap)
    vs.start()
    
    # while True:
    #     time.sleep(0.01)
    #     t1 = time.time()
    #     cap.read()
    #     t2 = time.time()
    #     print('t:', t2-t1)
    pass



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