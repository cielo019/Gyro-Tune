from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import pygame
import statistics
from collections import deque

# 🔊 Initialize pygame
pygame.mixer.init()

# 🎵 Load notes
notes = {
    'C': pygame.mixer.Sound("note_c.wav"),
    'D': pygame.mixer.Sound("note_d.wav"),
    'E': pygame.mixer.Sound("note_e.wav"),
    'F': pygame.mixer.Sound("note_f.wav"),
    'G': pygame.mixer.Sound("note_g.wav"),
    'A': pygame.mixer.Sound("note_a.wav"),
    'B': pygame.mixer.Sound("note_b.wav"),
}

# 🎶 Effects
fx = {
    'drum': pygame.mixer.Sound("drum.wav"),
    'effect': pygame.mixer.Sound("effect.wav"),
    'ambient': pygame.mixer.Sound("ambient.wav"),
}

# Channels
channel_notes = pygame.mixer.Channel(0)
channel_fx = pygame.mixer.Channel(1)

# State
last_note = None
ambient_triggered = False
mode = "notes"

# Smooth values (rolling average)
window_size = 5
x_vals, y_vals, z_vals = deque(maxlen=window_size), deque(maxlen=window_size), deque(maxlen=window_size)

def accel_handler(address, x, y, z):
    global last_note, ambient_triggered, mode

    # Add new values for smoothing
    x_vals.append(x); y_vals.append(y); z_vals.append(z)

    # Use average to reduce jitter
    x = statistics.mean(x_vals)
    y = statistics.mean(y_vals)
    z = statistics.mean(z_vals)

    print(f"Accel: x={x:.2f}, y={y:.2f}, z={z:.2f}, mode={mode}")

    # 🎼 Notes mode (immediate)
    if mode == "notes":
        if x < -0.714:
            note = 'C'
        elif x < -0.429:
            note = 'D'
        elif x < -0.143:
            note = 'E'
        elif x < 0.143:
            note = 'F'
        elif x < 0.429:
            note = 'G'
        elif x < 0.714:
            note = 'A'
        else:
            note = 'B'

        # Play only if note changed
        if note != last_note:
            print(f"🎵 Playing {note}")
            channel_notes.play(notes[note])
            last_note = note

        # Drum trigger (instant)
        if abs(z) > 1.2:
            print("🥁 Drum!")
            channel_fx.play(fx['drum'])

    # 🎧 FX mode (instant)
    if mode == "fx":
        if y > 0.6:
            print("🎧 FX!")
            channel_fx.play(fx['effect'])
        elif y < -0.6 and not ambient_triggered:
            print("🌫 Ambient!")
            channel_fx.play(fx['ambient'])
            ambient_triggered = True
        elif -0.6 <= y <= 0.6:
            ambient_triggered = False


# 🧭 OSC setup
dispatcher = Dispatcher()
dispatcher.map("/accel", accel_handler)

ip = "0.0.0.0"
port = 10000

print(f"🎧 Listening on {ip}:{port}...")
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()
