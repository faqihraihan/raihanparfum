from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify
from sqlalchemy import func, extract
from app import db
from app.models.models import Penjualan

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

    return render_template('dashboard/dashboard.html',
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