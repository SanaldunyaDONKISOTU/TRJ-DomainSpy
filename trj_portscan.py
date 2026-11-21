#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import concurrent.futures
import socket
import sys
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = WHITE = ""
    class Style:
        BRIGHT = RESET_ALL = ""

IMZA = "TRJ | Siber Güvenlik Araçları"
SIK_KULLANILAN_PORTLAR = [
    20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 123, 135, 139, 143,
    161, 389, 443, 445, 465, 587, 993, 995, 1433, 1521, 3306, 3389,
    5432, 5900, 6379, 8080, 8443, 8888, 9200, 27017
]

SERVISLER = {
    20: "FTP-Veri", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 80: "HTTP", 110: "POP3",
    123: "NTP", 135: "MS-RPC", 139: "NetBIOS", 143: "IMAP",
    161: "SNMP", 389: "LDAP", 443: "HTTPS", 445: "SMB",
    465: "SMTPS", 587: "SMTP", 993: "IMAPS", 995: "POP3S",
    1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis", 8080: "HTTP-Alternatif",
    8443: "HTTPS-Alternatif", 8888: "HTTP-Alternatif", 9200: "Elasticsearch",
    27017: "MongoDB"
}

def logo_goster():
    print(Fore.CYAN + Style.BRIGHT + r"""
 _____ ____       _   ____            _
|_   _|  _ \     | | |  _ \ ___  _ __| |_
  | | | |_) |____| | | |_) / _ \| '__| __|
  | | |  __/_____| | |  __/ (_) | |  | |_
  |_| |_|        |_| |_|   \___/|_|   \__|

       PORT & SERVİS KEŞİF ARACI
""")
    print(Fore.WHITE + f"  {IMZA}\n")

def port_listesi_coz(girdi):
    portlar = set()
    for parca in girdi.split(","):
        parca = parca.strip()
        if not parca:
            continue
        if "-" in parca:
            bolumler = parca.split("-", 1)
            if len(bolumler) != 2 or not bolumler[0].isdigit() or not bolumler[1].isdigit():
                raise ValueError(f"Port aralığı hatalı: {parca}")
            baslangic, bitis = map(int, bolumler)
            if baslangic > bitis:
                raise ValueError(f"Aralık başlangıcı bitişten büyük: {parca}")
            if baslangic < 1 or bitis > 65535:
                raise ValueError("Port numaraları 1 ile 65535 arasında olmalıdır.")
            portlar.update(range(baslangic, bitis + 1))
        else:
            if not parca.isdigit():
                raise ValueError(f"Port numarası geçersiz: {parca}")
            port = int(parca)
            if not 1 <= port <= 65535:
                raise ValueError("Port numaraları 1 ile 65535 arasında olmalıdır.")
            portlar.add(port)
    if not portlar:
        raise ValueError("Port listesi boş.")
    if len(portlar) > 65535:
        raise ValueError("Port sayısı sınırı aşıldı.")
    return sorted(portlar)

def servis_adi(port):
    if port in SERVISLER:
        return SERVISLER[port]
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Bilinmeyen"

