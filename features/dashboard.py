from db import get_db_connection

def get_ringkasan_keuangan():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Hitung Total Pemasukan
    cursor.execute("SELECT COALESCE(SUM(nominal), 0) AS total FROM transaksi WHERE tipe = 'pemasukan'")
    total_pemasukan = cursor.fetchone()['total']

    # 2. Hitung Total Pengeluaran
    cursor.execute("SELECT COALESCE(SUM(nominal), 0) AS total FROM transaksi WHERE tipe = 'pengeluaran'")
    total_pengeluaran = cursor.fetchone()['total']

    # 3. Sisa Saldo
    sisa_saldo = float(total_pemasukan) - float(total_pengeluaran)

    # 4. Ambil 10 Riwayat Transaksi Terbaru
    cursor.execute("""
        SELECT id, TO_CHAR(tanggal, 'YYYY-MM-DD') as tanggal, tipe, nominal, kategori, catatan 
        FROM transaksi 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    riwayat = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran,
        "sisa_saldo": sisa_saldo,
        "riwayat": riwayat
    }