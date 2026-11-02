import hmac
from datetime import datetime
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from config import Config
from database import KRS, Dosen, Mahasiswa, MataKuliah, Prodi, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

PESAN_FK = ("Data tidak dapat diproses: kode/ID sudah terdaftar, atau data masih "
            "dipakai oleh data lain (relasi).")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def simpan(pesan_sukses):
    """Commit sesi; tampilkan flash sukses/gagal. Mengembalikan True bila berhasil."""
    try:
        db.session.commit()
        flash(pesan_sukses, "success")
        return True
    except IntegrityError:
        db.session.rollback()
        flash(PESAN_FK, "danger")
        return False


def hapus(obj, pesan_sukses):
    db.session.delete(obj)
    simpan(pesan_sukses)


def teks(nama):
    return request.form.get(nama, "").strip()


def teks_atau_none(nama):
    nilai = teks(nama)
    return nilai or None


def angka(nama):
    return request.form.get(nama, type=int)


def query_krs_lengkap(q=""):
    """Query JOIN: krs + mahasiswa + mata_kuliah."""
    query = (
        db.session.query(
            KRS.id_krs,
            Mahasiswa.nim,
            Mahasiswa.nm_mahasiswa,
            MataKuliah.nm_mk,
            MataKuliah.sks,
            KRS.semester,
            KRS.th_akademik,
            KRS.nilai,
        )
        .select_from(KRS)
        .join(Mahasiswa, KRS.nim == Mahasiswa.nim)
        .join(MataKuliah, KRS.id_mk == MataKuliah.id_mk)
    )
    if q:
        like = f"%{q}%"
        query = query.filter(or_(
            Mahasiswa.nim.like(like),
            Mahasiswa.nm_mahasiswa.like(like),
            MataKuliah.nm_mk.like(like),
            KRS.th_akademik.like(like),
            KRS.nilai.like(like),
        ))
    return query.order_by(KRS.th_akademik.desc(), KRS.semester, Mahasiswa.nim,
                          KRS.id_krs).all()


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user_ok = hmac.compare_digest(username.encode(), app.config["ADMIN_USERNAME"].encode())
        pass_ok = hmac.compare_digest(password.encode(), app.config["ADMIN_PASSWORD"].encode())
        if user_ok and pass_ok:
            session.clear()
            session["logged_in"] = True
            session["username"] = username
            flash("Login berhasil. Selamat datang!", "success")
            return redirect(url_for("dashboard"))
        flash("Username atau password salah.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    stat = {
        "prodi": Prodi.query.count(),
        "dosen": Dosen.query.count(),
        "mahasiswa": Mahasiswa.query.count(),
        "mata_kuliah": MataKuliah.query.count(),
        "krs": KRS.query.count(),
    }
    krs_terbaru = query_krs_lengkap()[:5]
    return render_template("dashboard.html", stat=stat, krs_terbaru=krs_terbaru)


@app.route("/prodi")
@login_required
def prodi_index():
    q = request.args.get("q", "").strip()
    query = Prodi.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Prodi.nm_prodi.like(like),
                                 Prodi.jenjang.like(like),
                                 Prodi.akreditasi.like(like)))
    data = query.order_by(Prodi.id_prodi).all()
    return render_template("prodi/index.html", data=data, q=q)


@app.route("/prodi/tambah", methods=["GET", "POST"])
@login_required
def prodi_tambah():
    item = None
    if request.method == "POST":
        item = Prodi(nm_prodi=teks("nm_prodi"), jenjang=teks("jenjang"),
                     akreditasi=teks_atau_none("akreditasi"))
        db.session.add(item)
        if simpan("Data prodi berhasil ditambahkan."):
            return redirect(url_for("prodi_index"))
    return render_template("prodi/form.html", item=item, mode="tambah")


