import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to port 10000 (same as in your App)
server_address = ('0.0.0.0', 10000)
sock.bind(server_address)

print("🎧 Listening for motion data on port 10000...\n")

while True:
    data, address = sock.recvfrom(1024)
    print("📲 Received from", address, ":", data.decode())
