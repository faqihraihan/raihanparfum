from flask import Blueprint, redirect, url_for

scan = Blueprint('scan', __name__)

@scan.route('/scan/<qrcode>', methods=['POST', 'GET'])
def receive_scan_data(qrcode):
    # Mengambil data dari URL parameter
    qr_data = qrcode
    
    if qr_data.startswith('MEM'):
        return redirect(url_for('mobile.m_pelanggan', id_pelanggan = qr_data))