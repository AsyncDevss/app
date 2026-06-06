# Tek Dosyalık Siber Güvenlik Laboratuvarı (WAF/IDS Simülasyonu) 🛡️

Bu proje, Python ve Flask kullanılarak geliştirilmiş, siber güvenlik eğitimlerinde girdi doğrulama (input validation) ve imza tabanlı saldırı tespiti (IDS) mantığını anlamak için tasarlanmış tek dosyalık bir simülasyon ortamıdır.

## Özellikler
- SQL Injection ve XSS saldırılarına karşı mini IDS koruması.
- Şüpheli aktivitelerin `security_alerts.log` dosyasına anlık kaydedilmesi.

## Çalıştırma
```bash
pip install flask
python app.py
