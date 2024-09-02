from app import db
from datetime import datetime


# ID Code Information:
# S = Penjualan
# B = Pembelian
# O = Order
# IP = Item Parfum
# IB = Item Botol
# IL = Item Larutan
# EP = Ekpedisi
# MEM = Pelanggan


class Pabrik(db.Model):
    id_pabrik = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))

    aroma_rs = db.relationship("Aroma", backref="pabrik")
    penjualan_rs = db.relationship("Penjualan", backref="pabrik")
    stock_rs = db.relationship("Stock", backref="pabrik")


class Aroma(db.Model):
    # IP1 (IP-1: Prefix-ID Unik)
    id_aroma = db.Column(db.String(50), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    nama = db.Column(db.String(20))
    harga2 = db.Column(db.Integer()) # /100ml
    harga3 = db.Column(db.Integer()) # /250ml
    harga4 = db.Column(db.Integer()) # /500ml
    harga5 = db.Column(db.Integer()) # /1000ml

    penjualan_rs = db.relationship("Penjualan", backref="aroma")
    pembelian_rs = db.relationship("Pembelian", backref="aroma")
    stock_rs = db.relationship("Stock", backref="aroma")
    log_aroma_rs = db.relationship("Log_aroma", backref="aroma")


class Penjualan(db.Model):
    # S24081001 (S-2408-10001: Prefix-WaktuInput-Urutan)
    id_penjualan = db.Column(db.String(50), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.String(50), db.ForeignKey('aroma.id_aroma'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())
    created_at = db.Column(db.DateTime, default=datetime.now)
    id_pelanggan = db.Column(db.String(50), db.ForeignKey('pelanggan.id_pelanggan'))

    log_pelanggan_rs = db.relationship("Log_pelanggan", backref="penjualan")


class Stock(db.Model):
    id_stock = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.String(50), db.ForeignKey('aroma.id_aroma'))
    stock = db.Column(db.Integer())


class Supplier(db.Model):
    id_supplier = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))
    telp = db.Column(db.String(20))
    alamat = db.Column(db.String(50))

    barang_rs = db.relationship("Barang", backref="supplier")
    pembelian_rs = db.relationship("Pembelian", backref="supplier")
    pesanan_rs = db.relationship("Pesanan", backref="supplier")


class Barang(db.Model):
    id_barang = db.Column(db.String(50), primary_key = True)
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
    # B24081001 (B-2408-10001: Prefix-WaktuInput-Urutan)
    id_pembelian = db.Column(db.String(50), primary_key = True)
    id_aroma = db.Column(db.String(50), db.ForeignKey('aroma.id_aroma'))
    id_barang = db.Column(db.String(50), db.ForeignKey('barang.id_barang'))
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id_supplier'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())
    created_at = db.Column(db.DateTime, default=datetime.now)

    log_aroma_rs = db.relationship("Log_aroma", backref="pembelian")


class Pelanggan(db.Model):
    # MEM24081001 (MEM-2408-10001: Prefix-WaktuTerdaftar-Urutan)
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


class Log_aroma(db.Model):
    id_log_aroma = db.Column(db.Integer(), primary_key=True)
    id_aroma = db.Column(db.String(50), db.ForeignKey('aroma.id_aroma'))
    id_pembelian = db.Column(db.Integer(), db.ForeignKey('pembelian.id_pembelian'))


class Pesanan(db.Model):
    # O124081001 (O-1-2408-10001: Prefix-ID Supplier-WaktuTerdaftar-Urutan)
    id_pesanan = db.Column(db.String(50), primary_key=True)
    id_supplier = db.Column(db.Integer(), db.ForeignKey('supplier.id_supplier'))
    id_ekspedisi = db.Column(db.String(50), db.ForeignKey('ekspedisi.id_ekspedisi'))
    nama = db.Column(db.String(20))
    item = db.Column(db.JSON)
    status = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=datetime.now)


class Ekspedisi(db.Model):
    # EP1 (EP-1: Prefix-ID Ekspedisi)
    id_ekspedisi = db.Column(db.String(50), primary_key = True)
    nama = db.Column(db.String(20))
    telp = db.Column(db.String(20))
    alamat = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    pesanan_rs = db.relationship("Pesanan", backref="ekspedisi")
