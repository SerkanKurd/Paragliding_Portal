# Paragliding Portal – Güvenlik ve Geliştirme Yol Haritası

_Hazırlanma: 2026-11-24 · Güncelleme: 2026-11-24 · Proje sürümü 0.3.1 · Django 6.1.3 / Python 3.14_

## Mevcut durum özeti

- **Uygulamalar:** `pages` (araçlar: vario simülatörü, IGC→Excel, 3D uçuş, ağırlık kontrolü, signup/profil), `blog` (çevrilmiş yazılar), `paragliding` (Pilot, FlightData, Wing, Harness, Reserve modelleri).
- **Stack:** Django + HTMX + Tailwind/daisyUI, PostgreSQL, gunicorn, nginx, Docker → GHCR (GitHub Actions).
- **Sağlık:** 13 test geçiyor, `ruff` temiz, `pip-audit` ve `npm audit` bilinen açık bulmadı.

## Kararlar ve ortam bilgisi

- **Site canlıda, kullanıcı yok** → `SECRET_KEY` yenilemek ve oturumları sıfırlamak sorun değil.
- **HTTPS Cloudflare'de sonlanıyor** → HTTP→HTTPS yönlendirmesi Cloudflare'de ("Always Use HTTPS") yapılır, Django'da `SECURE_SSL_REDIRECT` kapalı kalır (yönlendirme döngüsü riski). nginx, Cloudflare'in `X-Forwarded-Proto` başlığını olduğu gibi iletmeli; gerçek istemci IP'si `CF-Connecting-IP`'de.
- **Deploy:** `main`'e push → GitHub Actions imajı derleyip GHCR'a gönderiyor. Yeni ortam değişkenleri sunucudaki `.env`'e **deploy'dan önce** eklenmeli.
- **Yaklaşım: en az değişiklik.** Yeni bağımlılık yerine mevcut araçlar (Django ayarları, nginx, Cloudflare) tercih edilir.
- Signup tasarımı ve hesaplayıcı araçları güvenlik fazlarından sonraya ertelendi.

## Uygulama sırası

Faz 0 → Faz 1 (CI) → Faz 2 → Faz 3 → Faz 4 → Faz 5

---

## Faz 0 – Acil güvenlik düzeltmeleri

