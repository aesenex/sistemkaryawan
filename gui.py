import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import subprocess
from PIL import Image, ImageTk
import os

# Kelas untuk entitas Karyawan
class Karyawan:
    def __init__(self, id_karyawan, nama, jenis_kelamin, tanggal_lahir, nomor_hape, email, alamat, tanggal_join, nama_departemen):
        self.id_karyawan = id_karyawan
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin
        self.tanggal_lahir = tanggal_lahir
        self.nomor_hape = nomor_hape
        self.email = email
        self.alamat = alamat
        self.tanggal_join = tanggal_join
        self.nama_departemen = nama_departemen

# Kelas untuk entitas Departemen
class Departemen:
    def __init__(self, lot_departemen, nama, jenis, id_manager, nama_manager):
        self.lot_departemen = lot_departemen
        self.nama = nama
        self.jenis = jenis
        self.id_manager = id_manager
        self.nama_manager = nama_manager

# Kelas untuk entitas Proyek
class Proyek:
    def __init__(self, id_proyek, nama_proyek, lot_departemen, nama_departemen, tanggal_mulai, tanggal_selesai, status_proyek):
        self.id_proyek = id_proyek
        self.nama_proyek = nama_proyek
        self.lot_departemen = lot_departemen
        self.nama_departemen = nama_departemen
        self.tanggal_mulai = tanggal_mulai
        self.tanggal_selesai = tanggal_selesai
        self.status_proyek = status_proyek

# Kelas untuk entitas Absensi
class Absensi:
    def __init__(self, id_absensi, id_karyawan, tanggal_absensi, status_absensi, catatan_absensi):
        self.id_absensi = id_absensi
        self.id_karyawan = id_karyawan
        self.tanggal_absensi = tanggal_absensi
        self.status_absensi = status_absensi
        self.catatan_absensi = catatan_absensi

# Kelas untuk entitas Gaji
class Gaji:
    def __init__(self, id_gaji, id_karyawan, jumlah, tanggal):
        self.id_gaji = id_gaji
        self.id_karyawan = id_karyawan
        self.jumlah = jumlah
        self.tanggal = tanggal

class EmployeeManagementSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")

        # Database connection parameters
        self.db_params = {
            'host': '127.0.0.1',
            'user': 'root',
            'password':'',
            'database':'sistemkaryawan'
        }

        # Buat frame untuk gambar latar belakang
        self.background_frame = ttk.Frame(root)
        self.background_frame.pack(fill="both", expand=True)

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.departemen_frame = ttk.Frame(self.tab_control)
        self.absensi_frame = ttk.Frame(self.tab_control)
        self.karyawan_frame = ttk.Frame(self.tab_control)
        self.proyek_frame = ttk.Frame(self.tab_control)
        self.gaji_frame = ttk.Frame(self.tab_control)
        self.tab_control.add(self.karyawan_frame, text='Karyawan')
        self.tab_control.add(self.departemen_frame, text='Departemen')
        self.tab_control.add(self.absensi_frame, text='Absensi')
        self.tab_control.add(self.proyek_frame, text='Proyek')
        self.tab_control.add(self.gaji_frame, text='Gaji')
        self.tab_control.pack(expand=1, fill="both")

        # Mengonversi gambar latar belakang ke format yang didukung tkinter
        image_path = os.path.join("image", "depan.jpg")
        self.background_image = Image.open(image_path)
        self.background_image = self.background_image.resize((1919 , 687))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Tambahkan Canvas untuk gambar latar belakang
        self.canvas = tk.Canvas(root, width=1919 , height=687)
        self.canvas.pack(fill="both", expand=True)

        # Tambahkan gambar latar belakang ke canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Buat header_frame
        header_frame = ttk.Frame(root)

        #menempatkan header frame di atas bg frame
        header_frame.pack()

        # Lift header_frame ke atas lapisan agar tidak tertutupi oleh gambar latar belakang
        header_frame.lift()
        
        # Connect to MySQL database
        self.connection = mysql.connector.connect(**self.db_params)

        # Create widgets for each tab
        self.create_karyawan_widgets()
        self.create_departemen_widgets()
        self.create_gaji_widgets()
        self.create_proyek_widgets()
        self.create_absensi_widgets()
        

        # Buat frame untuk tombol "Log Out"
        self.logout_frame = ttk.Frame(root)
        self.logout_frame.pack(side="left", fill="x", padx=10, pady=10)

        
        # Tambahkan tombol "Log Out" di logout_frame
        self.logout_button = ttk.Button(self.logout_frame, text="Log Out", command=self.logout)
        self.logout_button.pack(side="left", padx=10, pady=10)

        
        # Lift logout_frame ke atas lapisan agar tidak tertutupi oleh gambar latar belakang
        self.logout_frame.lift()

    def logout(self):
        print("Logout Sukses")
        self.root.destroy()
        subprocess.Popen(["python", "login.py"])

    def fetch_data(self, query, params=()):
        cur = self.connection.cursor()
        cur.execute(query, params)
        records = cur.fetchall()
        cur.close()
        return records

    def execute_query(self, query, params=()):
        cur = self.connection.cursor()
        try:
            cur.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.connection.rollback()
            return False
        finally:
            cur.close()

    # Create widgets for Departemen tab
    def create_departemen_widgets(self):
        # Add search box
        self.departemen_search_label = ttk.Label(self.departemen_frame, text="Search:")
        self.departemen_search_label.pack(side="left", padx=(10, 5))
        self.departemen_search_entry = ttk.Entry(self.departemen_frame)
        self.departemen_search_entry.pack(side="left", padx=(0, 10))
        self.departemen_search_button = ttk.Button(self.departemen_frame, text="Search", command=self.search_departemen)
        self.departemen_search_button.pack(side="left")

        # Add treeview
        self.departemen_tree = ttk.Treeview(self.departemen_frame, columns=("lot_departemen", "nama", "jenis", "id_manager", "nama_manager"), show="headings")
        self.departemen_tree.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["Lot Departemen", "Nama Departemen", "Jenis Departemen", "ID Manager", "Nama Manager"]
        for col in self.departemen_tree["columns"]:
            self.departemen_tree.heading(col, text=columns[self.departemen_tree["columns"].index(col)])
            self.departemen_tree.column(col, width=100)

        self.departemen_scrollbar = ttk.Scrollbar(self.departemen_frame, orient="vertical", command=self.departemen_tree.yview)
        self.departemen_scrollbar.pack(side="right", fill="y")
        self.departemen_tree.configure(yscrollcommand=self.departemen_scrollbar.set)

        self.load_departemen_data()

        # Add buttons
        self.departemen_add_button = ttk.Button(self.departemen_frame, text="Add", command=self.add_departemen)
        self.departemen_add_button.pack(side="left", padx=10, pady=10)

        self.departemen_edit_button = ttk.Button(self.departemen_frame, text="Edit", command=self.edit_departemen)
        self.departemen_edit_button.pack(side="left", padx=10, pady=10)

        self.departemen_delete_button = ttk.Button(self.departemen_frame, text="Delete", command=self.delete_departemen)
        self.departemen_delete_button.pack(side="left", padx=10, pady=10)

        self.departemen_refresh_button = ttk.Button(self.departemen_frame, text="Refresh", command=self.load_departemen_data)
        self.departemen_refresh_button.pack(side="left", padx=10, pady=10)

        self.departemen_logout_button = ttk.Button(self.departemen_frame, text="Log Out", command=self.logout)
        self.departemen_logout_button.pack(side="left", padx=10, pady=10)

    def load_departemen_data(self):
        self.departemen_tree.delete(*self.departemen_tree.get_children())
        query = "SELECT * FROM departemen"
        departemen_records = self.fetch_data(query)
        for departemen in departemen_records:
            self.departemen_tree.insert("", "end", values=departemen)

    def search_departemen(self):
        search_term = self.departemen_search_entry.get()
        query = "SELECT * FROM departemen WHERE lotDepartemen LIKE %s OR namaDepartemen LIKE %s OR jenisDepartemen LIKE %s OR idManager LIKE %s OR namaManager LIKE %s"
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        departemen_records = self.fetch_data(query, params)

        self.departemen_tree.delete(*self.departemen_tree.get_children())
        for departemen in departemen_records:
            self.departemen_tree.insert("", "end", values=departemen)

    def add_departemen(self):
        nama = simpledialog.askstring("Input", "Masukkan Nama Departemen:")
        jenis = simpledialog.askstring("Input", "Masukkan Jenis Departemen:")
        id_manager = simpledialog.askstring("Input", "Masukkan ID Manager:")
        nama_manager = simpledialog.askstring("Input", "Masukkan Nama Manager:")

        query = "INSERT INTO departemen (namaDepartemen, jenisDepartemen, idManager, namaManager) VALUES (%s, %s, %s, %s)"
        values = (nama, jenis, id_manager, nama_manager)
        if self.execute_query(query, values):
            self.load_departemen_data()

    def edit_departemen(self):
        selected_item = self.departemen_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        lotDepartemen = self.departemen_tree.item(selected_item)['values'][0]
        nama = simpledialog.askstring("Input", "Masukkan Nama Departemen:")
        jenis = simpledialog.askstring("Input", "Masukkan Jenis Departemen:")
        id_manager = simpledialog.askstring("Input", "Masukkan ID Manager:")
        nama_manager = simpledialog.askstring("Input", "Masukkan Nama Manager:")

        query = "UPDATE departemen SET namaDepartemen=%s, jenisDepartemen=%s, idManager=%s, namaManager=%s WHERE lotDepartemen=%s"
        values = (lotDepartemen,nama, jenis, id_manager, nama_manager)
        if self.execute_query(query, values):
            self.load_departemen_data()

    def delete_departemen(self):
        selected_item = self.departemen_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        departemen_id = self.departemen_tree.item(selected_item)['values'][0]
        query = "DELETE FROM departemen WHERE lotDepartemen=%s"
        if self.execute_query(query, (departemen_id,)):
            self.load_departemen_data()

    # Create widgets for Gaji tab
    def create_gaji_widgets(self):
        # Add search box
        self.gaji_search_label = ttk.Label(self.gaji_frame, text="Search:")
        self.gaji_search_label.pack(side="left", padx=(10, 5))
        self.gaji_search_entry = ttk.Entry(self.gaji_frame)
        self.gaji_search_entry.pack(side="left", padx=(0, 10))
        self.gaji_search_button = ttk.Button(self.gaji_frame, text="Search", command=self.search_gaji)
        self.gaji_search_button.pack(side="left")

        # Add treeview
        self.gaji_tree = ttk.Treeview(self.gaji_frame, columns=("id_gaji", "id_karyawan", "jumlah", "tanggal"), show="headings")
        self.gaji_tree.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID Gaji", "ID Karyawan", "Jumlah", "Tanggal"]
        for col in self.gaji_tree["columns"]:
            self.gaji_tree.heading(col, text=columns[self.gaji_tree["columns"].index(col)])
            self.gaji_tree.column(col, width=100)

        self.gaji_scrollbar = ttk.Scrollbar(self.gaji_frame, orient="vertical", command=self.gaji_tree.yview)
        self.gaji_scrollbar.pack(side="right", fill="y")
        self.gaji_tree.configure(yscrollcommand=self.gaji_scrollbar.set)
       

        self.load_gaji_data()

        # Add buttons
        self.gaji_add_button = ttk.Button(self.gaji_frame, text="Add", command=self.add_gaji)
        self.gaji_add_button.pack(side="left", padx=10, pady=10)

        self.gaji_edit_button = ttk.Button(self.gaji_frame, text="Edit", command=self.edit_gaji)
        self.gaji_edit_button.pack(side="left", padx=10, pady=10)

        self.gaji_delete_button = ttk.Button(self.gaji_frame, text="Delete", command=self.delete_gaji)
        self.gaji_delete_button.pack(side="left", padx=10, pady=10)

        self.gaji_refresh_button = ttk.Button(self.gaji_frame, text="Refresh", command=self.load_gaji_data)
        self.gaji_refresh_button.pack(side="left", padx=10, pady=10)

        self.gaji_logout_button = ttk.Button(self.gaji_frame, text="Log Out", command=self.logout)
        self.gaji_logout_button.pack(side="left", padx=10, pady=10)

    def load_gaji_data(self):
        self.gaji_tree.delete(*self.gaji_tree.get_children())
        query = "SELECT * FROM gaji"
        gaji_records = self.fetch_data(query)
        for gaji in gaji_records:
            self.gaji_tree.insert("", "end", values=gaji)

    def search_gaji(self):
        search_term = self.gaji_search_entry.get()
        query = "SELECT * FROM gaji WHERE idGaji LIKE %s OR idKaryawan LIKE %s OR jumlah LIKE %s OR tanggal LIKE %s"
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        gaji_records = self.fetch_data(query, params)

        self.gaji_tree.delete(*self.gaji_tree.get_children())
        for gaji in gaji_records:
            self.gaji_tree.insert("", "end", values=gaji)

    def add_gaji(self):
        id_karyawan = simpledialog.askstring("Input", "Masukkan ID Karyawan:")
        jumlah = simpledialog.askstring("Input", "Masukkan Jumlah Gaji:")
        tanggal = simpledialog.askstring("Input", "Masukkan Tanggal (YYYY-MM-DD):")

        query = "INSERT INTO gaji (idKaryawan, jumlah, tanggal) VALUES (%s, %s, %s)"
        values = (id_karyawan, jumlah, tanggal)
        if self.execute_query(query, values):
            self.load_gaji_data()

    def edit_gaji(self):
        selected_item = self.gaji_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        gaji_id = self.gaji_tree.item(selected_item)['values'][0]
        id_karyawan = simpledialog.askstring("Input", "Masukkan ID Karyawan:")
        jumlah = simpledialog.askstring("Input", "Masukkan Jumlah Gaji:")
        tanggal = simpledialog.askstring("Input", "Masukkan Tanggal (YYYY-MM-DD):")

        query = "UPDATE gaji SET idKaryawan=%s, jumlah=%s, tanggal=%s WHERE idGaji=%s"
        values = (id_karyawan, jumlah, tanggal, gaji_id)
        if self.execute_query(query, values):
            self.load_gaji_data()

    def delete_gaji(self):
        selected_item = self.gaji_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        gaji_id = self.gaji_tree.item(selected_item)['values'][0]
        query = "DELETE FROM gaji WHERE idGaji=%s"
        if self.execute_query(query, (gaji_id,)):
            self.load_gaji_data()

    # Create widgets for Karyawan tab
    def create_karyawan_widgets(self):
        # Add search box
        self.karyawan_search_label = ttk.Label(self.karyawan_frame, text="Search:")
        self.karyawan_search_label.pack(side="left", padx=(10, 5))
        self.karyawan_search_entry = ttk.Entry(self.karyawan_frame)
        self.karyawan_search_entry.pack(side="left", padx=(0, 10))
        self.karyawan_search_button = ttk.Button(self.karyawan_frame, text="Search", command=self.search_karyawan)
        self.karyawan_search_button.pack(side="left")

        # Add treeview
        self.karyawan_tree = ttk.Treeview(self.karyawan_frame, columns=("id_karyawan", "nama", "jenis_kelamin", "tanggal_lahir", "nomor_hape", "email", "alamat", "tanggal_join", "nama_departemen"), show="headings")
        self.karyawan_tree.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID Karyawan", "Nama", "Jenis Kelamin", "Tanggal Lahir", "Nomor HP", "Email", "Alamat", "Tanggal Join", "Nama Departemen"]
        for col in self.karyawan_tree["columns"]:
            self.karyawan_tree.heading(col, text=columns[self.karyawan_tree["columns"].index(col)])
            self.karyawan_tree.column(col, width=100)

        self.karyawan_scrollbar = ttk.Scrollbar(self.karyawan_frame, orient="vertical", command=self.karyawan_tree.yview)
        self.karyawan_scrollbar.pack(side="right", fill="y")
        self.karyawan_tree.configure(yscrollcommand=self.karyawan_scrollbar.set)

        self.load_karyawan_data()

        # Add buttons
        self.karyawan_add_button = ttk.Button(self.karyawan_frame, text="Add", command=self.add_karyawan)
        self.karyawan_add_button.pack(side="left", padx=10, pady=10)

        self.karyawan_edit_button = ttk.Button(self.karyawan_frame, text="Edit", command=self.edit_karyawan)
        self.karyawan_edit_button.pack(side="left", padx=10, pady=10)

        self.karyawan_delete_button = ttk.Button(self.karyawan_frame, text="Delete", command=self.delete_karyawan)
        self.karyawan_delete_button.pack(side="left", padx=10, pady=10)

        self.karyawan_refresh_button = ttk.Button(self.karyawan_frame, text="Refresh", command=self.load_karyawan_data)
        self.karyawan_refresh_button.pack(side="left", padx=10, pady=10)

        self.karyawan_logout_button = ttk.Button(self.karyawan_frame, text="Log Out", command=self.logout)
        self.karyawan_logout_button.pack(side="left", padx=10, pady=10)

    def load_karyawan_data(self):
        self.karyawan_tree.delete(*self.karyawan_tree.get_children())
        query = "SELECT * FROM karyawan"
        karyawan_records = self.fetch_data(query)
        for karyawan in karyawan_records:
            self.karyawan_tree.insert("", "end", values=karyawan)

    def search_karyawan(self):
        search_term = self.karyawan_search_entry.get()
        query = "SELECT * FROM karyawan WHERE idKaryawan LIKE %s OR nama LIKE %s OR jenisKelamin LIKE %s OR tanggalLahir LIKE %s OR nomorHape LIKE %s OR email LIKE %s OR alamat LIKE %s OR tanggalJoin LIKE %s OR namaDepartemen LIKE %s"
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        karyawan_records = self.fetch_data(query, params)

        self.karyawan_tree.delete(*self.karyawan_tree.get_children())
        for karyawan in karyawan_records:
            self.karyawan_tree.insert("", "end", values=karyawan)

    def add_karyawan(self):
        id_karyawan = simpledialog.askinteger("Input", "Masukkan ID Karyawan:")
        nama_karyawan = simpledialog.askstring("Input", "Masukkan Nama Karyawan:")
        jeniskelamin = simpledialog.asktstring("input", "Masukan Jenis Kelamin (L/P) :")
        tanggal_lahir = simpledialog.askstring("Input", "Masukkan Tanggal Lahir (YYYY-MM-DD):")
        nomor_hape = simpledialog.askstring("Input", "Masukkan Nomor HP:")
        email_karyawan = simpledialog.askstring("Input", "Masukkan Email:")
        alamat_karyawan = simpledialog.askstring("Input", "Masukkan Alamat:")
        tanggal_join = simpledialog.askstring("Input", "Masukkan Tanggal Join (YYYY-MM-DD):")
        nama_departemen = simpledialog.askstring("Input", "Masukkan Nama Departemen:")

        query = "INSERT INTO karyawan (IdKaryawan, namaKaryawan, jenisKelamin,tanggalLahir, nomorHape, emailKaryawan, alamatKaryawan, tanggalJoin, namaDepartemen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (id_karyawan, nama_karyawan, tanggal_lahir,jeniskelamin, nomor_hape, email_karyawan, alamat_karyawan, tanggal_join, nama_departemen)
        if self.execute_query(query, values):
            self.load_karyawan_data()

    def edit_karyawan(self):
        selected_item = self.karyawan_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        karyawan_id = self.karyawan_tree.item(selected_item)['values'][0]
        id_karyawan = simpledialog.askinteger("Input", "Masukkan ID Karyawan:")
        nama_karyawan = simpledialog.askstring("Input", "Masukkan Nama Karyawan:")
        jeniskelamin = simpledialog.asktstring("input", "Masukan Jenis Kelamin (L/P) :")
        tanggal_lahir = simpledialog.askstring("Input", "Masukkan Tanggal Lahir (YYYY-MM-DD):")
        nomor_hape = simpledialog.askstring("Input", "Masukkan Nomor HP:")
        email_karyawan = simpledialog.askstring("Input", "Masukkan Email:")
        alamat_karyawan = simpledialog.askstring("Input", "Masukkan Alamat:")
        tanggal_join = simpledialog.askstring("Input", "Masukkan Tanggal Join (YYYY-MM-DD):")
        nama_departemen = simpledialog.askstring("Input", "Masukkan Nama Departemen:")

        query = "UPDATE karyawan SET IdKaryawan=%s, namaKaryawan=%s,jenisKelamin=%s tanggalLahir=%s, nomorHape=%s, emailKaryawan=%s, alamatKaryawan=%s, tanggalJoin=%s, namaDepartemen=%s WHERE IdKaryawan=%s"
        values = (id_karyawan, nama_karyawan,jeniskelamin, tanggal_lahir, nomor_hape, email_karyawan, alamat_karyawan, tanggal_join, nama_departemen, karyawan_id)
        if self.execute_query(query, values):
            self.load_karyawan_data()

    def delete_karyawan(self):
        selected_item = self.karyawan_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        karyawan_id = self.karyawan_tree.item(selected_item)['values'][0]
        query = "DELETE FROM karyawan WHERE IdKaryawan=%s"
        if self.execute_query(query, (karyawan_id,)):
            self.load_karyawan_data()


    # Create widgets for Proyek tab
    def create_proyek_widgets(self):
        # Add search box
        self.proyek_search_label = ttk.Label(self.proyek_frame, text="Search:")
        self.proyek_search_label.pack(side="left", padx=(10, 5))
        self.proyek_search_entry = ttk.Entry(self.proyek_frame)
        self.proyek_search_entry.pack(side="left", padx=(0, 10))
        self.proyek_search_button = ttk.Button(self.proyek_frame, text="Search", command=self.search_proyek)
        self.proyek_search_button.pack(side="left")

        # Add treeview
        self.proyek_tree = ttk.Treeview(self.proyek_frame, columns=("id_proyek", "nama_proyek", "lot_departemen", "nama_departemen", "tanggal_mulai", "tanggal_selesai", "status_proyek"), show="headings")
        self.proyek_tree.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID Proyek", "Nama Proyek", "Lot Departemen", "Nama Departemen", "Tanggal Mulai", "Tanggal Selesai", "Status Proyek"]
        for col in self.proyek_tree["columns"]:
            self.proyek_tree.heading(col, text=columns[self.proyek_tree["columns"].index(col)])
            self.proyek_tree.column(col, width=100)

        self.proyek_scrollbar = ttk.Scrollbar(self.proyek_frame, orient="vertical", command=self.proyek_tree.yview)
        self.proyek_scrollbar.pack(side="right", fill="y")
        self.proyek_tree.configure(yscrollcommand=self.proyek_scrollbar.set)

        self.load_proyek_data()

        # Add buttons
        self.proyek_add_button = ttk.Button(self.proyek_frame, text="Add", command=self.add_proyek)
        self.proyek_add_button.pack(side="left", padx=10, pady=10)

        self.proyek_edit_button = ttk.Button(self.proyek_frame, text="Edit", command=self.edit_proyek)
        self.proyek_edit_button.pack(side="left", padx=10, pady=10)

        self.proyek_delete_button = ttk.Button(self.proyek_frame, text="Delete", command=self.delete_proyek)
        self.proyek_delete_button.pack(side="left", padx=10, pady=10)

        self.proyek_refresh_button = ttk.Button(self.proyek_frame, text="Refresh", command=self.load_proyek_data)
        self.proyek_refresh_button.pack(side="left", padx=10, pady=10)

        self.proyek_logout_button = ttk.Button(self.proyek_frame, text="Log Out", command=self.logout)
        self.proyek_logout_button.pack(side="left", padx=10, pady=10)

    def load_proyek_data(self):
        self.proyek_tree.delete(*self.proyek_tree.get_children())
        query = "SELECT * FROM proyek"
        proyek_records = self.fetch_data(query)
        for proyek in proyek_records:
            self.proyek_tree.insert("", "end", values=proyek)

    def search_proyek(self):
        search_term = self.proyek_search_entry.get()
        query = "SELECT * FROM proyek WHERE idProyek LIKE %s OR namaProyek LIKE %s OR lotDepartemen LIKE %s OR namaDepartemen LIKE %s OR tanggalMulai LIKE %s OR tanggalSelesai LIKE %s OR statusProyek LIKE %s"
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        proyek_records = self.fetch_data(query, params)

        self.proyek_tree.delete(*self.proyek_tree.get_children())
        for proyek in proyek_records:
            self.proyek_tree.insert("", "end", values=proyek)

    def add_proyek(self):
        nama_proyek = simpledialog.askstring("Input", "Masukkan Nama Proyek:")
        lot_departemen = simpledialog.askstring("Input", "Masukkan Lot Departemen:")
        nama_departemen = simpledialog.askstring("Input", "Masukkan Nama Departemen:")
        tanggal_mulai = simpledialog.askstring("Input", "Masukkan Tanggal Mulai (YYYY-MM-DD):")
        tanggal_selesai = simpledialog.askstring("Input", "Masukkan Tanggal Selesai (YYYY-MM-DD):")
        status_proyek = simpledialog.askstring("Input", "Masukkan Status Proyek:")

        query = "INSERT INTO proyek (namaProyek, lotDepartemen, namaDepartemen, tanggalMulai, tanggalSelesai, statusProyek) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (nama_proyek, lot_departemen, nama_departemen, tanggal_mulai, tanggal_selesai, status_proyek)
        if self.execute_query(query, values):
            self.load_proyek_data()

    def edit_proyek(self):
        selected_item = self.proyek_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        proyek_id = self.proyek_tree.item(selected_item)['values'][0]
        nama_proyek = simpledialog.askstring("Input", "Masukkan Nama Proyek:")
        lot_departemen = simpledialog.askstring("Input", "Masukkan Lot Departemen:")
        nama_departemen = simpledialog.askstring("Input", "Masukkan Nama Departemen:")
        tanggal_mulai = simpledialog.askstring("Input", "Masukkan Tanggal Mulai (YYYY-MM-DD):")
        tanggal_selesai = simpledialog.askstring("Input", "Masukkan Tanggal Selesai (YYYY-MM-DD):")
        status_proyek = simpledialog.askstring("Input", "Masukkan Status Proyek:")

        query = "UPDATE proyek SET namaProyek=%s, lotDepartemen=%s, namaDepartemen=%s, tanggalMulai=%s, tanggalSelesai=%s, statusProyek=%s WHERE idProyek=%s"
        values = (nama_proyek, lot_departemen, nama_departemen, tanggal_mulai, tanggal_selesai, status_proyek, proyek_id)
        if self.execute_query(query, values):
            self.load_proyek_data()

    def delete_proyek(self):
        selected_item = self.proyek_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        proyek_id = self.proyek_tree.item(selected_item)['values'][0]
        query = "DELETE FROM proyek WHERE idProyek=%s"
        if self.execute_query(query, (proyek_id,)):
            self.load_proyek_data()

    # Create widgets for Absensi tab
    def create_absensi_widgets(self):
        # Add search box
        self.absensi_search_label = ttk.Label(self.absensi_frame, text="Search:")
        self.absensi_search_label.pack(side="left", padx=(10, 5))
        self.absensi_search_entry = ttk.Entry(self.absensi_frame)
        self.absensi_search_entry.pack(side="left", padx=(0, 10))
        self.absensi_search_button = ttk.Button(self.absensi_frame, text="Search", command=self.search_absensi)
        self.absensi_search_button.pack(side="left")

        # Add treeview
        self.absensi_tree = ttk.Treeview(self.absensi_frame, columns=("id_absensi", "id_karyawan", "tanggal_absensi", "status_absensi", "catatan_absensi"), show="headings")
        self.absensi_tree.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ["ID Absensi", "ID Karyawan", "Tanggal Absensi", "Status Absensi", "Catatan Absensi"]
        for col in self.absensi_tree["columns"]:
            self.absensi_tree.heading(col, text=columns[self.absensi_tree["columns"].index(col)])
            self.absensi_tree.column(col, width=100)

        self.absensi_scrollbar = ttk.Scrollbar(self.absensi_frame, orient="vertical", command=self.absensi_tree.yview)
        self.absensi_scrollbar.pack(side="right", fill="y")
        self.absensi_tree.configure(yscrollcommand=self.absensi_scrollbar.set)

        self.load_absensi_data()

        # Add buttons
        self.absensi_add_button = ttk.Button(self.absensi_frame, text="Add", command=self.add_absensi)
        self.absensi_add_button.pack(side="left", padx=10, pady=10)

        self.absensi_edit_button = ttk.Button(self.absensi_frame, text="Edit", command=self.edit_absensi)
        self.absensi_edit_button.pack(side="left", padx=10, pady=10)

        self.absensi_delete_button = ttk.Button(self.absensi_frame, text="Delete", command=self.delete_absensi)
        self.absensi_delete_button.pack(side="left", padx=10, pady=10)

        self.absensi_refresh_button = ttk.Button(self.absensi_frame, text="Refresh", command=self.load_absensi_data)
        self.absensi_refresh_button.pack(side="left", padx=10, pady=10)

        self.absensi_logout_button = ttk.Button(self.absensi_frame, text="Log Out", command=self.logout)
        self.absensi_logout_button.pack(side="left", padx=10, pady=10)

    def load_absensi_data(self):
        self.absensi_tree.delete(*self.absensi_tree.get_children())
        query = "SELECT * FROM absensi"
        absensi_records = self.fetch_data(query)
        for absensi in absensi_records:
            self.absensi_tree.insert("", "end", values=absensi)

    def search_absensi(self):
        search_term = self.absensi_search_entry.get()
        query = "SELECT * FROM absensi WHERE idAbsensi LIKE %s OR idKaryawan LIKE %s OR tanggalAbsensi LIKE %s OR statusAbsensi LIKE %s OR catatanAbsensi LIKE %s"
        params = (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
        absensi_records = self.fetch_data(query, params)

        self.absensi_tree.delete(*self.absensi_tree.get_children())
        for absensi in absensi_records:
            self.absensi_tree.insert("", "end", values=absensi)

    def add_absensi(self):
        id_karyawan = simpledialog.askstring("Input", "Masukkan ID Karyawan:")
        tanggal_absensi = simpledialog.askstring("Input", "Masukkan Tanggal Absensi (YYYY-MM-DD):")
        status_absensi = simpledialog.askstring("Input", "Masukkan Status Absensi:")
        catatan_absensi = simpledialog.askstring("Input", "Masukkan Catatan Absensi:")

        query = "INSERT INTO absensi (idKaryawan, tanggalAbsensi, statusAbsensi, catatanAbsensi) VALUES (%s, %s, %s, %s)"
        values = (id_karyawan, tanggal_absensi, status_absensi, catatan_absensi)
        if self.execute_query(query, values):
            self.load_absensi_data()

    def edit_absensi(self):
        selected_item = self.absensi_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        absensi_id = self.absensi_tree.item(selected_item)['values'][0]
        id_karyawan = simpledialog.askstring("Input", "Masukkan ID Karyawan:")
        tanggal_absensi = simpledialog.askstring("Input", "Masukkan Tanggal Absensi (YYYY-MM-DD):")
        status_absensi = simpledialog.askstring("Input", "Masukkan Status Absensi:")
        catatan_absensi = simpledialog.askstring("Input", "Masukkan Catatan Absensi:")

        query = "UPDATE absensi SET idKaryawan=%s, tanggalAbsensi=%s, statusAbsensi=%s, catatanAbsensi=%s WHERE idAbsensi=%s"
        values = (id_karyawan, tanggal_absensi, status_absensi, catatan_absensi, absensi_id)
        if self.execute_query(query, values):
            self.load_absensi_data()

    def delete_absensi(self):
        selected_item = self.absensi_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return

        absensi_id = self.absensi_tree.item(selected_item)['values'][0]
        query = "DELETE FROM absensi WHERE idAbsensi=%s"
        if self.execute_query(query, (absensi_id,)):
            self.load_absensi_data()

root = tk.Tk()
app = EmployeeManagementSystemApp(root)
root.mainloop()

