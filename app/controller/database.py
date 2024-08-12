from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models.models import Penjualan, Aroma, Pabrik
from app import db
from datetime import datetime

datab = Blueprint('datab', __name__)

@datab.route('/database/penjualan', methods=['GET', 'POST'])
def penjualan():
    penjualan = db.session.query(Penjualan).order_by(Penjualan.id_penjualan.desc()).limit(10).all()
    pabrik = db.session.query(Pabrik).all()

    return render_template('database/penjualan.html', penjualan_nav = 'active', penjualan = penjualan, pabrik = pabrik)


@datab.route('/database/penjualan/add', methods=['POST'])
def penjualan_add():
    if request.method == 'POST':
        id_pabrik = request.form['pabrik']
        id_aroma = request.form['aroma']
        qty = request.form['qty']
        harga = request.form['harga']
        date = request.form['date']

        date_object = datetime.strptime(date, '%Y-%m-%d')

        data = Penjualan(id_pabrik = id_pabrik,
                     id_aroma = id_aroma,
                     qty = qty,
                     harga = harga,
                     date = date_object)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan')

        return redirect(url_for('datab.penjualan'))


@datab.route("/database/penjualan/edit", methods=['GET', 'POST'])
def penjualan_edit():
    if request.method == 'POST':
        update = Penjualan.query.get(request.form.get('id_penjualan'))

        pabrik = request.form.get('pabrik')
        aroma = request.form.get('aroma')

        if pabrik != None:
            update.id_pabrik = pabrik
        
        if aroma != None:
            update.id_aroma = aroma

        update.qty = request.form['qty']
        update.harga = request.form['harga']

        date = request.form['date']
        date_object = datetime.strptime(date, '%Y-%m-%d')
        update.date = date_object

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('datab.penjualan'))


@datab.route("/database/penjualan/delete", methods=['GET', 'POST'])
def penjualan_delete():
    id_penjualan = request.form['id_penjualan']
    delete = Penjualan.query.get(id_penjualan)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('datab.penjualan'))


@datab.route('/database/aroma', methods=['GET', 'POST'])
def aroma():
    aroma = db.session.query(Aroma).order_by(Aroma.id_aroma.desc()).limit(10).all()
    pabrik = db.session.query(Pabrik).all()

    return render_template('database/aroma.html', aroma_nav = 'active', aroma = aroma, pabrik = pabrik)


@datab.route('/database/aroma/add', methods=['POST'])
def aroma_add():
    if request.method == 'POST':
        nama = request.form['nama']
        id_pabrik = request.form['pabrik']
        harga = request.form['harga']

        data = Aroma(nama = nama,
                     id_pabrik = id_pabrik,
                     harga = harga)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan')

        return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/edit", methods=['GET', 'POST'])
def aroma_edit():
    if request.method == 'POST':
        update = Aroma.query.get(request.form.get('id_aroma'))
        update.nama = request.form['nama']

        pabrik = request.form.get('pabrik')

        if pabrik != None:
            update.id_pabrik = pabrik

        update.harga = request.form['harga']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/delete", methods=['GET', 'POST'])
def aroma_delete():
    id_aroma = request.form['id_aroma']
    delete = Aroma.query.get(id_aroma)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/live-search", methods=['GET', 'POST'])
def aroma_response():
    if request.method == 'POST':
        id = request.form['pabrik_response']
        aroma = db.session.query(Aroma).filter(Aroma.id_pabrik.like(id))

    return jsonify({'htmlresponse': render_template('database/aroma-response.html', aroma = aroma)})


@datab.route('/database/pabrik', methods=['GET', 'POST'])
def pabrik():
    pabrik = db.session.query(Pabrik).order_by(Pabrik.id_pabrik.desc()).limit(10).all() 

    return render_template('database/pabrik.html', pabrik_nav = 'active', pabrik = pabrik)


@datab.route('/database/pabrik/add', methods=['POST'])
def pabrik_add():
    if request.method == 'POST':
        nama = request.form['nama']

        data = Pabrik(nama = nama)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan')

        return redirect(url_for('datab.pabrik'))


@datab.route("/database/pabrik/edit", methods=['GET', 'POST'])
def pabrik_edit():
    if request.method == 'POST':
        update = Pabrik.query.get(request.form.get('id_pabrik'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah")

        return redirect(url_for('datab.pabrik'))


@datab.route("/database/pabrik/delete", methods=['GET', 'POST'])
def pabrik_delete():
    id_pabrik = request.form['id_pabrik']
    delete = Pabrik.query.get(id_pabrik)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus")

    return redirect(url_for('datab.pabrik'))