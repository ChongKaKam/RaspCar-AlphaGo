import socket
import time
import cv2
import numpy

class AlphaPortList:
    MainControlPort = 9990
    VideoPort = 9991

class VideoSocket_TCP:

    def __init__(self, cap, Server,port) -> None:
        self.camera = cap
        self.ServerAddr = (Server, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # FSM: ready -> start -> close -> ready
        self.state = 0
    def start(self):
        # try to connect server
        try:
            self.socket.connect(self.ServerAddr)
        except socket.error as msg:
            print(msg)
            return 1
        self.VideoStream_TCP()

        # close
        self.close()
    
    def close(self):
        print('\n--- Close VideoSokect ---\n')
        self.socket.close()
        pass
    
    def VideoStream_TCP(self, Gray=1 ,quality=50):
        ret, frame = self.camera.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        try:
            while ret:
                time.sleep(0.01)
                # t1 = time.time()
                if Gray:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                result, EncodeImg = cv2.imencode('.jpg', frame, encode_param)
                NPData = numpy.array(EncodeImg)
                Data = NPData.tobytes()
                Length = len(Data)
                self.socket.send(str.encode(str(Length).ljust(16)))
                self.socket.send(Data)
                ret, frame = self.camera.read()
        except KeyboardInterrupt:
            return 

class MoveSocket:
    
    pass

class AlphaSocket:

    PortList = {
        'Control':9990,
        'VedioPort': 9991,
    }
    def __init__(self) -> None:
        # create a main control TCP server
        
        # create a VedioSocket

        pass
    def start(self):
        
        pass
    pass

if __name__=="__main__":
    # cap = cv2.VideoCapture(0)
    # vs = VedioServer(cap)
    # vs.start()

    cap = cv2.VideoCapture(0)
    vs = VideoSocket_TCP(cap, "192.168.3.182", 9991)
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