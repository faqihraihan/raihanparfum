from app import db

class Pabrik(db.Model):
    id_pabrik = db.Column(db.Integer(), primary_key = True)
    nama = db.Column(db.String(20))

    penjualan_rs = db.relationship("Penjualan", backref="pabrik")
    aroma_rs = db.relationship("Aroma", backref="pabrik")

class Aroma(db.Model):
    id_aroma = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    nama = db.Column(db.String(20))
    harga = db.Column(db.Integer)

    penjualan_rs = db.relationship("Penjualan", backref="aroma")

class Penjualan(db.Model):
    id_penjualan = db.Column(db.Integer(), primary_key = True)
    id_pabrik = db.Column(db.Integer(), db.ForeignKey('pabrik.id_pabrik'))
    id_aroma = db.Column(db.Integer(), db.ForeignKey('aroma.id_aroma'))
    qty = db.Column(db.Integer())
    harga = db.Column(db.Integer())
    date = db.Column(db.Date())