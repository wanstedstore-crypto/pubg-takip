import requests
from bs4 import BeautifulSoup
import time

# --- AYARLAR ---
BOT_TOKEN = "8845086700:AAG7H-aA2y9uVDBaFmGq_tDDdXNxGQ_0vrU"
CHAT_ID = "7980506594"

# --- TÜM SİTELERİN TAKİP LİNKLERİ ---
SITELER = {
    "KABASAKAL": "https://www.kabasakalonline.com/ilanlar/pubg-mobile-hesap-satisi",
    "GAMESATIŞ": "https://www.gamesatis.com/pubg-mobile-hesap-satisi",
    "İTEMSATIŞ": "https://www.itemsatis.com/ilanlar/pubg-mobile-hesap-satisi.html",
    "HESAP.COM": "https://hesap.com/pubg-mobile-hesap-satisi",
    "BYNOGAME": "https://www.bynogame.com/tr/oyunlar/pubg-mobile/hesap-satisi",
    "OYUNEKS": "https://oyuneks.com/pazar/pubg-mobile-hesap-satisi"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fırsat olarak kabul edilecek anahtar kelimeler
FIRSAT_KELIMELERI = ["acil", "kelepir", "ucuz", "fırsat", "firsat", "buz diyarı", "buz diyari", "m416", "kelepir", "bedava"]

bilinen_ilanlar = set()

def telegram_mesaj_gonder(mesaj):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "Markdown"}
    try: requests.post(telegram_url, data=data)
    except: pass

def siteleri_tara():
    for site_adi, url in SITELER.items():
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200: continue
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if site_adi == "KABASAKAL":
                ilanlar = soup.find_all('div', class_='listing-card')
                for ilan in ilanlar:
                    i_id = "kabasakal_" + str(ilan.get('data-id'))
                    i_baslik = ilan.find('h3').text.strip() if ilan.find('h3') else "PUBG Hesabı"
                    i_fiyat = ilan.find('span', class_='price').text.strip() if ilan.find('span', class_='price') else "Bilinmiyor"
                    i_link = "https://www.kabasakalonline.com" + ilan.find('a')['href']
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)
                    
            elif site_adi == "GAMESATIŞ":
                ilanlar = soup.find_all('div', class_='cs-item')
                for ilan in ilanlar:
                    link = ilan.find('a')
                    if not link: continue
                    i_link = "https://www.gamesatis.com" + link['href']
                    i_id = "gamesatis_" + i_link.split('-')[-1]
                    i_baslik = ilan.find('h3').text.strip() if ilan.find('h3') else "PUBG Hesabı"
                    i_fiyat = ilan.find('div', class_='item-price').text.strip() if ilan.find('div', class_='item-price') else "Bilinmiyor"
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)

            elif site_adi == "İTEMSATIŞ":
                ilanlar = soup.find_all('div', class_='post-row')
                for ilan in ilanlar:
                    link = ilan.find('a')
                    if not link: continue
                    i_link = "https://www.itemsatis.com" + link['href']
                    i_id = "itemsatis_" + i_link.split('-')[-1].replace('.html', '')
                    i_baslik = ilan.find('h2').text.strip() if ilan.find('h2') else "PUBG Hesabı"
                    i_fiyat = ilan.find('div', class_='price').text.strip() if ilan.find('div', class_='price') else "Bilinmiyor"
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)

            elif site_adi == "HESAP.COM":
                ilanlar = soup.find_all('div', class_='product-box')
                for ilan in ilanlar:
                    link = ilan.find('a')
                    if not link: continue
                    i_link = link['href']
                    i_id = "hesapcom_" + i_link.split('/')[-1]
                    i_baslik = ilan.find('h3').text.strip() if ilan.find('h3') else "PUBG Hesabı"
                    i_fiyat = ilan.find('div', class_='price-box').text.strip() if ilan.find('div', class_='price-box') else "Bilinmiyor"
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)

            elif site_adi == "BYNOGAME":
                ilanlar = soup.find_all('div', class_='card') or soup.find_all('div', class_='product-item')
                for ilan in ilanlar:
                    link = ilan.find('a')
                    if not link: continue
                    i_link = "https://www.bynogame.com" + link['href'] if not link['href'].startswith('http') else link['href']
                    i_id = "bynogame_" + i_link.split('/')[-1]
                    i_baslik = ilan.find('h5').text.strip() if ilan.find('h5') else "PUBG Hesabı"
                    i_fiyat = ilan.find('span', class_='price').text.strip() if ilan.find('span', class_='price') else "Bilinmiyor"
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)

            elif site_adi == "OYUNEKS":
                ilanlar = soup.find_all('div', class_='product-card')
                for ilan in ilanlar:
                    link = ilan.find('a')
                    if not link: continue
                    i_link = link['href']
                    i_id = "oyuneks_" + i_link.split('/')[-1]
                    i_baslik = ilan.find('div', class_='title').text.strip() if ilan.find('div', class_='title') else "PUBG Hesabı"
                    i_fiyat = ilan.find('div', class_='price').text.strip() if ilan.find('div', class_='price') else "Bilinmiyor"
                    bildirim_gonder(i_id, site_adi, i_baslik, i_fiyat, i_link)
        except:
            pass

def bildirim_gonder(ilan_id, site, baslik, fiyat, link):
    if ilan_id not in bilinen_ilanlar:
        bilinen_ilanlar.add(ilan_id)
        
        # Hafıza dolduktan sonra bildirim tetiklensin
        if len(bilinen_ilanlar) > 50:
            # Başlıkta fırsat kelimelerinden biri geçiyor mu kontrol et
            baslik_kucuk = baslik.lower()
            is_firsat = any(kelime in baslik_kucuk for kelime in FIRSAT_KELIMELERI)
            
            if is_firsat:
                mesaj = f"🔥 *{site} - KAÇIRMA FIRSAT İLAN!* 🔥\n\n📝 *Başlık:* {baslik}\n💰 *Fiyat:* {fiyat}\n🔗 [Hemen İlana Git]({link})"
            else:
                mesaj = f"ℹ️ *{site} - Yeni İlan:* \n📝 {baslik}\n💰 Fiyat: {fiyat}\n🔗 [İlana Git]({link})"
                
            telegram_mesaj_gonder(mesaj)

print("Fırsat filtreli dev PUBG takip botu aktif...")
telegram_mesaj_gonder("🤖 Fırsat Filtreli Dev PUBG Botu Başlatıldı! Kelepir ve Buz Diyarı hesaplar '🔥' etiketiyle gelecek.")

while True:
    siteleri_tara()
    time.sleep(300)
                  