@app.route("/prodi/edit/<int:id_prodi>", methods=["GET", "POST"])
@login_required
def prodi_edit(id_prodi):
    item = db.get_or_404(Prodi, id_prodi)
    if request.method == "POST":
        item.nm_prodi = teks("nm_prodi")
        item.jenjang = teks("jenjang")
        item.akreditasi = teks_atau_none("akreditasi")
        if simpan("Data prodi berhasil diperbarui."):
            return redirect(url_for("prodi_index"))
    return render_template("prodi/form.html", item=item, mode="edit")


@app.route("/prodi/hapus/<int:id_prodi>", methods=["POST"])
@login_required
def prodi_hapus(id_prodi):
    hapus(db.get_or_404(Prodi, id_prodi), "Data prodi berhasil dihapus.")
    return redirect(url_for("prodi_index"))


@app.route("/dosen")
@login_required
def dosen_index():
    q = request.args.get("q", "").strip()
    query = Dosen.query.outerjoin(Prodi, Dosen.id_prodi == Prodi.id_prodi)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Dosen.nidn.like(like), Dosen.nm_dosen.like(like),
                                 Dosen.email.like(like), Prodi.nm_prodi.like(like)))
    data = query.order_by(Dosen.nm_dosen).all()
    return render_template("dosen/index.html", data=data, q=q)


@app.route("/dosen/tambah", methods=["GET", "POST"])
@login_required
def dosen_tambah():
    item = None
    if request.method == "POST":
        item = Dosen(nidn=teks("nidn"), nm_dosen=teks("nm_dosen"),
                     email=teks_atau_none("email"), id_prodi=angka("id_prodi"))
        db.session.add(item)
        if simpan("Data dosen berhasil ditambahkan."):
            return redirect(url_for("dosen_index"))
    return render_template("dosen/form.html", item=item, mode="tambah",
                           prodi_list=Prodi.query.order_by(Prodi.nm_prodi).all())


@app.route("/dosen/edit/<nidn>", methods=["GET", "POST"])
@login_required
def dosen_edit(nidn):
    item = db.get_or_404(Dosen, nidn)
    if request.method == "POST":
        item.nm_dosen = teks("nm_dosen")
        item.email = teks_atau_none("email")
        item.id_prodi = angka("id_prodi")
        if simpan("Data dosen berhasil diperbarui."):
            return redirect(url_for("dosen_index"))
    return render_template("dosen/form.html", item=item, mode="edit",
                           prodi_list=Prodi.query.order_by(Prodi.nm_prodi).all())


@app.route("/dosen/hapus/<nidn>", methods=["POST"])
@login_required
def dosen_hapus(nidn):
    hapus(db.get_or_404(Dosen, nidn), "Data dosen berhasil dihapus.")
    return redirect(url_for("dosen_index"))


def parse_tanggal(nilai):
    try:
        return datetime.strptime(nilai, "%Y-%m-%d").date() if nilai else None
    except ValueError:
        return None


@app.route("/mahasiswa")
@login_required
def mahasiswa_index():
    q = request.args.get("q", "").strip()
    query = Mahasiswa.query.outerjoin(Prodi, Mahasiswa.id_prodi == Prodi.id_prodi)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Mahasiswa.nim.like(like), Mahasiswa.nm_mahasiswa.like(like),
                                 Mahasiswa.jns_kelamin.like(like), Mahasiswa.alamat.like(like),
                                 Prodi.nm_prodi.like(like)))
    data = query.order_by(Mahasiswa.nim).all()
    return render_template("mahasiswa/index.html", data=data, q=q)


@app.route("/mahasiswa/tambah", methods=["GET", "POST"])
@login_required
def mahasiswa_tambah():
    item = None
    if request.method == "POST":
        item = Mahasiswa(nim=teks("nim"), nm_mahasiswa=teks("nm_mahasiswa"),
                         jns_kelamin=teks_atau_none("jns_kelamin"),
                         tgl_lahir=parse_tanggal(teks("tgl_lahir")),
                         alamat=teks_atau_none("alamat"), id_prodi=angka("id_prodi"))
        db.session.add(item)
        if simpan("Data mahasiswa berhasil ditambahkan."):
            return redirect(url_for("mahasiswa_index"))
    return render_template("mahasiswa/form.html", item=item, mode="tambah",
                           prodi_list=Prodi.query.order_by(Prodi.nm_prodi).all())


