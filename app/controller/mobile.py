from flask import Blueprint, render_template
from app.models.models import Pelanggan, Log_pelanggan

mobile = Blueprint('mobile', __name__)

@mobile.route('/m/pelanggan/<id_pelanggan>', methods=['GET', 'POST'])
def m_pelanggan(id_pelanggan=None):
    pelanggan = Pelanggan.query.all()

    if id_pelanggan:
        purchase_history_data = Log_pelanggan.query.filter_by(id_pelanggan=id_pelanggan).order_by(Log_pelanggan.id_log_pelanggan.desc()).all()
        data = Pelanggan.query.filter_by(id_pelanggan=id_pelanggan).first()

        formatted_data = [
            {"aroma": log.penjualan.aroma.nama, "pabrik": log.penjualan.pabrik.nama, "date": log.penjualan.date, "qty": log.penjualan.qty, "harga": log.penjualan.harga} 
            for log in purchase_history_data
        ]

        if purchase_history_data:
            created = purchase_history_data[0].pelanggan.created_at.strftime('%Y-%m-%d')
        else:
            created = data.created_at.strftime('%Y-%m-%d')

        return render_template('mobile/pelanggan.html', purchase_history_nav = 'active',
                        purchase_history_data = formatted_data, created = created, data = data)

    return render_template('mobile/pelanggan.html', pelanggan = pelanggan)