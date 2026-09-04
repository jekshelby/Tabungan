import re
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

def olah_gambar_struk(image_file):
    """
    Pre-processing gambar agar kontras tinggi dan mudah dibaca OCR.
    """
    img = Image.open(image_file)
    
    # 1. Konversi ke Grayscale (Hitam Putih)
    img = img.convert('L')
    
    # 2. Tingkatkan Kontras Teks
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # 3. Penajaman Gambar (Sharpen)
    img = img.filter(ImageFilter.SHARPEN)
    
    return img

def ekstraksi_total_struk(image_file):
    try:
        # Pre-process gambar
        img = olah_gambar_struk(image_file)
        
        # Ekstrak teks menggunakan Tesseract Python (Bahasa Indonesia + Inggris)
        teks = pytesseract.image_to_string(img, lang='ind+eng')
        print("--- TEKS STRUK TERBACA SERVER ---")
        print(teks)
        print("---------------------------------")
        
        baris_list = teks.upper().split('\n')
        nominal_ditemukan = None

        # Prioritas 1: Cari kata kunci Total / Bayar / Jumlah
        for baris in baris_list:
            if any(kw in baris for kw in ["TOTAL", "JUMLAH", "BAYAR", "GRAND TOTAL", "NET"]):
                # Ambil hanya deretan angka
                angka_list = re.findall(r'\d+', baris)
                if angka_list:
                    gabung_angka = int("".join(angka_list))
                    if gabung_angka >= 500:  # Abaikan nominal terlalu kecil
                        nominal_ditemukan = gabung_angka
                        break

        # Prioritas 2: Jika tidak ada kata kunci, ambil angka terbesar di struk
        if not nominal_ditemukan:
            semua_angka = re.findall(r'\b\d{4,8}\b', teks)
            if semua_angka:
                daftar = [int(n) for n in semua_angka if int(n) >= 1000]
                if daftar:
                    nominal_ditemukan = max(daftar)

        return nominal_ditemukan or 0

    except Exception as e:
        print(f"Error OCR Server: {e}")
        return 0