from flask import Flask, make_response, render_template, redirect, url_for, request, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from bson import ObjectId
from xhtml2pdf import pisa
import io
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'LisaMary'

UPLOAD_FOLDER = 'static/assets/images/foto'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)

# Koneksi MongoDB
client = MongoClient('mongodb+srv://AyangFreya:AyangElla@projectayang.c1mw30u.mongodb.net/')
db = client['Ayang_freya']
nilai_collection = db['nilai']
absen_collection = db['absen']
data_collection = db['data']
users_collection = db['users']
jadwal_collection = db['jadwal_ujian_guru']

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user_data = users_collection.find_one({'username': username})
    if not user_data:
        return

    user = User()
    user.id = username
    user.role = user_data.get('role', 'unknown')
    return user

@app.route('/')
def index():
    return render_template('SMP31-main.html')


@app.route('/data')
def data_siswa():
    hab = data_collection.find()
    return render_template('data_siswa.html', data=hab)

@app.route('/petugas')
def petugas():
    return render_template('petugas_dashboard.html')

@app.route('/dash')
def dash():
    return render_template('admin_dashboard.html')

@app.route('/siswa')
def siswa():
    return render_template('siswa_dashboard.html')

@app.route('/absen-siswa')
def absen_siswa():
    pe = absen_collection.find()
    return render_template('tambah_absen_siswa.html', absen=pe)

@app.route('/login-doang')
def login_doang():
    return render_template('login.html')

@app.route('/tambah')
def tambah_input():
    return render_template('tambah_input.html')

@app.route('/absen')
def tambah_absen():
    return render_template('tambah_absen.html')

@app.route('/prestasi')
def prestasi():
    return render_template('prestasi.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/galery')
def galery():
    return render_template('galery.html')

@app.route('/pendidikan')
def pendidikan():
    return render_template('pendidikan.html')

@app.route('/peserta')
def peserta():
    return render_template('peserta_didik.html')

@app.route('/data-kelas')
def data_kelas():
    return render_template('data-kelas.html')

@app.route('/absensi')
def absensi():
    pe = absen_collection.find()
    return render_template('absensi.html', absen=pe)

@app.route('/petugas-absensi')
def petugas_absensi():
    pe = absen_collection.find()
    return render_template('petugas-absensi.html', absen=pe)

@app.route('/input')
def input_page():
    syg = nilai_collection.find()
    return render_template('input.html', nilai=syg)

@app.route('/laporan')
def laporan():
    nilai = list(nilai_collection.find())
    return render_template('laporan.html', nilai=nilai)

@app.route('/pengaturan')
def pengaturan():
    return render_template('pengaturan.html')

@app.route('/terima-aduan')
def terima_aduan():
    return render_template('terima-aduan.html')

@app.route('/berita')
def berita():
    return render_template('berita.html')

@app.route('/aduan')
def aduan():
    return render_template('aduan.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/jadwal-ujian')
def jadwal_ujian():
    guru = jadwal_collection.find()
    return render_template('jadwal-ujian-guru.html', jadwal=guru)

@app.route('/ujian')
def ujian():
    return render_template('tambah_ujian_guru')

@app.route('/add-nilai', methods=['GET', 'POST'])
def add_nilai():
    if request.method == 'POST':
        nama = request.form['studentName']
        kelas = request.form['studentClass']
        status = request.form['status']

        data_absen = {
            'nama': nama,
            'kelas': kelas,
            'status': status
        }
        nilai_collection.insert_one(data_absen)
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template('Tambah.html')

@app.route('/add-absen', methods=['GET', 'POST'])
def add_absen():
    if request.method == 'POST':
        nama = request.form['nama_siswa']
        kelas = request.form['kelas']
        keterangan = request.form['keterangan']
        tanggal = request.form['tanggal']
        status_kehadiran = request.form['status']

        data_nilai = {
            'nama': nama,
            'kelas': kelas,
            'tanggal': tanggal,
            "keterangan":keterangan,
            'status_kehadiran': status_kehadiran
        }
        absen_collection.insert_one(data_nilai)
        return redirect(url_for('petugas'))
    elif request.method == 'GET':
        return render_template('Tambah.html')
    
    
@app.route('/add-siswa', methods=['GET', 'POST'])
def add_siswa():
    if request.method == 'POST':
        nama = request.form['nama_siswa']
        kelas = request.form['kelas']
        keterangan = request.form['keterangan']
        tanggal = request.form['tanggal']
        status_kehadiran = request.form['status']

        data_nilai = {
            'nama': nama,
            'kelas': kelas,
            'tanggal': tanggal,
            "keterangan":keterangan,
            'status_kehadiran': status_kehadiran
        }
        data_collection.insert_one(data_nilai)
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template('Tambah.html')

