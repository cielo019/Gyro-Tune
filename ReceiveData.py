from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


def accel_handler(address, *args):
    print(f"Accelerometer {address}: {args}")


def gyro_handler(address, *args):
    print(f"Gyroscope {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/accel", accel_handler)
dispatcher.map("/gyro", gyro_handler)

ip = "0.0.0.0"  # Listen on all interfaces
port = 10000    # Use same port as in app

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"Listening on {ip}:{port}")
server.serve_forever()
