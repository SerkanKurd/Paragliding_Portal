from googletrans import Translator

def translate_agent():
    # 1. Veri Tabanı Bağlantısı
    conn = sqlite3.connect('veriler.db')
    cursor = conn.cursor()
    translator = Translator()

    # 2. Çevrilmemiş verileri seç (Örn: 'tr_metin' kolonu boş olanlar)
    cursor.execute("SELECT id, orjinal_metin FROM yazilar WHERE tr_metin IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        row_id, text = row
        print(f"Çevriliyor: {text[:30]}...")

        try:
            # 3. Çeviri İşlemi
            translation = translator.translate(text, dest='tr')
            translated_text = translation.text

            # 4. Veri Tabanını Güncelle
            cursor.execute(
                "UPDATE yazilar SET tr_metin = ? WHERE id = ?", 
                (translated_text, row_id)
            )
            conn.commit()
            print(f"ID {row_id} başarıyla güncellendi.")
            
        except Exception as e:
            print(f"Hata oluştu: {e}")

    conn.close()

if __name__ == "__main__":
    translate_agent()