@app.route("/mahasiswa/edit/<nim>", methods=["GET", "POST"])
@login_required
def mahasiswa_edit(nim):
    item = db.get_or_404(Mahasiswa, nim)
    if request.method == "POST":
        item.nm_mahasiswa = teks("nm_mahasiswa")
        item.jns_kelamin = teks_atau_none("jns_kelamin")
        item.tgl_lahir = parse_tanggal(teks("tgl_lahir"))
        item.alamat = teks_atau_none("alamat")
        item.id_prodi = angka("id_prodi")
        if simpan("Data mahasiswa berhasil diperbarui."):
            return redirect(url_for("mahasiswa_index"))
    return render_template("mahasiswa/form.html", item=item, mode="edit",
                           prodi_list=Prodi.query.order_by(Prodi.nm_prodi).all())


@app.route("/mahasiswa/hapus/<nim>", methods=["POST"])
@login_required
def mahasiswa_hapus(nim):
    hapus(db.get_or_404(Mahasiswa, nim), "Data mahasiswa berhasil dihapus.")
    return redirect(url_for("mahasiswa_index"))

@app.route("/mata-kuliah")
@login_required
def mk_index():
    q = request.args.get("q", "").strip()
    query = MataKuliah.query.outerjoin(Dosen, MataKuliah.nidn == Dosen.nidn)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(MataKuliah.nm_mk.like(like), MataKuliah.nidn.like(like),
                                 Dosen.nm_dosen.like(like)))
    data = query.order_by(MataKuliah.id_mk).all()
    return render_template("mata_kuliah/index.html", data=data, q=q)


@app.route("/mata-kuliah/tambah", methods=["GET", "POST"])
@login_required
def mk_tambah():
    item = None
    if request.method == "POST":
        item = MataKuliah(nm_mk=teks("nm_mk"), sks=angka("sks") or 0,
                          nidn=teks_atau_none("nidn"))
        db.session.add(item)
        if simpan("Data mata kuliah berhasil ditambahkan."):
            return redirect(url_for("mk_index"))
    return render_template("mata_kuliah/form.html", item=item, mode="tambah",
                           dosen_list=Dosen.query.order_by(Dosen.nm_dosen).all())


@app.route("/mata-kuliah/edit/<int:id_mk>", methods=["GET", "POST"])
@login_required
def mk_edit(id_mk):
    item = db.get_or_404(MataKuliah, id_mk)
    if request.method == "POST":
        item.nm_mk = teks("nm_mk")
        item.sks = angka("sks") or 0
        item.nidn = teks_atau_none("nidn")
        if simpan("Data mata kuliah berhasil diperbarui."):
            return redirect(url_for("mk_index"))
    return render_template("mata_kuliah/form.html", item=item, mode="edit",
                           dosen_list=Dosen.query.order_by(Dosen.nm_dosen).all())


@app.route("/mata-kuliah/hapus/<int:id_mk>", methods=["POST"])
@login_required
def mk_hapus(id_mk):
    hapus(db.get_or_404(MataKuliah, id_mk), "Data mata kuliah berhasil dihapus.")
    return redirect(url_for("mk_index"))

def data_pilihan_krs():
    return {
        "mahasiswa_list": Mahasiswa.query.order_by(Mahasiswa.nim).all(),
        "mk_list": MataKuliah.query.order_by(MataKuliah.nm_mk).all(),
    }


@app.route("/krs")
@login_required
def krs_index():
    q = request.args.get("q", "").strip()
    return render_template("krs/index.html", data=query_krs_lengkap(q), q=q)


@app.route("/krs/tambah", methods=["GET", "POST"])
@login_required
def krs_tambah():
    item = None
    if request.method == "POST":
        item = KRS(nim=teks("nim"), id_mk=angka("id_mk"), semester=angka("semester") or 0,
                   th_akademik=teks("th_akademik"), nilai=teks_atau_none("nilai"))
        db.session.add(item)
        if simpan("Data KRS berhasil ditambahkan."):
            return redirect(url_for("krs_index"))
    return render_template("krs/form.html", item=item, mode="tambah", **data_pilihan_krs())