| # | Sorun | Nerede | Yapılacak |
|---|-------|--------|-----------|
| 0.1 | `SECRET_KEY` için repoya gömülü varsayılan değer (git geçmişinde de var) | `core/settings.py:33` | DEBUG kapalıyken env yoksa uygulama başlamasın; Dockerfile'daki `collectstatic` adımına geçici build anahtarı ver; sunucuda **yeni anahtar** üret |
| 0.2 | `django_browser_reload` prod'da da yüklü: app, middleware ve `/__reload__/` URL'i | `settings.py`, `core/urls.py` | Yalnızca `DEBUG=True` iken ekle |
| 0.3 | HTTPS sertleştirme eksik | `settings.py`, `nginx/default.conf`, Cloudflare | `SECURE_REFERRER_POLICY`, `SECURE_CROSS_ORIGIN_OPENER_POLICY`; HSTS kısa süreyle başlat (Django ya da Cloudflare'de, tek yerde); nginx'te `X-Forwarded-Proto`'yu Cloudflare'den ilet; W008'i bilinçli olarak sustur |
| 0.4 | Kullanıcıya ham exception mesajı gösteriliyor (`str(e)`) | `pages/views.py` | Genel mesaj göster, detayı logla |
| 0.5 | `Content-Disposition` başlığında kullanıcı dosya adı doğrudan kullanılıyor | `pages/views.py` | `django.utils.http.content_disposition_header` kullan |
| 0.6 | Upload sınırları tutarsız (nginx 20M, uygulama 10M) | `nginx/default.conf`, `settings.py` | nginx 10M, Django upload ayarları |

## Faz 1 – CI güvenlik ağı

| # | Konu | Yapılacak |
|---|------|-----------|
| 1.1 | CI test/lint çalıştırmadan imaj basıyor; PR'larda da push ediyor | Önce `ruff` + `test` + `check --deploy`; push sadece `main`'de |
| 1.2 | Bağımlılık taraması yok | CI'a `pip-audit` + Dependabot (uv, npm, actions, docker) |
| 1.3 | Action'lar sürüm tag'iyle | SHA'ya sabitle (Dependabot günceller) |

## Faz 2 – Kimlik doğrulama ve tarayıcı güvenliği

| # | Konu | Yapılacak |
|---|------|-----------|
| 2.1 | Login brute-force koruması yok | nginx `limit_req` (`CF-Connecting-IP` anahtarıyla) login ve upload uçlarında; ek olarak Cloudflare rate limiting kuralı (ücretsiz planda 1 kural) |
| 2.2 | Admin varsayılan `/admin/` yolunda | Admin yolunu env'den al; istenirse Cloudflare Access ile /admin/ koruması (kod değişikliği yok) |
| 2.3 | CSP yok; inline script'ler var | Django 6 yerleşik CSP: önce report-only, sonra zorunlu |
| 2.4 | `{{ flight_points\|safe }}` ile JS içine veri basılıyor | `json_script` filtresine geç |
| 2.5 | Harici script'ler SRI'sız ve eski: htmx 1.9.10, Cesium 1.114 | Sürüm sabitle + `integrity`; htmx 2.x geçişi ayrı test edilmeli |
| 2.6 | Cesium ion token istemciye açık (kaçınılmaz) | Cesium ion panelinde token'ı alan adına kısıtla |

## Faz 3 – Altyapı

| # | Konu | Yapılacak |
|---|------|-----------|
| 3.1 | Container root çalışıyor, `uv:latest` sabit değil, dev bağımlılıkları kuruluyor | Non-root kullanıcı, uv sürümü sabit, `--no-dev`, gunicorn worker/timeout |
| 3.2 | `.dockerignore`'da `.venv`, `.ruff_cache`, `.github` yok | Ekle |
| 3.3 | Gereksiz/ölü kod: `cookiecutter` bağımlılığı, `pages/utilities/translate.py`, `main.py` | Kaldır |
| 3.4 | nginx'te `server_tokens off` yok; statikler `no-cache` | Ekle; hash'li statiklere uzun cache |

## Faz 4 – Kod kalitesi ve hatalar

| # | Konu | Yapılacak |
|---|------|-----------|
| 4.1 | `weight_control/` URL'i iki kez tanımlı | Düzelt |
| 4.2 | Menüde `/settings/` ve "Ayarlar" kırık linkler | Kaldır veya sayfa ekle |
| 4.3 | `APP_VERSION` her açılışta `uv version` subprocess'i çalıştırıyor | `importlib.metadata.version()` |
| 4.4 | IGC parser kırılgan (HFDTE/PILOT yoksa, kısa B satırları) | Sağlamlaştır + birim testleri |
| 4.5 | Testler SQLite, prod PostgreSQL | CI'da Postgres service |
| 4.6 | `LOGGING` yapılandırması yok | Konsol logging |
| 4.7 | Admin'de `Post`, `Harness`, `Reserve` kayıtlı değil | Kaydet |
| 4.8 | Her view'da tekrar eden "HX-Request → partial" mantığı | Ortak yardımcı / `request.htmx` |

## Faz 5 – Sonraki aşamalar (ertelendi)

1. **Signup sayfası tasarımı ve politikası:** e-posta doğrulama, bot koruması (Cloudflare Turnstile), açık/kapalı kayıt kararı
2. **Hesaplayıcılar:** L/D süzülme, bulut tabanı
3. Ekipman logbook'u (kanat/yedek/harness muayene tarihleri)
4. Yedek katlama hatırlatıcısı (e-posta → SMTP ayarları gerekir)
5. Kalkış alanı rehberi
6. THK sınav deneme modülü

Kullanıcı verisi içeren özelliklerde nesne düzeyi yetki kontrolü (`Pilot.manager`) ve KVKK değerlendirmesi şart.

---

## Çalışma şekli

Her madde ayrı, küçük bir değişiklik olarak yapılır → testler + `check --deploy` çalıştırılır → onayınla commit.
