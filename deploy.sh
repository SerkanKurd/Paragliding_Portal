#!/bin/bash

# 1. Hataları durdur (Herhangi bir adım hata verirse süreci durdurur)
set -e

echo "🚀 Dağıtım süreci başlıyor..."

# 2. Tailwind CSS'i yerelde derle (Node.js/NPM senin Mac'inde çalışır)
echo "🎨 Tailwind CSS derleniyor..."
cd theme/static_src/
npm run build
cd ../..

# 3. Docker imajlarını derle ve ayağa kaldır
# --build: Kod değişikliklerini algılar
# -d: Arka planda çalıştırır
echo "🐳 Docker konteynerları paketleniyor ve başlatılıyor..."
docker compose up --build -d

# 4. Gereksiz/Eski imajları temizle (Disk alanını korumak için)
echo "🧹 Eski Docker imajları temizleniyor..."
docker image prune -f

echo "✅ İşlem tamamlandı! Uygulama http://localhost adresinde yayında."

# 5. Docker Hub'a imajı gönder (Opsiyonel)
docker tag paragliding_portal-web serkankurd/paragliding-portal:latest
docker push serkankurd/paragliding-portal:latest