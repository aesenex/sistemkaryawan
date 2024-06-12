import mysql.connector

class DatabaseConfig:
    def __init__(self):
        self.db_params = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',  # Ganti dengan password yang sesuai
            'database': 'sistemkaryawan',
        }

    def configure_database(self):
        try:
            self.conn = mysql.connector.connect(**self.db_params)
            print("Koneksi database berhasil")
            return self.conn
        except mysql.connector.Error as err:
            print(f"Terjadi kesalahan: {err}")
            return None