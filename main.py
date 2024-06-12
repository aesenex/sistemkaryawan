import login
import gui
import databaseconfig

def main():
    print("Aplikasi Employee Management System")

    # Konfigurasi database
    db_config = databaseconfig.DatabaseConfig()
    db_config.configure_database()

     # Eksekusi modul karyawan
    gui.EmployeeManagementSystemApp()  # Ganti dengan nama fungsi atau kelas yang sesuai

    # Eksekusi modul login
    login.LoginApp()  # Ganti dengan nama fungsi atau kelas yang sesuai

   
if __name__ == "__main__":
    main()
