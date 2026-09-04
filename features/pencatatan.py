from db import get_db_connection

def get_kategori_transaksi():
    return {
        "pemasukan": ["Gaji", "Bonus", "Transfer", "Lainnya"],
        "pengeluaran": ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan", "Lainnya"]
    }

def simpan_transaksi_baru(tipe, nominal, kategori, catatan):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO transaksi (tipe, nominal, kategori, catatan)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (tipe, nominal, kategori, catatan))
    
    conn.commit()
    cursor.close()
    conn.close()