@app.route("/krs/edit/<int:id_krs>", methods=["GET", "POST"])
@login_required
def krs_edit(id_krs):
    item = db.get_or_404(KRS, id_krs)
    if request.method == "POST":
        item.nim = teks("nim")
        item.id_mk = angka("id_mk")
        item.semester = angka("semester") or 0
        item.th_akademik = teks("th_akademik")
        item.nilai = teks_atau_none("nilai")
        if simpan("Data KRS berhasil diperbarui."):
            return redirect(url_for("krs_index"))
    return render_template("krs/form.html", item=item, mode="edit", **data_pilihan_krs())


@app.route("/krs/hapus/<int:id_krs>", methods=["POST"])
@login_required
def krs_hapus(id_krs):
    hapus(db.get_or_404(KRS, id_krs), "Data KRS berhasil dihapus.")
    return redirect(url_for("krs_index"))


@app.route("/krs/join")
@login_required
def krs_join():
    q = request.args.get("q", "").strip()
    return render_template("krs/join.html", data=query_krs_lengkap(q), q=q)


@app.route("/laporan")
@login_required
def laporan_index():
    return render_template("laporan/index.html")


@app.route("/laporan/<jenis>")
@login_required
def laporan_detail(jenis):
    if jenis == "prodi":
        judul = "Laporan Data Prodi"
        kolom = ["No", "ID Prodi", "Nama Prodi", "Jenjang", "Akreditasi"]
        baris = [[i, p.id_prodi, p.nm_prodi, p.jenjang, p.akreditasi or "-"]
                 for i, p in enumerate(Prodi.query.order_by(Prodi.id_prodi), 1)]
    elif jenis == "dosen":
        judul = "Laporan Data Dosen"
        kolom = ["No", "NIDN", "Nama Dosen", "Email", "Prodi"]
        baris = [[i, d.nidn, d.nm_dosen, d.email or "-", d.prodi.nm_prodi if d.prodi else "-"]
                 for i, d in enumerate(Dosen.query.order_by(Dosen.nm_dosen), 1)]
    elif jenis == "mahasiswa":
        judul = "Laporan Data Mahasiswa"
        kolom = ["No", "NIM", "Nama Mahasiswa", "Jenis Kelamin", "Tgl Lahir", "Alamat", "Prodi"]
        baris = [[i, m.nim, m.nm_mahasiswa, m.jns_kelamin or "-",
                  m.tgl_lahir.strftime("%d-%m-%Y") if m.tgl_lahir else "-",
                  m.alamat or "-", m.prodi.nm_prodi if m.prodi else "-"]
                 for i, m in enumerate(Mahasiswa.query.order_by(Mahasiswa.nim), 1)]
    elif jenis == "mata-kuliah":
        judul = "Laporan Data Mata Kuliah"
        kolom = ["No", "ID MK", "Nama Mata Kuliah", "SKS", "Dosen Pengampu"]
        baris = [[i, mk.id_mk, mk.nm_mk, mk.sks, mk.dosen.nm_dosen if mk.dosen else "-"]
                 for i, mk in enumerate(MataKuliah.query.order_by(MataKuliah.id_mk), 1)]
    elif jenis == "krs":
        judul = "Laporan Data KRS"
        kolom = ["No", "NIM", "Nama Mahasiswa", "Mata Kuliah", "SKS", "Semester",
                 "Tahun Akademik", "Nilai"]
        baris = [[i, r.nim, r.nm_mahasiswa, r.nm_mk, r.sks, r.semester, r.th_akademik,
                  r.nilai or "-"]
                 for i, r in enumerate(query_krs_lengkap(), 1)]
    else:
        return render_template("laporan/index.html"), 404

    return render_template("laporan/detail.html", judul=judul, kolom=kolom, baris=baris,
                           dicetak=datetime.now().strftime("%d-%m-%Y %H:%M"))

if __name__ == "__main__":
    app.run(debug=True)
