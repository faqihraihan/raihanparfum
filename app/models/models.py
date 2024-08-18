from app import db

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
    harga = db.Column(db.Integer)
    harga2 = db.Column(db.Integer())
    harga3 = db.Column(db.Integer())
    harga4 = db.Column(db.Integer())
    harga5 = db.Column(db.Integer())

    penjualan_rs = db.relationship("Penjualan", backref="aroma")
    pembelian_rs = db.relationship("Pembelian", backref="aroma")
    stock_rs = db.relationship("Stock", backref="aroma")

class Penjualan(db.Model):
    id_penjualan = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.Integer(), db.ForeignKey('aroma.id_aroma'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())

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