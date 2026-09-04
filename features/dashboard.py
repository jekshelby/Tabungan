from db import get_db_connection
from datetime import datetime

# Helper untuk nama hari dan bulan dalam bahasa Indonesia
NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_BULAN = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

def format_tanggal_lengkap(tgl_str):
    try:
        dt = datetime.strptime(tgl_str, '%Y-%m-%d')
        hari = NAMA_HARI[dt.weekday()]
        bulan = NAMA_BULAN[dt.month]
        return f"{hari}, {dt.day} {bulan} {dt.year}"
    except Exception:
        return tgl_str

# --- 1. Fungsi Ringkasan Keuangan untuk Dashboard ---
def get_ringkasan_keuangan():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hitung Total Pemasukan
    cursor.execute("SELECT COALESCE(SUM(nominal), 0) AS total FROM transaksi WHERE tipe = 'pemasukan'")
    total_pemasukan = cursor.fetchone()['total']

    # Hitung Total Pengeluaran
    cursor.execute("SELECT COALESCE(SUM(nominal), 0) AS total FROM transaksi WHERE tipe = 'pengeluaran'")
    total_pengeluaran = cursor.fetchone()['total']

    # Sisa Saldo
    sisa_saldo = float(total_pemasukan) - float(total_pengeluaran)

    # Ambil 3 Riwayat Transaksi Terbaru
    cursor.execute("""
        SELECT id, TO_CHAR(tanggal, 'YYYY-MM-DD') as tanggal, tipe, nominal, kategori, catatan 
        FROM transaksi 
        ORDER BY tanggal DESC, created_at DESC 
        LIMIT 3
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

# --- 2. Fungsi Semua Riwayat Terkelompok untuk Halaman Transaksi ---
def get_semua_riwayat():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, TO_CHAR(tanggal, 'YYYY-MM-DD') as tanggal, tipe, nominal, kategori, catatan 
        FROM transaksi 
        ORDER BY tanggal DESC, created_at DESC
    """)
    semua_data = cursor.fetchall()

    cursor.close()
    conn.close()

    riwayat_grouped = {}
    for item in semua_data:
        tgl_indo = format_tanggal_lengkap(item['tanggal'])
        if tgl_indo not in riwayat_grouped:
            riwayat_grouped[tgl_indo] = {
                "items": [],
                "total_pengeluaran": 0,
                "total_pemasukan": 0
            }
        
        riwayat_grouped[tgl_indo]["items"].append(item)
        
        if item['tipe'] == 'pengeluaran':
            riwayat_grouped[tgl_indo]["total_pengeluaran"] += float(item['nominal'])
        else:
            riwayat_grouped[tgl_indo]["total_pemasukan"] += float(item['nominal'])

    return riwayat_grouped