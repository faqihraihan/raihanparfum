from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.models.models import Penjualan, Aroma, Pabrik, Stock, Supplier, Barang, Ukur, Pembelian, Pelanggan, Log_pelanggan
from app import db
from datetime import datetime
import os
from sqlalchemy import func

datab = Blueprint('datab', __name__)

basedir = os.path.abspath(os.path.dirname(__file__))
foto_btl_folder = os.path.join(basedir, '..', 'static', 'img', 'btl')

datab.config = {
    'FOTO_BTL_FOLDER': foto_btl_folder,
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg'}
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in datab.config['ALLOWED_EXTENSIONS']


@datab.route('/database/penjualan', methods=['GET', 'POST'])
def penjualan():

    penjualan = db.session.query(Penjualan).order_by(Penjualan.id_penjualan.desc()).limit(20).all()
    pabrik = db.session.query(Pabrik).all()
    pelanggan = db.session.query(Pelanggan).all()

    return render_template('database/penjualan.html', penjualan_nav = 'active', penjualan = penjualan, pabrik = pabrik, pelanggan = pelanggan)


@datab.route('/database/penjualan/add', methods=['POST'])
def penjualan_add():
    if request.method == 'POST':
        id_pabrik = request.form['pabrik']
        id_aroma = request.form['aroma']
        qty = int(request.form['qty'])
        harga = request.form['harga']
        date = request.form['date']

        date_object = datetime.strptime(date, '%Y-%m-%d')
        
        id_pelanggan = request.form.get('pelanggan')
        
        now = datetime.now()
        year = now.strftime("%y")
        month = now.strftime("%m")

        last_penjualan = db.session.query(Penjualan).filter(
            func.strftime('%Y-%m', Penjualan.created_at) == now.strftime('%Y-%m')
            ).order_by(Penjualan.id_penjualan.desc()).first()

        if last_penjualan:
            last_id_str = last_penjualan.id_penjualan[-5:]
            last_id_number = int(last_id_str)
            new_id_number = last_id_number + 1
        else:
            new_id_number = 10001

        id_penjualan = f"S{year}{month}{new_id_number}"

        stock_item = Stock.query.filter_by(id_aroma = id_aroma).first()
        if stock_item:
            if stock_item.stock >= qty:
                stock_item.stock -= qty
                
                if id_pelanggan:
                    log = Log_pelanggan(id_pelanggan = id_pelanggan,
                                        id_penjualan = id_penjualan)

                    db.session.add(log)

                    data = Penjualan(id_penjualan = id_penjualan,
                                id_pabrik = id_pabrik,
                                id_aroma = id_aroma,
                                qty = qty,
                                harga = harga,
                                date = date_object,
                                id_pelanggan = id_pelanggan)
                else:
                    data = Penjualan(id_penjualan = id_penjualan,
                                id_pabrik = id_pabrik,
                                id_aroma = id_aroma,
                                qty = qty,
                                harga = harga,
                                date = date_object)
                    
                db.session.add(data)
                db.session.commit()
                flash('Data berhasil ditambahkan', 'success')
            else:
                db.session.rollback()
                flash('Stock tidak mencukupi', 'primary')
        else:
            db.session.rollback()
            flash('Belum ada data stock aroma ini ', 'primary')

        return redirect(url_for('datab.penjualan'))


@datab.route("/database/penjualan/edit", methods=['GET', 'POST'])
def penjualan_edit():
    if request.method == 'POST':
        update = Penjualan.query.get(request.form.get('id_penjualan'))
        log_pelanggan = Log_pelanggan.query.filter_by(id_penjualan = request.form.get('id_penjualan')).first()

        old_qty = update.qty
        old_aroma = update.id_aroma

        pabrik = request.form.get('pabrik')
        aroma = request.form.get('aroma')
        qty = int(request.form['qty'])
        update.harga = request.form['harga']
        date = request.form['date']
        date_object = datetime.strptime(date, '%Y-%m-%d')
        pelanggan = request.form.get('pelanggan')

        if pabrik:
            update.id_pabrik = pabrik
        
        if aroma:
            update.id_aroma = aroma

        update.qty = qty
        update.date = date_object

        if pelanggan != update.id_pelanggan:
            update.id_pelanggan = pelanggan

            if log_pelanggan:
                log_pelanggan.id_pelanggan = pelanggan
            else:
                new_log_pelanggan = Log_pelanggan(id_pelanggan = pelanggan, id_penjualan = update.id_penjualan)
                db.session.add(new_log_pelanggan)

        if aroma: # Parfum
            new_stock = Stock.query.filter_by(id_aroma = aroma).first()
            if new_stock:
                new_stock.stock += qty
            else:
                db.session.rollback()
                flash("Belum ada data stock aroma ini", 'primary')
                return redirect(url_for('datab.penjualan'))

        else: # Botol dan Larutan
            new_stock = Stock.query.filter_by(id_aroma = old_aroma).first()
     
            if qty > old_qty:
                stock_difference = qty - old_qty
                if new_stock.stock >= stock_difference:
                    new_stock.stock -= stock_difference
                else:
                    db.session.rollback()
                    flash("Stock tidak mencukupi", 'primary')
                    return redirect(url_for('datab.penjualan'))
            else:
                stock_difference = old_qty - qty
                new_stock.stock += stock_difference

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.penjualan'))


@datab.route("/database/penjualan/delete", methods=['GET', 'POST'])
def penjualan_delete():
    id_penjualan = request.form['id_penjualan']
    delete = Penjualan.query.get(id_penjualan)

    delete_log_pelanggan = Log_pelanggan.query.filter_by(id_penjualan = id_penjualan).first()

    stock_item = Stock.query.filter_by(id_aroma = delete.id_aroma).first()
    stock_item.stock += delete.qty

    db.session.delete(delete)
    db.session.delete(delete_log_pelanggan)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.penjualan'))


@datab.route('/database/aroma', methods=['GET', 'POST'])
def aroma():
    aroma = db.session.query(Aroma).order_by(Aroma.id_aroma.desc()).limit(20).all()
    pabrik = db.session.query(Pabrik).all()

    results = []
    if request.method == 'POST':
        search_pabrik = request.form.get('search_pabrik')
        search_aroma = request.form.get('search_aroma')

        if search_pabrik is None:
            search_pabrik = ''

        if search_aroma is None:
            search_aroma = ''

        results = db.session.query(Aroma).filter(
            Aroma.id_pabrik.contains(search_pabrik),
            Aroma.nama.contains(search_aroma)
        ).limit(20).all()
    
        return render_template('database/aroma.html', aroma_nav = 'active', aroma = aroma, pabrik = pabrik, search_aroma = results)

    return render_template('database/aroma.html', aroma_nav = 'active', aroma = aroma, pabrik = pabrik)


@datab.route('/database/aroma/add', methods=['POST'])
def aroma_add():
    if request.method == 'POST':
        nama = request.form['nama']
        id_pabrik = request.form['pabrik']
        harga2 = request.form['harga2']
        harga3 = request.form['harga3']
        harga4 = request.form['harga4']
        harga5 = request.form['harga5']

        data = Aroma(nama = nama,
                     id_pabrik = id_pabrik,
                     harga2 = harga2,
                     harga3 = harga3,
                     harga4 = harga4,
                     harga5 = harga5)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/edit", methods=['GET', 'POST'])
def aroma_edit():
    if request.method == 'POST':
        update = Aroma.query.get(request.form.get('id_aroma'))
        update.nama = request.form['nama']

        pabrik = request.form.get('pabrik')

        if pabrik != None:
            update.id_pabrik = pabrik

        update.harga2 = request.form['harga2']
        update.harga3 = request.form['harga3']
        update.harga4 = request.form['harga4']
        update.harga5 = request.form['harga5']

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/delete", methods=['GET', 'POST'])
def aroma_delete():
    id_aroma = request.form['id_aroma']
    delete = Aroma.query.get(id_aroma)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.aroma'))


@datab.route("/database/aroma/live-search", methods=['GET', 'POST'])
def aroma_response():
    if request.method == 'POST':
        id = request.form['pabrik_response']
        aroma = db.session.query(Aroma).filter(Aroma.id_pabrik.like(id))

    return jsonify({'htmlresponse': render_template('database/aroma-response.html', aroma = aroma)})


@datab.route('/database/stock', methods=['GET', 'POST'])
def stock():
    stock = db.session.query(Stock).order_by(Stock.id_stock.desc()).limit(20).all()
    pabrik = db.session.query(Pabrik).all()

    results = []
    if request.method == 'POST':
        search_pabrik = request.form.get('search_pabrik')
        search_aroma = request.form.get('search_aroma')

        if search_pabrik is None:
            search_pabrik = ''

        if search_aroma is None:
            search_aroma = ''

        results = db.session.query(Stock).join(Stock.aroma).filter(
            Stock.id_pabrik.contains(search_pabrik),
            Aroma.nama.contains(search_aroma)
        ).limit(20).all()
    
        return render_template('database/stock.html', stock_nav = 'active', stock = stock, pabrik = pabrik, search_stock = results)

    return render_template('database/stock.html', stock_nav = 'active', stock = stock, pabrik = pabrik)


@datab.route('/database/stock/add', methods=['POST'])
def stock_add():
    if request.method == 'POST':
        id_pabrik = request.form['pabrik']
        id_aroma = request.form['aroma']
        stock = request.form['stock']

        existing_stock = Stock.query.filter_by(id_aroma=id_aroma).first()

        if existing_stock:
            flash('Gagal menambahkan, data stock sudah ada dalam database', 'primary')
            return redirect(url_for('datab.stock'))

        data = Stock(id_pabrik = id_pabrik,
                     id_aroma = id_aroma,
                     stock = stock)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.stock'))


@datab.route("/database/stock/edit", methods=['GET', 'POST'])
def stock_edit():
    if request.method == 'POST':
        update = Stock.query.get(request.form.get('id_stock'))
        update.stock = request.form['stock']

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.stock'))


@datab.route("/database/stock/delete", methods=['GET', 'POST'])
def stock_delete():
    id_stock = request.form['id_stock']
    delete = Stock.query.get(id_stock)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.stock'))


@datab.route('/database/pabrik', methods=['GET', 'POST'])
def pabrik():
    pabrik = db.session.query(Pabrik).order_by(Pabrik.id_pabrik.desc()).limit(20).all() 

    return render_template('database/pabrik.html', pabrik_nav = 'active', pabrik = pabrik)


@datab.route('/database/pabrik/add', methods=['POST'])
def pabrik_add():
    if request.method == 'POST':
        nama = request.form['nama']

        data = Pabrik(nama = nama)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.pabrik'))


@datab.route("/database/pabrik/edit", methods=['GET', 'POST'])
def pabrik_edit():
    if request.method == 'POST':
        update = Pabrik.query.get(request.form.get('id_pabrik'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.pabrik'))


@datab.route("/database/pabrik/delete", methods=['GET', 'POST'])
def pabrik_delete():
    id_pabrik = request.form['id_pabrik']
    delete = Pabrik.query.get(id_pabrik)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.pabrik'))


@datab.route('/database/supplier', methods=['GET', 'POST'])
def supplier():
    supplier = db.session.query(Supplier).order_by(Supplier.id_supplier.desc()).limit(20).all() 

    return render_template('database/supplier.html', supplier_nav = 'active', supplier = supplier)


@datab.route('/database/supplier/add', methods=['POST'])
def supplier_add():
    if request.method == 'POST':
        nama = request.form['nama']

        data = Supplier(nama = nama)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.supplier'))


@datab.route("/database/supplier/edit", methods=['GET', 'POST'])
def supplier_edit():
    if request.method == 'POST':
        update = Supplier.query.get(request.form.get('id_supplier'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.supplier'))


@datab.route("/database/supplier/delete", methods=['GET', 'POST'])
def supplier_delete():
    id_supplier = request.form['id_supplier']
    delete = Supplier.query.get(id_supplier)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.supplier'))


@datab.route('/database/barang', methods=['GET', 'POST'])
def barang():
    barang = db.session.query(Barang).order_by(Barang.id_barang.desc()).all()
    supplier = db.session.query(Supplier).all()
    ukur = db.session.query(Ukur).all()

    return render_template('database/barang.html', barang_nav = 'active', barang = barang, supplier = supplier, ukur = ukur)


@datab.route('/database/barang/add', methods=['POST'])
def barang_add():
    if request.method == 'POST':
        nama = request.form['barang']
        jenis = request.form['jenis']
        toko = request.form['toko']
        harga = request.form['harga']
        ukur = request.form['ukur']

        data = Barang(jenis = jenis,
                    nama = nama,
                    id_supplier = toko,
                    harga = harga,
                    id_ukur = ukur)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.barang'))


@datab.route("/database/barang/edit", methods=['GET', 'POST'])
def barang_edit():
    if request.method == 'POST':
        update = Barang.query.get(request.form.get('id_barang'))
        update.nama = request.form['barang']
        update.harga = request.form['harga']
        toko = request.form.get('toko')
        jenis = request.form.get('jenis')
        ukur = request.form.get('ukur')

        if toko:
            update.id_supplier = toko

        if jenis:
            update.jenis = jenis

        if ukur:
            update.id_ukur = ukur

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.barang'))


@datab.route("/database/barang/delete", methods=['GET', 'POST'])
def barang_delete():
    id_barang = request.form['id_barang']
    delete = Barang.query.get(id_barang)

    image_filename = delete.foto
    
    db.session.delete(delete)
    db.session.commit()

    if image_filename:
        image_path = os.path.join(datab.config['FOTO_BTL_FOLDER'], image_filename)
        if os.path.isfile(image_path):
            os.remove(image_path)

    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.barang'))


@datab.route("/database/barang/live-search", methods=['GET', 'POST'])
def barang_response():
    if request.method == 'POST':
        jenis = request.form['barang_response']
        barang = db.session.query(Barang).filter(Barang.jenis.like(jenis))

    return jsonify({'htmlresponse': render_template('database/barang-response.html', barang = barang)})


@datab.route('/database/barang/foto/add', methods=['POST'])
def barang_add_foto():
    if request.method == 'POST':
        id = request.form['id_barang']
        file = request.files['image']

        if not allowed_file(file.filename):
            flash('Tipe gambar tidak sesuai', 'info')
            return redirect(url_for('datab.barang'))
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{id}.{extension}"
        filepath = os.path.join(datab.config['FOTO_BTL_FOLDER'], new_filename)
        file.save(filepath)

        update = Barang.query.get(request.form.get('id_barang'))
        update.foto = new_filename

        db.session.commit()
        flash('Foto berhasil ditambahkan', 'success')

        return redirect(url_for('datab.barang'))


@datab.route("/database/barang/foto/edit", methods=['GET', 'POST'])
def barang_edit_foto():
    if request.method == 'POST':
        update = Barang.query.get(request.form.get('id_barang'))
        file = request.files['image']

        if not allowed_file(file.filename):
            flash('Tipe gambar tidak sesuai', 'info')
            return redirect(url_for('datab.barang'))

        image_filename = update.foto
        
        if file:
            image_path = os.path.join(datab.config['FOTO_BTL_FOLDER'], image_filename)
            if os.path.isfile(image_path):
                os.remove(image_path)

            file.save(image_path)

        flash("Foto berhasil diubah", 'success')

        return redirect(url_for('datab.barang'))


@datab.route("/database/barang/foto/delete", methods=['GET', 'POST'])
def barang_delete_foto():
    id_barang = request.form['id_barang']
    barang = Barang.query.get(id_barang)

    image_filename = barang.foto
    
    barang.foto = None
    db.session.commit()

    if image_filename:
        image_path = os.path.join(datab.config['FOTO_BTL_FOLDER'], image_filename)
        if os.path.isfile(image_path):
            os.remove(image_path)

    flash("Foto berhasil dihapus", 'success')

    return redirect(url_for('datab.barang'))


@datab.route('/database/ukuran', methods=['GET', 'POST'])
def ukur():
    ukur = db.session.query(Ukur).order_by(Ukur.id_ukur.desc()).limit(20).all() 

    return render_template('database/ukur.html', ukur_nav = 'active', ukur = ukur)


@datab.route('/database/ukuran/add', methods=['POST'])
def ukur_add():
    if request.method == 'POST':
        nama = request.form['nama']

        data = Ukur(nama = nama)

        db.session.add(data)
        db.session.commit()
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.ukur'))


@datab.route("/database/ukuran/edit", methods=['GET', 'POST'])
def ukur_edit():
    if request.method == 'POST':
        update = Ukur.query.get(request.form.get('id_ukur'))
        update.nama = request.form['nama']

        db.session.commit()
        flash("Data berhasil diubah", 'success')

        return redirect(url_for('datab.ukur'))


@datab.route("/database/ukuran/delete", methods=['GET', 'POST'])
def ukur_delete():
    id_ukur = request.form['id_ukur']
    delete = Ukur.query.get(id_ukur)

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.ukur'))


@datab.route('/database/pembelian', methods=['GET', 'POST'])
def pembelian():
    pembelian = db.session.query(Pembelian).order_by(Pembelian.id_pembelian.desc()).limit(20).all()
    pabrik = db.session.query(Pabrik).all()
    barang = db.session.query(Barang).all()
    supplier = db.session.query(Supplier).all()

    return render_template('database/pembelian.html', pembelian_nav = 'active', pembelian = pembelian, pabrik = pabrik, barang = barang, supplier = supplier)


@datab.route('/database/pembelian/add', methods=['POST'])
def pembelian_add():
    if request.method == 'POST':
        id_pabrik = request.form.get('pabrik')
        id_aroma = request.form.get('aroma')
        id_barang = request.form.get('barang')
        id_supplier = request.form['toko']
        qty_list = request.form.getlist('qty')
        harga = request.form['harga']
        date = request.form['date']

        date_object = datetime.strptime(date, '%Y-%m-%d')

        selected_qty = None
        for qty_str in qty_list:
            if qty_str:
                selected_qty = int(qty_str)
                break

        if id_aroma:
            stock_item = Stock.query.filter_by(id_aroma = id_aroma).first()

            update = Aroma.query.get(id_aroma)
            if selected_qty == 100:
                update.harga2 = int(harga) // 100
            elif selected_qty == 250:
                update.harga3 = int(harga) // 250
            elif selected_qty == 500:
                update.harga4 = int(harga) // 500
            elif selected_qty == 1000:
                update.harga5 = int(harga) // 1000

            if stock_item:
                stock_item.stock += selected_qty
            else:
                stock = Stock(id_pabrik = id_pabrik,
                                id_aroma = id_aroma,
                                stock = selected_qty)
                
                db.session.add(stock)

            data = Pembelian(id_aroma = id_aroma,
                        qty = selected_qty,
                        harga = harga,
                        date = date_object,
                        id_supplier = id_supplier)

            db.session.add(data)
            db.session.commit()
        else:
            data = Pembelian(id_barang = id_barang,
                        qty = selected_qty,
                        harga = harga,
                        date = date_object,
                        id_supplier = id_supplier)

            db.session.add(data)
            db.session.commit()
        
        flash('Data berhasil ditambahkan', 'success')

        return redirect(url_for('datab.pembelian'))


@datab.route("/database/pembelian/delete", methods=['GET', 'POST'])
def pembelian_delete():
    id_pembelian = request.form['id_pembelian']
    id_aroma = request.form.get('aroma')
    delete = Pembelian.query.get(id_pembelian)

    if id_aroma:
        stock_item = Stock.query.filter_by(id_aroma = delete.id_aroma).first()
        stock_item.stock -= delete.qty

    db.session.delete(delete)
    db.session.commit()
    flash("Data berhasil dihapus", 'success')

    return redirect(url_for('datab.pembelian'))