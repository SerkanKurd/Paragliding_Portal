#!/bin/sh
# Container açılışında çalışır, ardından verilen komutu (gunicorn) başlatır.
set -e

# static_volume yalnızca ilk oluşturulduğunda imajdan doldurulur; sonraki imaj
# güncellemelerinde eski dosyalar kalır. Her açılışta yeniden toplayarak yeni
# CSS/JS dosyalarının siteye yansımasını sağlıyoruz.
if [ "${SKIP_COLLECTSTATIC:-0}" != "1" ]; then
    if ! python manage.py collectstatic --no-input --verbosity 0; then
        echo "UYARI: collectstatic başarısız oldu (static volume bu kullanıcı için yazılabilir değil olabilir)." >&2
        echo "UYARI: Uygulama mevcut statik dosyalarla başlatılıyor." >&2
    fi
fi

exec "$@"
