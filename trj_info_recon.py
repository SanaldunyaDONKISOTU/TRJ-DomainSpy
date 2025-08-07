import whois
import dns.resolver
import socket
import requests

try:
    import sublist3r
except ImportError:
    print("Sublist3r modülü eksik, kuruyorum...")
    import os
    os.system("pip install sublist3r")
    import sublist3r

try:
    from colorama import init, Fore
    init(autoreset=True)
except ImportError:
    Fore = None

def renkli_yaz(metin, renk="white"):
    if not Fore:
        print(metin)
        return
    renkler = {
        "kirmizi": Fore.RED,
        "yesil": Fore.GREEN,
        "sari": Fore.YELLOW,
        "mavi": Fore.BLUE,
        "beyaz": Fore.WHITE
    }
    print(renkler.get(renk, Fore.WHITE) + metin)

def whois_sorgusu(domain):
    renkli_yaz("\n[+] Whois Sorgusu:", "mavi")
    try:
        bilgi = whois.whois(domain)
        print(bilgi)
    except Exception as e:
        renkli_yaz(f"HATA: {e}", "kirmizi")

def dns_kayitlari(domain):
    renkli_yaz("\n[+] DNS Kayıtları:", "mavi")
    kayit_tipleri = ['A', 'MX', 'NS']
    for kayit in kayit_tipleri:
        try:
            cevap = dns.resolver.resolve(domain, kayit)
            for rdata in cevap:
                print(f"{kayit} Kaydı: {rdata.to_text()}")
        except Exception:
            renkli_yaz(f"{kayit} kaydı bulunamadı.", "sari")

def ip_cozumu(domain):
    renkli_yaz("\n[+] IP Çözümleme:", "mavi")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} IP adresi: {ip}")
    except Exception as e:
        renkli_yaz(f"HATA: {e}", "kirmizi")

def subdomain_taramasi(domain):
    filename = f"{domain}_subdomains.txt"
    print(f"\n[+] Subdomain sonuçları {filename} dosyasına kaydediliyor...\n")

    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        subdomains = set()
        for entry in data:
            names = entry['name_value'].split('\n')
            for name in names:
                if domain in name:
                    subdomains.add(name.strip())

        if subdomains:
            print(f"[+] {len(subdomains)} adet subdomain bulundu:")
            with open(filename, "w") as f:
                for sub in sorted(subdomains):
                    print(f"  └─ {sub}")
                    f.write(sub + "\n")
            print(f"\n[✓] Subdomainler başarıyla '{filename}' dosyasına kaydedildi.")
        else:
            print("[-] Subdomain bulunamadı.")
    except Exception as e:
        print(f"Hata: {e}")


def baslat():
    print("""
████████╗██████╗      ██╗
╚══██╔══╝██╔══██╗     ██║
   ██║   ██████╔╝     ██║
   ██║   ██╔═══╝██   ██║
   ██║   ██║     ╚█████╔╝
   ╚═╝   ╚═╝      ╚════╝
TRJ InfoRecon v2.0 🕵️‍♂️
""")
    domain = input("Hedef Domain: ").strip()
    whois_sorgusu(domain)
    dns_kayitlari(domain)
    ip_cozumu(domain)
    subdomain_taramasi(domain)

if __name__ == "__main__":
    baslat()
