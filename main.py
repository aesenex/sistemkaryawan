import login
import gui
import databaseconfig
import tkinter as tk

def main():
    print("Aplikasi Employee Management System")

    # Konfigurasi database
    db_config = databaseconfig.DatabaseConfig()
    db_config.configure_database()

    # Buat jendela utama Tkinter
    root = tk.Tk()

    # Eksekusi modul karyawan
    app = gui.EmployeeManagementSystemApp(root)

    # Eksekusi modul login
    login.LoginApp()

    # Jalankan aplikasi Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()


