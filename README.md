# 🛡️ TRJ DomainSpy

<div align="center">

### TRJ Siber Güvenlik Araçları
**Domain keşfi • TCP port kontrolü • Servis tespiti**

</div>

---

> Kendi sistemlerinizi veya test için açıkça izin aldığınız hedefleri analiz etmek amacıyla geliştirilmiştir.

## 🔎 Port & Servis Keşfi — TRJ PortScan

TRJ PortScan, hedef sistemde seçilen TCP portlarına bağlantı kurmayı deneyerek açık portları belirler. Port numarasına göre olası servis adını gösterir. İstenirse bağlantı kurulan servislerden pasif şekilde kısa bir banner okunmaya çalışılır; tarayıcı servislerine herhangi bir test isteği veya payload gönderilmez.

### Özellikler

- ⚡ Eş zamanlı TCP bağlantı kontrolü
- 🎯 Yaygın portlar hazır listesi
- 🧩 Tek port, virgülle port listesi ve aralık desteği
- 🗂️ İsteğe bağlı tüm TCP portlarını kontrol etme
- 🏷️ Port numarasına göre servis adı gösterme
- 📡 İsteğe bağlı banner okuma (veri göndermez)
- 📝 Sonuçları TXT raporuna kaydetme
- 🖥️ Windows, Linux ve macOS terminal desteği
- 🇹🇷 Türkçe menüler ve terminal çıktısı

### Kurulum

Python 3.9 veya üzeri gerekir. Renkli terminal için Colorama kullanılır; Colorama olmadan da çalışır.

```bash
git clone https://github.com/SanaldunyaDONKISOTU/TRJ-DomainSpy.git
cd TRJ-DomainSpy
python -m pip install colorama
```

### Kullanım

**Yaygın portları kontrol et:**
```bash
python trj_portscan.py 192.168.1.1
```

**Belirli portlar:**
```bash
python trj_portscan.py 192.168.1.1 -p 22,80,443,8080
```

**Port aralığı:**
```bash
python trj_portscan.py 192.168.1.1 -p 1-1024
```

**Tam TCP port aralığı:**
```bash
python trj_portscan.py 192.168.1.1 --tum-portlar
```

**Banner okumayı dene ve rapor kaydet:**
```bash
python trj_portscan.py hedef.local -p 21,22,25,80,443 -b -o tarama_raporu.txt
```

**Bağlantı süresi ve eş zamanlılık ayarı:**
```bash
python trj_portscan.py hedef.local -p 1-1000 -t 1 -w 40
```

| Parametre | Açıklama |
|---|---|
| `-p, --portlar` | Port, liste veya aralık belirt |
| `--tum-portlar` | 1–65535 aralığını kontrol et |
| `-t, --zaman-asimi` | Bağlantı zaman aşımı (saniye) |
| `-w, --isci` | Eş zamanlı bağlantı sayısı (1–100) |
| `-b, --banner` | Açık portta kısa banner okumayı dene |
| `-o, --rapor` | TXT rapor dosyasının yolu |

## ⚠️ Kullanım Sorumluluğu

Bu araç yalnızca izinli güvenlik kontrolleri ve eğitim ortamları için kullanılmalıdır. İzinsiz tarama yapmayın. Açık görünmeyen portlar kapalı olduğu anlamına gelmeyebilir; güvenlik duvarı veya ağ filtreleri bağlantıyı engelliyor olabilir. Servis adı port numarasından tahmin edilir, kesin servis tespiti değildir.

---

<div align="center">

**TRJ** · *Siber güvenlik araçları ve öğrenme projeleri*

</div>
