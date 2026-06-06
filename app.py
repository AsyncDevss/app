import os
import re
import logging
from flask import Flask, request, render_template_string

LOG_FILE = "security_alerts.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - [ALARM] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def detect_attack(user_input, ip_address):
    """Basit bir İmza Tabanlı Saldırı Tespit Sistemi (IDS)"""
    sqli_patterns = [r"UNION\s+SELECT", r"'\sOR\s'\d+'\s=\s'\d+", r"admin'\s*--"]
    xss_patterns = [r"<script>", r"javascript:", r"onerror="]


    for pattern in sqli_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            logging.info(f"SQL Injection Girişimi Engellendi! IP: {ip_address} | Girdi: {user_input}")
            return "SQL Injection Saldırısı Tespit Edildi!"


    for pattern in xss_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            logging.info(f"XSS Girişimi Engellendi! IP: {ip_address} | Girdi: {user_input}")
            return "XSS Saldırısı Tespit Edildi!"
return None

app = Flask(name)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Siber Güvenlik Test Laboratuvarı</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }
        .container { max-width: 600px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        input[type="submit"] { background-color: #007BFF; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        .alert { padding: 10px; margin-top: 20px; border-radius: 4px; background-color: #ffcccc; color: #cc0000; font-weight: bold; }
        .success { padding: 10px; margin-top: 20px; border-radius: 4px; background-color: #d4edda; color: #155724; }
        footer { margin-top: 30px; font-size: 0.8em; color: #777; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Mini Siber Güvenlik Labı (IDS & WAF Simülasyonu)</h2>
        <p>Aşağıdaki kutuya arama terimi girerek sistemi test edin (Örn: <code>' OR '1'='1</code> veya <code>&lt;script&gt;</code>):</p>

        <form method="POST">
            <input type="text" name="search_query" placeholder="Bir şeyler arayın..." required>
            <input type="submit" value="Sorgula">
        </form>

        {% if alert %}
            <div class="alert">{{ alert }}</div>
        {% elif result %}
            <div class="success">Güvenli Girdi Alındı: {{ result }}</div>
        {% endif %}
    </div>
    <footer>Enes tarafından yapılmıştır.</footer>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    alert = None
    result = None

    if request.method == "POST":
        user_input = request.form.get("search_query", "")
        ip_address = request.remote_addr

        attack_detected = detect_attack(user_input, ip_address)

        if attack_detected:
            alert = f"⚠️ {attack_detected} Log dosyasına (security_alerts.log) kaydedildi."
        else:
            result = user_input

    return render_template_string(HTML_TEMPLATE, alert=alert, result=result)

if name == "main":
    print("[] Siber güvenlik laboratuvarı başlatılıyor...")
    print(f"[] Saldırı logları '{LOG_FILE}' dosyasına yazılacak.")
    app.run(debug=True, port=5000)
