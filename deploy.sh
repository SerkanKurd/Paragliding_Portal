#!/bin/bash

# 1. Hataları durdur (Herhangi bir adım hata verirse süreci durdurur)
set -e

echo "🚀 Yerel dağıtım süreci başlıyor..."

# 2. Tailwind CSS'i yerelde derle
echo "🎨 Tailwind CSS derleniyor..."
cd theme/static_src/
npm run build
cd ../..

# 3. Docker imajlarını derle ve ayağa kaldır
# --build: Kod değişikliklerini algılar ve yerel imajı günceller
# -d: Konteynerları arka planda çalıştırır
echo "🐳 Docker konteynerları yerelde paketleniyor ve başlatılıyor..."
docker compose up --build -d

# 4. Gereksiz/Eski imajları temizle (Disk alanını korumak için)
echo "🧹 Eski ve askıda kalan Docker imajları temizleniyor..."
docker image prune -f

echo "✅ İşlem başarıyla tamamlandı!"
echo "🌐 Uygulama yerelde çalışıyor: http://localhost"