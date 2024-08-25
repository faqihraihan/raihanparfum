from app import db
from datetime import datetime


class Pabrik(db.Model):
    id_pabrik = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))

    aroma_rs = db.relationship("Aroma", backref="pabrik")
    penjualan_rs = db.relationship("Penjualan", backref="pabrik")
    stock_rs = db.relationship("Stock", backref="pabrik")


class Aroma(db.Model):
    id_aroma = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    nama = db.Column(db.String(20))
    harga2 = db.Column(db.Integer()) # /100ml
    harga3 = db.Column(db.Integer()) # /250ml
    harga4 = db.Column(db.Integer()) # /500ml
    harga5 = db.Column(db.Integer()) # /1000ml

    penjualan_rs = db.relationship("Penjualan", backref="aroma")
    pembelian_rs = db.relationship("Pembelian", backref="aroma")
    stock_rs = db.relationship("Stock", backref="aroma")


class Penjualan(db.Model):
    id_penjualan = db.Column(db.String(50), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.Integer(), db.ForeignKey('aroma.id_aroma'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())
    created_at = db.Column(db.DateTime, default=datetime.now)
    id_pelanggan = db.Column(db.String(50), db.ForeignKey('pelanggan.id_pelanggan'))

    log_pelanggan_rs = db.relationship("Log_pelanggan", backref="penjualan")


class Stock(db.Model):
    id_stock = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.Integer(), db.ForeignKey('aroma.id_aroma'))
    stock = db.Column(db.Integer())


class Supplier(db.Model):
    id_supplier = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))

    barang_rs = db.relationship("Barang", backref="supplier")
    pembelian_rs = db.relationship("Pembelian", backref="supplier")


class Barang(db.Model):
    id_barang = db.Column(db.Integer(), primary_key = True)
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id_supplier'))
    id_ukur = db.Column(db.Integer(), db.ForeignKey('ukur.id_ukur'))
    nama = db.Column(db.String(20))
    jenis = db.Column(db.String(20))
    harga = db.Column(db.Integer())
    foto = db.Column(db.String(20))

    pembelian_rs = db.relationship("Pembelian", backref="barang")


class Ukur(db.Model):
    id_ukur = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))

    barang_rs = db.relationship("Barang", backref="ukur")


class Pembelian(db.Model):
    id_pembelian = db.Column(db.Integer(), primary_key = True)
    id_aroma = db.Column(db.Integer(), db.ForeignKey('aroma.id_aroma'))
    id_barang = db.Column(db.Integer(), db.ForeignKey('barang.id_barang'))
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id_supplier'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())


class Pelanggan(db.Model):
    # MEM2024081001 (MEM-202408-10001: Prefix-WaktuTerdaftar-Urutan)
    id_pelanggan = db.Column(db.String(50), primary_key=True)
    nama = db.Column(db.String(20))
    telp = db.Column(db.String(20))
    alamat = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    penjualan_rs = db.relationship("Penjualan", backref="pelanggan")
    log_pelanggan_rs = db.relationship("Log_pelanggan", backref="pelanggan")


class Log_pelanggan(db.Model):
    id_log_pelanggan = db.Column(db.Integer(), primary_key=True)
    id_pelanggan = db.Column(db.String(50), db.ForeignKey('pelanggan.id_pelanggan'))
    id_penjualan = db.Column(db.Integer(), db.ForeignKey('penjualan.id_penjualan'))