def port_kontrol(hedef_ip, port, zaman_asimi, banner_al):
    durum = {
        "port": port,
        "servis": servis_adi(port),
        "durum": "Kapalı / Filtreli",
        "banner": ""
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soket:
            soket.settimeout(zaman_asimi)
            sonuc = soket.connect_ex((hedef_ip, port))
            if sonuc == 0:
                durum["durum"] = "AÇIK"
                if banner_al:
                    try:
                        soket.settimeout(min(zaman_asimi, 1.5))
                        gelen = soket.recv(256)
                        durum["banner"] = gelen.decode("utf-8", errors="replace").strip()
                    except (socket.timeout, OSError):
                        pass
    except (socket.timeout, OSError):
        pass
    return durum

def rapor_kaydet(dosya, hedef, ip, sonuclar):
    with open(dosya, "w", encoding="utf-8") as cikti:
        cikti.write("TRJ PORTSCAN - TARAMA RAPORU\n")
        cikti.write("=" * 42 + "\n")
        cikti.write(f"Hedef: {hedef}\nIP: {ip}\nTarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
        aciklar = [sonuc for sonuc in sonuclar if sonuc["durum"] == "AÇIK"]
        if not aciklar:
            cikti.write("Açık port bulunamadı.\n")
        for sonuc in aciklar:
            cikti.write(f"{sonuc['port']}/tcp  {sonuc['servis']}  AÇIK\n")
            if sonuc["banner"]:
                cikti.write(f"  Banner: {sonuc['banner']}\n")
        cikti.write("\n" + IMZA + "\n")

def main():
    logo_goster()
    parser = argparse.ArgumentParser(
        description="TRJ PortScan - TCP port ve servis keşif aracı",
        epilog="Yalnızca sahibi olduğunuz veya tarama izniniz bulunan sistemlerde kullanın."
    )
    parser.add_argument("hedef", help="IP adresi veya alan adı")
    parser.add_argument("-p", "--portlar", help="Port listesi/range (örn: 22,80,443 veya 1-1024)")
    parser.add_argument("--tum-portlar", action="store_true", help="1-65535 TCP portlarını kontrol et")
    parser.add_argument("-t", "--zaman-asimi", type=float, default=0.6, help="Bağlantı zaman aşımı (varsayılan: 0.6 sn)")
    parser.add_argument("-w", "--isci", type=int, default=60, help="Eş zamanlı bağlantı sayısı (1-100)")
    parser.add_argument("-b", "--banner", action="store_true", help="Açık portlarda banner okumayı dene (veri göndermez)")
    parser.add_argument("-o", "--rapor", help="Sonuçları metin dosyasına kaydet")
    args = parser.parse_args()

    if args.zaman_asimi <= 0:
        parser.error("Zaman aşımı 0'dan büyük olmalı.")
    if not 1 <= args.isci <= 100:
        parser.error("İşçi sayısı 1-100 arasında olmalı.")

    try:
        hedef_ip = socket.gethostbyname(args.hedef)
    except socket.gaierror:
        print(Fore.RED + f"[!] Hedef çözümlenemedi: {args.hedef}")
        return 1

    if args.tum_portlar:
        portlar = list(range(1, 65536))
    elif args.portlar:
        try:
            portlar = port_listesi_coz(args.portlar)
        except ValueError as hata:
            parser.error(str(hata))
    else:
        portlar = SIK_KULLANILAN_PORTLAR

    print(Fore.WHITE + f"  Hedef : {args.hedef} ({hedef_ip})")
    print(f"  Port  : {len(portlar)} port kontrol edilecek")
    print(f"  Zaman : {args.zaman_asimi} saniye | Eş zamanlı: {args.isci}")
    print(Fore.YELLOW + "\n[*] Kontrol başladı...\n")

    sonuclar = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.isci) as havuz:
        gorevler = [havuz.submit(port_kontrol, hedef_ip, port, args.zaman_asimi, args.banner) for port in portlar]
        tamamlanan = 0
        for gorev in concurrent.futures.as_completed(gorevler):
            sonuc = gorev.result()
            sonuclar.append(sonuc)
            tamamlanan += 1
            if sonuc["durum"] == "AÇIK":
                satir = f"[+] {sonuc['port']}/tcp  {sonuc['servis']:<18} AÇIK"
                print(Fore.GREEN + satir)
                if sonuc["banner"]:
                    print(Fore.WHITE + f"    Banner: {sonuc['banner'][:100]}")
            elif tamamlanan % max(1, len(portlar) // 10) == 0:
                print(Fore.WHITE + f"[*] İlerleme: {tamamlanan}/{len(portlar)}")

    sonuclar.sort(key=lambda item: item["port"])
    acik_portlar = [sonuc for sonuc in sonuclar if sonuc["durum"] == "AÇIK"]
    print(Fore.CYAN + "\n" + "-" * 54)
    print(Fore.WHITE + Style.BRIGHT + "TARAMA TAMAMLANDI")
    print(f"  Kontrol edilen : {len(portlar)}")
    print(f"  Açık port     : {len(acik_portlar)}")
    print(f"  Hedef IP      : {hedef_ip}")
    print(Fore.CYAN + "-" * 54)
    if not acik_portlar:
        print(Fore.YELLOW + "Açık port tespit edilmedi.")
    print(Fore.WHITE + f"\n{IMZA}")

    if args.rapor:
        try:
            rapor_kaydet(args.rapor, args.hedef, hedef_ip, sonuclar)
            print(Fore.GREEN + f"[✓] Rapor kaydedildi: {args.rapor}")
        except OSError as hata:
            print(Fore.RED + f"[!] Rapor yazılamadı: {hata}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
