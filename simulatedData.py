import time
import random
from pythonosc.udp_client import SimpleUDPClient

# Your PC IP and the port your other script is listening on
ip = "127.0.0.1"  # Or use your actual IP
port = 10000

client = SimpleUDPClient(ip, port)

while True:
    # Simulate accelerometer and gyro data
    accel = [random.uniform(-1, 1) for _ in range(3)]
    gyro = [random.uniform(-0.5, 0.5) for _ in range(3)]

    # Send to matching OSC paths
    client.send_message("/accel", accel)
    client.send_message("/gyro", gyro)

    print(f"Sent accel: {accel}, gyro: {gyro}")
    time.sleep(0.1)
