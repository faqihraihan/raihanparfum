from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import Pelanggan, Log_pelanggan
from datetime import datetime
from sqlalchemy import func

cust = Blueprint('cust', __name__)


@cust.route('/pelanggan', methods=['GET', 'POST'])
def pelanggan():

    pelanggan = db.session.query(Pelanggan).order_by(Pelanggan.id_pelanggan.desc()).limit(20).all()

    return render_template('pelanggan/pelanggan.html', pelanggan_nav = 'active', pelanggan = pelanggan)


@cust.route('/pelanggan/add', methods=['POST'])
def pelanggan_add():
    if request.method == 'POST':
        telp = request.form['telp']

        check_telp = db.session.query(Pelanggan).filter(Pelanggan.telp == telp).first()

        if check_telp:
            flash('No. Hp sudah terdaftar', 'primary')

            return redirect(url_for('cust.purchase_history', id_pelanggan = check_telp.id_pelanggan))
        else:
            nama = request.form['nama']
            alamat = request.form['alamat']

            now = datetime.now()
            year = now.strftime("%y")
            month = now.strftime("%m")

            last_pelanggan = db.session.query(Pelanggan).filter(
                func.strftime('%Y-%m', Pelanggan.created_at) == now.strftime('%Y-%m')
                ).order_by(Pelanggan.id_pelanggan.desc()).first()

            if last_pelanggan:
                last_id_str = last_pelanggan.id_pelanggan[-5:]
                last_id_number = int(last_id_str)
                new_id_number = last_id_number + 1
            else:
                new_id_number = 10001

            id_pelanggan = f"MEM{year}{month}{new_id_number}"

            data = Pelanggan(id_pelanggan = id_pelanggan,
                                nama = nama,
                                telp = telp,
                                alamat = alamat)

            db.session.add(data)
            db.session.commit()
            flash('Data berhasil ditambahkan', 'success')

            return redirect(url_for('cust.pelanggan'))


@cust.route("/pelanggan/edit", methods=['GET', 'POST'])
def pelanggan_edit():
    if request.method == 'POST':
        update = Pelanggan.query.get(request.form.get('id_pelanggan'))
        update.nama = request.form['nama']
        telp = request.form['telp']
        update.alamat = request.form['alamat']

        check_telp = db.session.query(Pelanggan).filter(Pelanggan.telp == telp).first()

        if check_telp:
            flash('No. Hp sudah terdaftar', 'primary')

            return redirect(url_for('cust.purchase_history', id_pelanggan = check_telp.id_pelanggan))
        else:
            update.telp = telp

            db.session.commit()
            flash("Data berhasil diubah", 'success')

        return redirect(url_for('cust.pelanggan'))


@cust.route("/pelanggan/delete", methods=['GET', 'POST'])
def pelanggan_delete():
    id_pelanggan = request.form['id_pelanggan']
    delete = Pelanggan.query.get(id_pelanggan)
    
    delete_log_pelanggan = Log_pelanggan.query.filter_by(id_pelanggan = id_pelanggan).all()

    db.session.delete(delete)
    for data in delete_log_pelanggan:
        db.session.delete(data)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('cust.pelanggan'))


@cust.route('/pelanggan/purchase_history/<id_pelanggan>', methods=['GET', 'POST'])
@cust.route('/pelanggan/purchase_history', methods=['GET', 'POST'])
def purchase_history(id_pelanggan=None):
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

        return render_template('pelanggan/purchase-history.html', purchase_history_nav = 'active',
                           purchase_history_data = formatted_data, created = created, data = data)

    return render_template('pelanggan/purchase-history-search.html', purchase_history_nav = 'active', pelanggan = pelanggan)