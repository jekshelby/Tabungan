from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from features.dashboard import get_ringkasan_keuangan, get_semua_riwayat
from features.pencatatan import get_kategori_transaksi, simpan_transaksi_baru
from features.ocr import ekstraksi_total_struk

app = Flask(__name__)

@app.route('/')
def index():
    data_dashboard = get_ringkasan_keuangan()
    return render_template('dashboard.html', data=data_dashboard)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_transaksi():
    if request.method == 'POST':
        tipe = request.form.get('tipe')
        nominal = request.form.get('nominal')
        kategori = request.form.get('kategori')
        catatan = request.form.get('catatan')

        simpan_transaksi_baru(tipe, nominal, kategori, catatan)
        return redirect(url_for('index'))

    kategori = get_kategori_transaksi()
    return render_template('pencatatan.html', kategori=kategori)

@app.route('/transaksi')
def transaksi():
    riwayat_lengkap = get_semua_riwayat()
    return render_template('transaksi.html', riwayat=riwayat_lengkap)

@app.route('/api/scan-ocr', methods=['POST'])
def api_scan_ocr():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Tidak ada file diunggah'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'File kosong'}), 400

    nominal = ekstraksi_total_struk(file)
    return jsonify({
        'success': True,
        'nominal': nominal
    })

@app.route('/scan')
def scan_ocr():
    return render_template('scan.html')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)