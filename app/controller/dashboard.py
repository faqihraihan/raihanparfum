from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from sqlalchemy import func, extract
from app import db
from app.models.models import Penjualan, Supplier, Pesanan, Pabrik, Aroma, Barang, Ekspedisi
from sqlalchemy.orm.attributes import flag_modified

dashb = Blueprint('dashb', __name__)


@dashb.route('/', methods=['GET', 'POST'])
def dashboard():

    # Perhitungan Total Penjualan 'Hari Ini'
    date_today = datetime.today().date()
    total_today = db.session.query(func.sum(Penjualan.harga)).filter_by(date = date_today).scalar()
    total_today = total_today if total_today is not None else 0

    date_yesterday = date_today - timedelta(days = 1)
    total_yesterday = db.session.query(func.sum(Penjualan.harga)).filter_by(date = date_yesterday).scalar()
    total_yesterday = total_yesterday if total_yesterday is not None else 0

    if total_yesterday > 0:
        result_today = abs(((total_today - total_yesterday) / total_yesterday) * 100)
        result_today = round(result_today)

        if total_today < total_yesterday:
            status_today = 'danger'
            icon_today = 'down'
        elif total_today == total_yesterday:
            status_today = 'warning'
            icon_today = 'left'
        else:
            status_today = 'success'
            icon_today = 'up'
    else:
        if total_today > 0:
            result_today = float('100')
            status_today = 'success'
            icon_today = 'up'
        else:
            result_today = 0
            status_today = 'warning'
            icon_today = 'left'

    # Perhitungan Total Penjualan 'Minggu Ini'
    start_week = date_today - timedelta(days = date_today.weekday())
    end_week = start_week + timedelta(days = 6)

    start_last_week = start_week - timedelta(days = 7)
    end_last_week = end_week - timedelta(days = 7)

    total_this_week = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_week, end_week)).scalar()
    total_this_week = total_this_week if total_this_week is not None else 0

    total_last_week = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_last_week, end_last_week)).scalar()
    total_last_week = total_last_week if total_last_week is not None else 0

    if total_last_week > 0:
        result_week = abs(((total_this_week - total_last_week) / total_last_week) * 100)
        result_week = round(result_week)

        if total_this_week < total_last_week:
            status_week = 'danger'
            icon_week = 'down'
        elif total_this_week == total_last_week:
            status_week = 'warning'
            icon_week = 'left'
        else:
            status_week = 'success'
            icon_week = 'up'
    else:
        if total_this_week > 0:
            result_week = float('100')
            status_week = 'success'
            icon_week = 'up'
        else:
            result_week = 0
            status_week = 'warning'
            icon_week = 'left'

    # Perhitungan Total Penjualan 'Bulan Ini'
    start_month = date_today.replace(day = 1)
    end_month = (start_month + timedelta(days = 31)).replace(day = 1) - timedelta(days = 1)

    start_last_month = (start_month - timedelta(days = 1)).replace(day = 1)
    end_last_month = (start_month - timedelta(days = 1))

    total_this_month = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_month, end_month)).scalar()
    total_this_month = total_this_month if total_this_month is not None else 0

    total_last_month = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_last_month, end_last_month)).scalar()
    total_last_month = total_last_month if total_last_month is not None else 0

    if total_last_month > 0:
        result_month = abs(((total_this_month - total_last_month) / total_last_month) * 100)
        result_month = round(result_month)

        if total_this_month < total_last_month:
            status_month = 'danger'
            icon_month = 'down'
        elif total_this_month == total_last_month:
            status_month = 'warning'
            icon_month = 'left'
        else:
            status_month = 'success'
            icon_month = 'up'
    else:
        if total_this_month > 0:
            result_month = float('100')
            status_month = 'success'
            icon_month = 'up'
        else:
            result_month = 0
            status_month = 'warning'
            icon_month = 'left'

    # Perhitungan Total Penjualan 'Tahun Ini'
    start_year = date_today.replace(month = 1, day = 1)
    end_year = date_today.replace(month = 12, day = 31)

    start_last_year = start_year - timedelta(days = 365)
    end_last_year = end_year - timedelta(days = 365)

    total_this_year = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_year, end_year)).scalar()
    total_this_year = total_this_year if total_this_year is not None else 0

    total_last_year = db.session.query(func.sum(Penjualan.harga)).filter(Penjualan.date.between(start_last_year, end_last_year)).scalar()
    total_last_year = total_last_year if total_last_year is not None else 0

    if total_last_year > 0:
        result_year = abs(((total_this_year - total_last_year) / total_last_year) * 100)
        result_year = round(result_year)

        if total_this_year < total_last_year:
            status_year = 'danger'
            icon_year = 'down'
        elif total_this_year == total_last_year:
            status_year = 'warning'
            icon_year = 'left'
        else:
            status_year = 'success'
            icon_year = 'up'
    else:
        if total_this_year > 0:
            result_year = float('100')
            status_year = 'success'
            icon_year = 'up'
        else:
            result_year = 0
            status_year = 'normal'
            icon_year = 'left'

    return render_template('dashboard/dashboard.html', dashboard_nav = 'active',
                            total_today = total_today, result_today = result_today, status_today = status_today, icon_today = icon_today,
                            total_this_week = total_this_week, result_week = result_week, status_week = status_week, icon_week = icon_week,
                            total_this_month = total_this_month, result_month = result_month, status_month = status_month, icon_month = icon_month,
                            total_this_year = total_this_year, result_year = result_year, status_year = status_year, icon_year = icon_year)

