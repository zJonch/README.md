import socket
import sys
import random

def udp_bypass(ip, port, header, packet_size):
    try:
        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Enviando paquetes UDP a {ip}:{port} con tamaño {packet_size} bytes y cabecera personalizada:\n{header}\n")

        # Añadir la cabecera al inicio del payload
        payload = f"{header}\n" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=packet_size - len(header) - 1))
        
        while True:
            # Enviar el paquete
            sock.sendto(payload.encode(), (ip, int(port)))
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python3 udp_bypass_minimal.py <IP> <PORT> <HEADER> <PACKET_SIZE>")
        sys.exit(1)

    # Leer los argumentos
    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    custom_header = sys.argv[3]
    packet_size = int(sys.argv[4])

    # Validar tamaño del paquete
    if packet_size <= len(custom_header):
        print("Error: El tamaño del paquete debe ser mayor que el tamaño de la cabecera.")
        sys.exit(1)

    # Ejecutar el bypass UDP
    udp_bypass(target_ip, target_port, custom_header, packet_size)