@app.route('/tambah-ujian-guru', methods=['GET', 'POST'])
def tambah_ujian_guru():
    if request.method == 'POST':
        # Mendapatkan data dari form
        nama_guru = request.form['nama_guru']
        tanggal_ujian = request.form['tanggal_ujian']
        mapel = request.form['mapel']
        
        # Menyimpan data ke dalam database
        jadwal_ujian = {
            'nama_guru': nama_guru,
            'tanggal_ujian': tanggal_ujian,
            'mapel': mapel
        }
        jadwal_collection.insert_one(jadwal_ujian)
        
        # Redirect ke halaman daftar jadwal ujian guru
        return redirect(url_for('jadwal_ujian'))  # Ubah ke route yang benar
    
    # Render template untuk menambah jadwal ujian guru
    return render_template('tambah_ujian_guru.html')

@app.route('/edit-absen/<id>', methods=['GET', 'POST'])
def edit_absen(id):
    if request.method == 'GET':
        if ObjectId.is_valid(id):
            data = absen_collection.find_one({'_id': ObjectId(id)})
            if data:
                return render_template('edit_absensi.html', absen=data)
        return "Data tidak ditemukan", 404
    elif request.method == 'POST':
        nama = request.form['nama_siswa']
        kelas = request.form['kelas']
        keterangan = request.form['keterangan']
        tanggal = request.form['tanggal']
        status_kehadiran = request.form['status']

        absen_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'nama': nama,
                'kelas': kelas,
                'keterangan': keterangan,
                'tanggal': tanggal,
                'status_kehadiran': status_kehadiran
            }}
        )
        return redirect(url_for('dashboard'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_nilai(id):
    if request.method == 'GET':
        if ObjectId.is_valid(id):
            data = nilai_collection.find_one({'_id': ObjectId(id)})
            if data:
                return render_template('edit.html', nilai=data)
        return "Data tidak ditemukan", 404
    elif request.method == 'POST':
        nama = request.form['studentName']
        kelas = request.form['studentClass']
        status = request.form['status']

        nilai_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'nama': nama,
                'kelas': kelas,
                'status': status
            }}
        )
        return redirect(url_for('input_page'))


@app.route("/delete/<siswa_id>", methods=['GET', 'POST'])
def delete_data(siswa_id):
    print(f"Request received to delete siswa with id: {siswa_id}")
    if request.method == 'GET':
        if ObjectId.is_valid(siswa_id):
            try:
                # Convert siswa_id to ObjectId
                obj_id = ObjectId(siswa_id)
                print(f"Converted siswa_id to ObjectId: {obj_id}")
                # Find and delete the document
                hab = data_collection.find_one_and_delete({'_id': obj_id})
                if hab:
                    print(f"Siswa with id {siswa_id} deleted successfully: {hab}")
                    return redirect(url_for('dashboard'))
                else:
                    print(f"Siswa with id {siswa_id} not found in the database")
                    return 'Data not found', 404
            except Exception as e:
                print(f"Error occurred: {e}")
                return 'Internal Server Error', 500
        else:
            print(f"Invalid ObjectID: {siswa_id}")
            return 'Invalid ObjectID', 400
    else:
        print(f"Method not allowed for delete request")
        return 'Method not allowed', 405
    
@app.route("/delete/<absen_id>", methods=['GET', 'POST'])
def delete_data3(absen_id):
    if request.method == 'GET':
        if ObjectId.is_valid(absen_id):
            pe = absen_collection.find_one_and_delete({'_id': ObjectId(absen_id)})
            if pe:
                return redirect(url_for('dashboard'))
            else:
                return 'Data not found', 404
        else:
            return 'Invalid ObjectID', 400
    else:
        return 'Method not allowed', 405

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin_dashboard.html')
    elif current_user.role == 'petugas':
        return render_template('petugas_dashboard.html')
    elif current_user.role == 'siswa':
        return render_template('siswa_dashboard.html')
    else:
        return 'Welcome to the visitor dashboard!'
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user_data = users_collection.find_one({'username': username, 'password': password})
    if user_data:
        user = User()
        user.id = username
        user.role = user_data['role']
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid username or password'
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_doang'))

if __name__ == '__main__':
    app.run(debug=True)