@dashb.route('/api/penjualan-sebulan')
def penjualan_sebulan():
    date_today = datetime.today().date()

    start_month = date_today.replace(day=1)
    end_month = (start_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    start_last_month = (start_month - timedelta(days=1)).replace(day=1)
    end_last_month = start_month - timedelta(days=1)

    daily_sales_current_month = db.session.query(
        extract('day', Penjualan.date).label('day'),
        func.sum(Penjualan.harga).label('total_penjualan')
    ).filter(Penjualan.date.between(start_month, end_month))\
    .group_by(extract('day', Penjualan.date))\
    .order_by(extract('day', Penjualan.date)).all()

    daily_sales_last_month = db.session.query(
        extract('day', Penjualan.date).label('day'),
        func.sum(Penjualan.harga).label('total_penjualan')
    ).filter(Penjualan.date.between(start_last_month, end_last_month))\
    .group_by(extract('day', Penjualan.date))\
    .order_by(extract('day', Penjualan.date)).all()

    data_dict_current_month = {sale.day: sale.total_penjualan for sale in daily_sales_current_month}

    data_dict_last_month = {sale.day: sale.total_penjualan for sale in daily_sales_last_month}

    all_days = sorted(set(
        range(1, 32)
    ))

    data = [{'date': f'{day:02d}',
            'sale_this_month': data_dict_current_month.get(day, 0),
            'sale_last_month': data_dict_last_month.get(day, 0)}
            for day in all_days]

    return jsonify(data)


@dashb.route('/dashboard/list-pesanan', methods=['GET', 'POST'])
def list_pesanan():
    supplier = db.session.query(Supplier).all()
    pabrik = db.session.query(Pabrik).all()
    pesanan = db.session.query(Pesanan).filter_by(status = 0).all()

    id_aroma_set = {item['id_aroma'] 
                for order in pesanan 
                if order.item 
                for item in order.item
                if 'id_aroma' in item}

    id_larutan_set = {item['id_larutan'] 
                    for order in pesanan 
                    if order.item 
                    for item in order.item 
                    if 'id_larutan' in item}

    id_btl_set = {item['id_btl'] 
                for order in pesanan 
                if order.item 
                for item in order.item 
                if 'id_btl' in item}

    aroma = {
    aroma.id_aroma: {'nama': aroma.nama,
                     'pabrik': aroma.pabrik.nama,
                     'harga2': aroma.harga2 or 0,
                     'harga3': aroma.harga3 or 0,
                     'harga4': aroma.harga4 or 0,
                     'harga5': aroma.harga5 or 0}
                      for aroma in db.session.query(Aroma).filter(Aroma.id_aroma.in_(id_aroma_set)).all()
                     }

    larutan = {
        larutan.id_barang: {'nama': larutan.nama,
                            'ukur': larutan.ukur.nama,
                            'harga': larutan.harga}
                            for larutan in db.session.query(Barang).filter(Barang.id_barang.in_(id_larutan_set)).all()
                            }

    botol = {
        btl.id_barang: {'nama': btl.nama,
                        'ukur': btl.ukur.nama,
                        'harga': btl.harga}
                        for btl in db.session.query(Barang).filter(Barang.id_barang.in_(id_btl_set)).all()
                        }

    return render_template('dashboard/list-pesanan.html', list_pesanan_nav = 'active', supplier = supplier, pesanan = pesanan, pabrik = pabrik, aroma = aroma, larutan = larutan, botol = botol)


@dashb.route('/dashboard/list-pesanan/add', methods=['POST'])
def list_pesanan_add():
    if request.method == 'POST':
        id_supplier = request.form['id_supplier']
        nama = request.form['nama']
        status = 0

        now = datetime.now()
        year = now.strftime("%y")
        month = now.strftime("%m")

        last_pesanan = db.session.query(Pesanan).filter(
            func.strftime('%Y-%m', Pesanan.created_at) == now.strftime('%Y-%m')
            ).order_by(Pesanan.id_pesanan.desc()).first()

        if last_pesanan:
            last_id_str = last_pesanan.id_pesanan[-5:]
            last_id_number = int(last_id_str)
            new_id_number = last_id_number + 1
        else:
            new_id_number = 10001

        id_pesanan = f"O{id_supplier}{year}{month}{new_id_number}"

        data = Pesanan(id_pesanan = id_pesanan,
                       id_supplier = id_supplier,
                       item = [],
                       nama = nama,
                       status = status)
                    
        db.session.add(data)
        db.session.commit()

        return redirect(url_for('dashb.list_pesanan'))


@dashb.route("/dashboard/list-pesanan/add-item", methods=['GET', 'POST'])
def list_pesanan_add_item():
    if request.method == 'POST':
        id_aroma = request.form.get('aroma')
        id_barang = request.form.get('barang')
        qty_list = request.form.getlist('qty')
        update = Pesanan.query.get(request.form.get('id_pesanan'))

        selected_qty = None
        for qty_str in qty_list:
            if qty_str:
                selected_qty = int(qty_str)
                break

        if id_aroma:
            item_json = update.item

            if not item_json:
                item_json = []

            data_baru = {
                "id_aroma": id_aroma,
                "qty": int(selected_qty)
            }

            item_json.append(data_baru)

            update.item = item_json

            flag_modified(update, 'item')
            db.session.commit()
        else:
            item_json = update.item

            if not item_json:
                item_json = []

            if id_barang.startswith('IB'):
                data_baru = {
                    "id_btl": id_barang,
                    "qty": int(selected_qty)
                }
            else:
                data_baru = {
                    "id_larutan": id_barang,
                    "qty": int(selected_qty)
                }

            item_json.append(data_baru)

            update.item = item_json

            flag_modified(update, 'item')
            db.session.commit()

        return redirect(url_for('dashb.list_pesanan'))
    

@dashb.route('/dashboard/list-pesanan/delete_item/<order_id>/<int:item_index>', methods=['GET'])
def list_pesanan_delete_item(order_id, item_index):
    order = db.session.query(Pesanan).get(order_id)
    
    order.item.pop(item_index-1)
    flag_modified(order, 'item')
    db.session.commit()
    
    return redirect(url_for('dashb.list_pesanan', order_id=order_id))


@dashb.route("/dashboard/list-pesanan/delete/<order_id>", methods=['GET', 'POST'])
def list_pesanan_delete_pesanan(order_id):
    delete = Pesanan.query.get(order_id)

    db.session.delete(delete)
    db.session.commit()

    return redirect(url_for('dashb.list_pesanan'))


@dashb.route("/dashboard/list-pesanan/<order_id>/print", methods=['GET', 'POST'])
@dashb.route("/dashboard/list-pesanan/<order_id>", methods=['GET', 'POST'])
def detail_pesanan(order_id):
    pesanan = db.session.query(Pesanan).filter_by(id_pesanan=order_id).first()
    ekspedisi = db.session.query(Ekspedisi).all()

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    date = now.strftime("%d")
    time = (f"{date}-{month}-{year}")

    id_aroma_set = {item['id_aroma']
                for item in pesanan.item
                if 'id_aroma' in item}

    id_larutan_set = {item['id_larutan'] 
                    for item in pesanan.item 
                    if 'id_larutan' in item}

    id_btl_set = {item['id_btl']
                for item in pesanan.item 
                if 'id_btl' in item}

    aroma = {
            aroma.id_aroma: {'nama': aroma.nama,
                            'pabrik': aroma.pabrik.nama,
                            'harga2': aroma.harga2 or 0,
                            'harga3': aroma.harga3 or 0,
                            'harga4': aroma.harga4 or 0,
                            'harga5': aroma.harga5 or 0}
                            for aroma in db.session.query(Aroma).filter(Aroma.id_aroma.in_(id_aroma_set)).all()
                            }

    larutan = {
            larutan.id_barang: {'nama': larutan.nama,
                                'ukur': larutan.ukur.nama,
                                'harga': larutan.harga}
                                for larutan in db.session.query(Barang).filter(Barang.id_barang.in_(id_larutan_set)).all()
                                }

    botol = {
            btl.id_barang: {'nama': btl.nama,
                            'ukur': btl.ukur.nama,
                            'harga': btl.harga}
                            for btl in db.session.query(Barang).filter(Barang.id_barang.in_(id_btl_set)).all()}

    if request.path.endswith('/print'):
        return render_template('dashboard/detail-pesanan-print.html', list_pesanan_nav = 'active', order_id = order_id, pesanan = pesanan, time = time, aroma = aroma, larutan = larutan, botol = botol)
    else:
        return render_template('dashboard/detail-pesanan.html', list_pesanan_nav = 'active', order_id = order_id, pesanan = pesanan, time = time, aroma = aroma, larutan = larutan, botol = botol, ekspedisi = ekspedisi)
    

@dashb.route('/dashboard/list-pesanan/<order_id>/ekspedisi-add', methods=['POST'])
def ekspedisi_add(order_id):
    update = Pesanan.query.get(order_id)
    update.id_ekspedisi = request.form['ekspedisi']

    db.session.commit()

    return redirect(url_for('dashb.detail_pesanan', order_id = order_id))