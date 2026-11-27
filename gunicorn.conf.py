"""Gunicorn ayarları.

Gunicorn çalışma dizinindeki bu dosyayı otomatik okur; bu yüzden sunucudaki
docker-compose 'command' satırı değişmeden de geçerlidir. Komut satırında verilen
seçenekler (ör. --bind) buradakileri ezer.
"""

import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

# Varsayılan 1 worker yerine birkaç worker: bir istek uzun sürerken (ör. büyük
# IGC dosyası) diğer istekler beklemesin.
workers = int(os.environ.get("GUNICORN_WORKERS", "3"))

# IGC → Excel dönüşümü büyük dosyalarda varsayılan 30 sn'yi aşabilir.
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30

# Bellek sızıntılarına karşı worker'ları belirli aralıklarla yenile.
max_requests = 1000
max_requests_jitter = 100

# Docker'da heartbeat dosyaları için bellek içi dizin.
worker_tmp_dir = "/dev/shm"

# Erişim ve hata logları container loglarına (docker logs) gitsin.
accesslog = "-"
errorlog = "-"
