import socket
import threading
from datetime import datetime
from colorama import Fore, Style

def banner():
    print(Fore.CYAN + r"""
 _______ _____  _______         _______             _                 
|__   __|  __ \|__   __|       |__   __|           | |                
   | |  | |__) | | | __ _  ___    | |_ __ __ _  ___| | _____ _ __ ___ 
   | |  |  _  /  | |/ _` |/ __|   | | '__/ _` |/ __| |/ / _ \ '__/ __|
   | |  | | \ \  | | (_| | (__    | | | | (_| | (__|   <  __/ |  \__ \
   |_|  |_|  \_\ |_|\__,_|\___|   |_|_|  \__,_|\___|_|\_\___|_|  |___/
                                github.com/furkan-trj
""" + Style.RESET_ALL)

def scan_port(trabzon_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((trabzon_ip, port))
            if result == 0:
                print(Fore.GREEN + f"[+] Açık Port: {port}" + Style.RESET_ALL)
    except Exception:
        pass  # Hataları bastır

def main():
    banner()
    target = input("Hedef IP / Domain: ").strip()
    try:
        trabzon_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(Fore.RED + "[!] Geçersiz domain ya da IP!" + Style.RESET_ALL)
        return

    start_port = int(input("Başlangıç Portu: "))
    end_port = int(input("Bitiş Portu: "))

    print(Fore.MAGENTA + f"\n[+] {trabzon_ip} adresi taranıyor... [{start_port}-{end_port}]" + Style.RESET_ALL)
    start_time = datetime.now()

    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(trabzon_ip, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    duration = datetime.now() - start_time
    print(Fore.CYAN + f"\n[✓] Tarama tamamlandı ({duration.seconds} saniye)" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
