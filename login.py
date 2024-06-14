import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import subprocess
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Employee Management System")
        self.root.geometry("1920x1080")

        # Setup the background for the main window (login)
        self.setup_main_background()

        # Header Frame
        header_frame = ttk.Frame(root)
        header_frame.place(relx=0.5, rely=0.10, anchor=tk.N)

        # Header Label
        
        # Canvas untuk latar belakang
        self.canvas = tk.Canvas(root, width=1920, height=1080)
        self.canvas.place(x=0, y=0)

        # Mendapatkan path lengkap ke gambar belakang
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "image", "belakang.jpg")

        # Mengonversi gambar latar belakang ke format yang didukung tkinter
        self.background_image = Image.open(image_path)
        self.background_image = self.background_image.resize((1920, 1080))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Menambahkan gambar belakang ke canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Lift header_frame ke atas lapisan agar tidak tertutupi oleh gambar latar belakang
        header_frame.lift()

        # Form Frame
        form_frame = ttk.Frame(root)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Label dan Entry untuk Username
        self.email_label = ttk.Label(form_frame, text="Username *")
        self.email_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ttk.Entry(form_frame)
        self.entry_email.grid(row=0, column=1, padx=10, pady=5)

        # Label dan Entry untuk Password
        self.password_label = ttk.Label(form_frame, text="Password *")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_password = ttk.Entry(form_frame, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        # Checkbox Frame
        checkbox_frame = ttk.Frame(root)
        checkbox_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Checkbutton "Ingat Saya"
        self.remember_me = ttk.Checkbutton(checkbox_frame, text="Ingat Saya")
        self.remember_me.grid(row=0, column=0, padx=5)

        # Label "Lupa Password"
        self.forgot_password = ttk.Label(checkbox_frame, text="Lupa Password", cursor="hand2")
        self.forgot_password.grid(row=0, column=1, padx=5)
        self.forgot_password.bind("<Button-1>", lambda e: self.show_forgot_password_window())

        # Login Button
        self.login_button = ttk.Button(root, text="Masuk", command=self.on_login)
        self.login_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Register Label
        self.register_label = ttk.Label(root, text="Belum memiliki akun ?", cursor="hand2")
        self.register_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        self.register_label.bind("<Button-1>", lambda e: self.show_register_window())

        # Buat jendela pendaftaran, tapi sembunyikan dulu
        self.register_window = None

    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="login"
            )
            print("Koneksi ke database berhasil")
            return conn
        except mysql.connector.Error as err:
            print("Error:", err)
            return None

    def on_login(self):
        username = self.entry_email.get()
        password = self.entry_password.get()
        if username and password:
            conn = self.connect_to_database()
            if conn:
                if self.login(conn, username, password):
                    conn.close()
                    self.hide_login_window()  # Panggil fungsi untuk menyembunyikan jendela login
                    self.switch_to_gui()  # Panggil fungsi untuk beralih ke gui.py
        else:
            messagebox.showwarning("Peringatan", "Mohon isi username dan password.")

    def login(self, conn, username, password):
        try:
            cursor = conn.cursor()
            find_user_query = """
            SELECT * FROM users
            WHERE username = %s AND password = %s
            """
            data = (username, password)
            cursor.execute(find_user_query, data)
            user = cursor.fetchone()
            if user:
                print("Login berhasil")
                messagebox.showinfo("Login Berhasil", "Selamat datang! Login berhasil.")
                return True
            else:
                print("Login gagal")
                messagebox.showwarning("Login Gagal", "Username dan password Anda salah.")
                return False
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "Terjadi kesalahan. Silakan coba lagi.")
            return False

    def hide_login_window(self):
        self.root.withdraw()  # Menyembunyikan jendela login setelah login berhasil

    def show_login_window(self):
        self.root.deiconify()  # Menampilkan kembali jendela login

    def switch_to_gui(self):
        try:
            subprocess.run(["python", "gui.py"])
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Error", "Gagal beralih ke Tampilan . Silakan coba lagi.")

    def setup_main_background(self):
        # Get the complete path to the background image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "image", "belakang.jpg")

        # Convert the background image to a format supported by tkinter
        self.main_background_image = Image.open(image_path)
        self.main_background_image = self.main_background_image.resize((1920, 1080))
        self.main_background_photo = ImageTk.PhotoImage(self.main_background_image)

        # Create a Canvas widget for the main window background
        self.main_canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.main_canvas.place(x=0, y=0)

        # Add the image to the main window canvas
        self.main_canvas.create_image(0, 0, anchor=tk.NW, image=self.main_background_photo)

    def show_register_window(self):
        self.hide_login_window()  # Sembunyikan jendela login saat membuka jendela pendaftaran
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Register")
        self.register_window.geometry("1920x1080")

        # Get the complete path to the background image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "image", "belakang.jpg")

        # Convert the background image to a format supported by tkinter
        self.register_background_image = Image.open(image_path)
        self.register_background_image = self.register_background_image.resize((1920, 1080))
        self.register_background_photo = ImageTk.PhotoImage(self.register_background_image)

        # Create a Canvas widget for the register window background
        self.register_canvas = tk.Canvas(self.register_window, width=1920, height=1080)
        self.register_canvas.pack(fill="both", expand=True)

        # Add the image to the register window canvas
        self.register_canvas.create_image(0, 0, anchor="nw", image=self.register_background_photo)

        #Header Frame
        header_frame = ttk.Frame(self.register_window)
        header_frame.place(relx=0.5, rely=0.10, anchor=tk.N)    

        
        # Form Frame
        form_frame = ttk.Frame(self.register_window)
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create and place widgets on the register window canvas
        name_label = ttk.Label(form_frame, text="Nama Lengkap:")
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        email_label = ttk.Label(form_frame, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        username_label = ttk.Label(form_frame, text="Username:")
        username_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)

        password_label = ttk.Label(form_frame, text="Password:")
        password_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = ttk.Entry(form_frame, show='*')
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        show_password_checkbox = ttk.Checkbutton(form_frame, text="Lihat Password", command=self.toggle_password)
        show_password_checkbox.grid(row=4, column=1, padx=10, pady=5)

        register_button = ttk.Button(self.register_window, text="Daftar", command=self.on_register)
        register_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)  # Menggunakan posisi yang sama dengan tombol login

        # Add Back Button
        back_button = ttk.Button(self.register_window, text="Kembali", command=self.on_back)
        back_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)  # Menggunakan posisi yang sama dengan label register

    def on_back(self):
        self.register_window.destroy()  # Close the register window
        self.show_login_window()  # Show the login window again

    def toggle_password(self):
        if self.password_entry.cget('show') == '':
            self.password_entry.config(show='*')
        else:
            self.password_entry.config(show='')

    def on_register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if name and email and username and password:
            conn = self.connect_to_database()
            if conn:
                self.register(conn, name, email, username, password)
                conn.close()
                self.show_login_window()  # Tampilkan kembali jendela login setelah registrasi berhasil
                self.register_window.destroy()  # Close the register window after registration
        else:
            messagebox.showwarning("Peringatan", "Mohon lengkapi semua kolom.")

    def register(self, conn, name, email, username, password):
        try:
            cursor = conn.cursor()
            register_query = """
            INSERT INTO users (name, email, username, password)
            VALUES (%s, %s, %s, %s)
            """
            data = (name, email, username, password)
            cursor.execute(register_query, data)
            conn.commit()
            print("Pendaftaran berhasil")
            messagebox.showinfo("Registrasi Berhasil", "Registrasi berhasil. Silakan login.")
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "Registrasi gagal. Silakan coba lagi.")

    def show_forgot_password_window(self):
        self.forgot_password_window = tk.Toplevel(self.root)
        self.forgot_password_window.title("Lupa Password")
        self.forgot_password_window.geometry("300x200")

        username_label = ttk.Label(self.forgot_password_window, text="Username:")
        username_label.pack(pady=5)
        self.username_entry_forgot = ttk.Entry(self.forgot_password_window)
        self.username_entry_forgot.pack(pady=5)

        new_password_label = ttk.Label(self.forgot_password_window, text="New Password:")
        new_password_label.pack(pady=5)
        self.new_password_entry = ttk.Entry(self.forgot_password_window, show='*')
        self.new_password_entry.pack(pady=5)

        confirm_button = ttk.Button(self.forgot_password_window, text="Confirm", command=self.on_confirm_password_change)
        confirm_button.pack(pady=10)

    def on_confirm_password_change(self):
        username = self.username_entry_forgot.get()
        new_password = self.new_password_entry.get()

        if username and new_password:
            conn = self.connect_to_database()
            if conn:
                self.change_password(conn, username, new_password)
                conn.close()
        else:
            messagebox.showwarning("Peringatan", "Mohon lengkapi semua kolom.")

    def change_password(self, conn, username, new_password):
        try:
            cursor = conn.cursor()
            update_query = """
            UPDATE users
            SET password = %s
            WHERE username = %s
            """
            data = (new_password, username)
            cursor.execute(update_query, data)
            conn.commit()
            print("Password berhasil diubah")
            messagebox.showinfo("Berhasil", "Password berhasil diubah.")
            self.forgot_password_window.destroy()  # Menutup jendela lupa password setelah berhasil mengubah password
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "Gagal mengubah password. Silakan coba lagi.")


root = tk.Tk()

app = LoginApp(root)
root.mainloop()
