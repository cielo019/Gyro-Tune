from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import pygame
import statistics
from collections import deque
import time

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

# 🎶 Load effects
fx = {
    'drum': pygame.mixer.Sound("drum.wav"),
    'effect': pygame.mixer.Sound("effect.wav"),
    'ambient': pygame.mixer.Sound("ambient.wav"),
}

# Channels
channel_notes = pygame.mixer.Channel(0)
channel_fx = pygame.mixer.Channel(1)

# State variables
last_note = None
ambient_triggered = False
mode = "notes"
last_drum_time = 0  # Cooldown for drums

# Rolling average for smooth accelerometer
window_size = 5
x_vals, y_vals, z_vals = deque(maxlen=window_size), deque(maxlen=window_size), deque(maxlen=window_size)

def accel_handler(address, x, y, z):
    global last_note, ambient_triggered, mode, last_drum_time

    # Append new values
    x_vals.append(x)
    y_vals.append(y)
    z_vals.append(z)

    # Smoothed values
    x = statistics.mean(x_vals)
    y = statistics.mean(y_vals)
    z = statistics.mean(z_vals)

    now = time.time()
    print(f"Accel: x={x:.2f}, y={y:.2f}, z={z:.2f}, mode={mode}")

    # -----------------
    # Notes mode
    # -----------------
    if mode == "notes":
        # Map X-axis to 7 notes (equal slices)
        if x < -0.714: note = 'C'
        elif x < -0.429: note = 'D'
        elif x < -0.143: note = 'E'
        elif x < 0.143:  note = 'F'
        elif x < 0.429:  note = 'G'
        elif x < 0.714:  note = 'A'
        else: note = 'B'

        # Continuous note playback
        if note != last_note:
            if last_note is not None:
                channel_notes.stop()  # Stop previous note
            channel_notes.play(notes[note], loops=-1)  # Play current note indefinitely
            last_note = note
            print(f"🎵 Playing {note}")

        # Drum trigger (Z-axis) with short cooldown
        if abs(z) > 1.2 and now - last_drum_time > 0.2:
            print("🥁 Drum!")
            channel_fx.play(fx['drum'])
            last_drum_time = now

    # -----------------
    # FX mode
    # -----------------
    if mode == "fx":
        # Effect trigger
        if y > 0.6:
            print("🎧 FX!")
            channel_fx.play(fx['effect'])

        # Ambient trigger
        elif y < -0.6 and not ambient_triggered:
            print("🌫 Ambient!")
            channel_fx.play(fx['ambient'])
            ambient_triggered = True
        elif -0.6 <= y <= 0.6:
            ambient_triggered = False

# -----------------
# OSC server setup
# -----------------
dispatcher = Dispatcher()
dispatcher.map("/accel", accel_handler)

ip = "0.0.0.0"
port = 10000

print(f"🎧 Listening on {ip}:{port}...")
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()
