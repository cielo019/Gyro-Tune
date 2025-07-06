from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import pygame
import time

# 🔊 Initialize pygame mixer
pygame.mixer.init()

# 🎧 Load musical notes
notes = {
    'C': pygame.mixer.Sound("note_c.wav"),
    'D': pygame.mixer.Sound("note_d.wav"),
    'E': pygame.mixer.Sound("note_e.wav"),
    'F': pygame.mixer.Sound("note_f.wav"),
    'G': pygame.mixer.Sound("note_g.wav"),
    'A': pygame.mixer.Sound("note_a.wav"),
    'B': pygame.mixer.Sound("note_b.wav"),
}

# Load additional sound effects
extra_sounds = {
    'drum': pygame.mixer.Sound("drum.wav"),
    'effect': pygame.mixer.Sound("effect.wav"),
    'ambient': pygame.mixer.Sound("ambient.wav"),
}

# Set volumes (0.0 to 1.0)
for sound in notes.values():
    sound.set_volume(1.0)
for sound in extra_sounds.values():
    sound.set_volume(1.0)

# Use channels to manage sounds
channel_notes = pygame.mixer.Channel(0)
channel_fx = pygame.mixer.Channel(1)

# 🎼 Track last played note and ambient
last_note = None
last_ambient_triggered = False
last_note_time = 0

def accel_handler(address, x, y, z):
    global last_note, last_note_time, last_ambient_triggered

    print(f"Accel: x={x:.2f}, y={y:.2f}, z={z:.2f}")
    current_time = time.time()

    # 📌 Map X tilt to 7-note scale
    if x < -0.85:
        note = 'C'
    elif x < -0.6:
        note = 'D'
    elif x < -0.3:
        note = 'E'
    elif x < 0.0:
        note = 'F'
    elif x < 0.3:
        note = 'G'
    elif x < 0.6:
        note = 'A'
    else:
        note = 'B'

    # ✅ Only play note if it's new or after cooldown
    if note != last_note or current_time - last_note_time > 0.3:
        print(f"🎵 Playing note: {note}")
        channel_notes.play(notes[note])
        last_note = note
        last_note_time = current_time

    # 🥁 Trigger drum if Z accel exceeds threshold
    if abs(z) > 1.2:
        print("🥁 Drum triggered!")
        channel_fx.play(extra_sounds['drum'])

    # 🎧 Trigger FX if Y tilt positive
    if y > 0.6:
        print("🎧 FX triggered!")
        channel_fx.play(extra_sounds['effect'])

    # 🌫 Ambient triggered only once when Y < -0.6
    elif y < -0.6:
        if not last_ambient_triggered:
            print("🌫 Ambient triggered!")
            channel_fx.play(extra_sounds['ambient'])
            last_ambient_triggered = True
    else:
        last_ambient_triggered = False

# 🧭 OSC Server Setup
dispatcher = Dispatcher()
dispatcher.map("/accel", accel_handler)

ip = "0.0.0.0"
port = 10000

print(f"🎧 Listening for motion on {ip}:{port} ...")
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
server.serve_forever()
