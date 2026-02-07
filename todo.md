Site için araç fikirleri
1.IGC ve Veri Analiz Araçları
• IGC to Excel/CSV Converter: Pilotların uçuş verilerini (irtifa, hız, koordinat) analiz etmek için Excel'e aktarmasını sağlar. Django tarafında pandas kütüphanesi ile bunu kolayca yapabiliriz.
• Uçuş Replay (3D Visualizer): CesiumJS veya Three.js kullanarak IGC dosyasını harita üzerinde 3D oynatmak. (Daha önce konuştuğumuz Doarama alternatifi).
• Vario Bip Sesi Simülatörü: Yeni başlayanlar için farklı yükseliş hızlarında varyonun nasıl ses çıkaracağını gösteren etkileşimli bir araç.
2. Meteoroloji ve Hesaplama Araçları
• Termik Saat Tahmini: Mevcut hava durumuna (sıcaklık, nem, rüzgar) bakarak günün en iyi termik saatlerini tahmin eden bir algoritma.
• L/D (Süzülme) Hesaplayıcı: "Şu irtifadayım, şu kadar rüzgar var, karşıdaki tepeye yetişir miyim?" hesabı yapan bir güvenli süzülme aracı.
• Bulut Tabanı (Cloudbase) Hesaplayıcı: Yer sıcaklığı ve çiğlenme noktasını girerek bulutun tahmini kaç metrede oluşacağını hesaplar.
3. Ekipman ve Güvenlik
• Paraşüt Ömür Takibi (Logbook): Kanat, yedek ve harnesin son muayene tarihlerini ve toplam uçuş saatini takip eden bir panel.
• Yedek Atım Zamanlayıcısı: Yedeğin katlanma zamanı geldiğinde pilota e-posta veya site içi bildirim gönderen bir araç.
• Ağırlık Limit Kontrolü: Pilot ağırlığı + ekipman ağırlığını hesaplayıp, seçilen kanadın (S, M, L) kilo limitlerinin neresinde olduğunu gösteren görsel bir bar.
4. Sosyal ve Eğitim
• Take-off (Kalkış Alanı) Rehberi: Türkiye'deki kalkış alanlarının GPS koordinatları, uygun rüzgar yönleri ve ulaşım bilgileri.
• Sertifika Sınavı Denemeleri: THK P2-P3-P4 sınavlarına hazırlık için online çoktan seçmeli test modülü.