from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Prodi(db.Model):
    __tablename__ = "prodi"

    id_prodi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nm_prodi = db.Column(db.String(100), nullable=False)
    jenjang = db.Column(db.String(10), nullable=False)
    akreditasi = db.Column(db.String(10))

    dosen = db.relationship("Dosen", back_populates="prodi", passive_deletes="all")
    mahasiswa = db.relationship("Mahasiswa", back_populates="prodi", passive_deletes="all")


class Dosen(db.Model):
    __tablename__ = "dosen"

    nidn = db.Column(db.String(20), primary_key=True)
    nm_dosen = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    id_prodi = db.Column(db.Integer, db.ForeignKey("prodi.id_prodi"))

    prodi = db.relationship("Prodi", back_populates="dosen")
    mata_kuliah = db.relationship("MataKuliah", back_populates="dosen", passive_deletes="all")


class Mahasiswa(db.Model):
    __tablename__ = "mahasiswa"

    nim = db.Column(db.String(20), primary_key=True)
    nm_mahasiswa = db.Column(db.String(100), nullable=False)
    jns_kelamin = db.Column(db.String(10))
    tgl_lahir = db.Column(db.Date)
    alamat = db.Column(db.Text)
    id_prodi = db.Column(db.Integer, db.ForeignKey("prodi.id_prodi"))

    prodi = db.relationship("Prodi", back_populates="mahasiswa")
    krs = db.relationship("KRS", back_populates="mahasiswa", passive_deletes="all")


class MataKuliah(db.Model):
    __tablename__ = "mata_kuliah"

    id_mk = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nm_mk = db.Column(db.String(100), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    nidn = db.Column(db.String(20), db.ForeignKey("dosen.nidn"))

    dosen = db.relationship("Dosen", back_populates="mata_kuliah")
    krs = db.relationship("KRS", back_populates="mata_kuliah", passive_deletes="all")


class KRS(db.Model):
    __tablename__ = "krs"

    id_krs = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nim = db.Column(db.String(20), db.ForeignKey("mahasiswa.nim"), nullable=False)
    id_mk = db.Column(db.Integer, db.ForeignKey("mata_kuliah.id_mk"), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    th_akademik = db.Column(db.String(10), nullable=False)
    nilai = db.Column(db.String(10))

    mahasiswa = db.relationship("Mahasiswa", back_populates="krs")
    mata_kuliah = db.relationship("MataKuliah", back_populates="krs")
