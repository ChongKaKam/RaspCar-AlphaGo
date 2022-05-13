import time
import socket

address= ('', 9999)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(address)
dt = 0
time_start = time.time()
try:
    while True:
        print('wait for command')
        data, addr = server.recvfrom(1024)
        if len(data):
            time_check = time.time()
            dt = time_check-time_start
            time_start = time_check
            print('dt:',dt, 'COMMADN:', data.decode(encoding='utf-8'))
except KeyboardInterrupt:
    server.close()

