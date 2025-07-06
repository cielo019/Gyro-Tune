from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import pygame

# 🔊 Initialize pygame mixer
pygame.mixer.init()

# 🎧 Load your downloaded .wav sound files
sound1 = pygame.mixer.Sound("sound1.wav")  # Tilt left
sound2 = pygame.mixer.Sound("sound2.wav")  # Tilt right
sound3 = pygame.mixer.Sound("sound4.wav")  # Neutral

# 🎯 Handle incoming accelerometer data
def accel_handler(address, x, y, z):
    print(f"Accel: x={x:.2f}, y={y:.2f}, z={z:.2f}")

    # 📌 Map x-axis tilt to sound
    if x < -0.5:
        print("Tilt Left: Playing sound1")
        sound1.play()
    elif x > 0.5:
        print("Tilt Right: Playing sound2")
        sound2.play()
    else:
        print("Neutral: Playing sound3")
        sound3.play()

# 🧭 Set up OSC server
dispatcher = Dispatcher()
dispatcher.map("/accel", accel_handler)  # Match your OSC path

ip = "0.0.0.0"
port = 10000  # Same as your simulated or real data sender

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"🎧 Listening on {ip}:{port} for motion data...")
server.serve_forever()
