import socket
import time
import cv2
import numpy
import sys

def SendVideo():
    # 192.168.3.182
    # 192.168.207.19
    address = ('192.168.3.182', 9999)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    while ret:
        time.sleep(0.01)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result, imgencode = cv2.imencode('.jpg',frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        sock.send(str.encode(str(len(stringData)).ljust(16)))
        sock.send(stringData)
        receive = sock.recv(1024)
        # if len(receive): print(str(receive,encoding='utf-8'))
        ret, frame = cap.read()
        if cv2.waitKey(10) == ord('q'):
            
            break
    sock.close()

if __name__=="__main__":
    SendVideo()
