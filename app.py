from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from features.dashboard import get_ringkasan_keuangan
from features.pencatatan import get_kategori_transaksi, simpan_transaksi_baru

app = Flask(__name__)

@app.route('/')
def index():
    data_dashboard = get_ringkasan_keuangan()
    return render_template('dashboard.html', data=data_dashboard)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_transaksi():
    if request.method == 'POST':
        # Ambil data dari form HTML
        tipe = request.form.get('tipe')
        nominal = request.form.get('nominal')
        kategori = request.form.get('kategori')
        catatan = request.form.get('catatan')

        # Simpan ke Neon PostgreSQL
        simpan_transaksi_baru(tipe, nominal, kategori, catatan)

        # Redirect kembali ke Dashboard setelah berhasil
        return redirect(url_for('index'))

    # Jika akses biasa (GET)
    kategori = get_kategori_transaksi()
    return render_template('pencatatan.html', kategori=kategori)

# Tambahkan ini di app.py
@app.route('/scan')
def scan_ocr():
    return render_template('scan.html')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5000)