import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Kelas Manajemen Keuangan
class Keuangan:
    def __init__(self, file_csv):
        # Membaca data keuangan dari file CSV
        self.transaksi = pd.read_csv(file_csv)
        
    def tambah_transaksi(self, tanggal, jenis, jumlah, keterangan):
        # Menambah transaksi baru ke DataFrame
        transaksi_baru = pd.DataFrame([[tanggal, jenis, jumlah, keterangan]], columns=self.transaksi.columns)
        self.transaksi = pd.concat([self.transaksi, transaksi_baru], ignore_index=True)

    def simpan_transaksi(self, file_csv):
        # Menyimpan data transaksi ke CSV
        self.transaksi.to_csv(file_csv, index=False)

    def laporan_keuangan(self):
        # Menghitung total pemasukan, pengeluaran, dan saldo akhir
        pemasukan = self.transaksi[self.transaksi["Jenis"] == "Pemasukan"]["Jumlah"].sum()
        pengeluaran = self.transaksi[self.transaksi["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
        saldo_akhir = pemasukan - pengeluaran
        return pemasukan, pengeluaran, saldo_akhir

    def tampilkan_laporan(self):
        # Menampilkan laporan keuangan
        return self.transaksi

# Kelas Pengelolaan Stok
class Stok:
    def __init__(self, file_csv):
        # Membaca data stok dari file CSV
        self.stok_barang = pd.read_csv(file_csv)
        
    def tambah_barang(self, kode, nama, jumlah, harga):
        # Menambah barang baru ke DataFrame
        barang_baru = pd.DataFrame([[kode, nama, jumlah, harga]], columns=self.stok_barang.columns)
        self.stok_barang = pd.concat([self.stok_barang, barang_baru], ignore_index=True)

    def update_stok(self, kode, jumlah):
        # Memperbarui jumlah stok barang berdasarkan kode
        self.stok_barang.loc[self.stok_barang["Kode Barang"] == kode, "Jumlah"] += jumlah

    def simpan_stok(self, file_csv):
        # Menyimpan data stok barang ke CSV
        self.stok_barang.to_csv(file_csv, index=False)

    def laporan_stok(self):
        # Menghasilkan laporan stok barang
        return self.stok_barang

    def tampilkan_laporan(self):
        # Menampilkan laporan stok barang
        return self.stok_barang

# Fungsi Analisa Stok dan Keuangan
def analisa_keuangan_ke_stok(keuangan, stok):
    pemasukan, pengeluaran, saldo_akhir = keuangan.laporan_keuangan()
    total_nilai_stok = (stok.stok_barang["Jumlah"] * stok.stok_barang["Harga"]).sum()
    
    warning = ""
    if saldo_akhir < total_nilai_stok:
        warning = "Peringatan: Saldo tidak cukup untuk menutupi nilai stok barang!"
    
    return total_nilai_stok, saldo_akhir, warning

# Fungsi untuk Visualisasi Keuangan
def visualisasi_keuangan(keuangan):
    pemasukan, pengeluaran, saldo_akhir = keuangan.laporan_keuangan()
    data = [pemasukan, pengeluaran, saldo_akhir]
    labels = ["Pemasukan", "Pengeluaran", "Saldo Akhir"]

    fig, ax = plt.subplots()
    ax.bar(labels, data, color=["green", "red", "blue"])
    ax.set_title("Visualisasi Laporan Keuangan")
    ax.set_ylabel("Jumlah")
    
    # Menampilkan plot dengan Streamlit
    st.pyplot(fig)

# URL mentah dari file CSV di GitHub
keuangan_url = "https://raw.githubusercontent.com/Kaepci/kupengenmeletup/refs/heads/main/keuangan.csv"
stok_url = "https://raw.githubusercontent.com/Kaepci/kupengenmeletup/refs/heads/main/stok.csv"

# Membaca file CSV langsung dari GitHub
keuangan = Keuangan(keuangan_url)
stok = Stok(stok_url)

# Streamlit UI untuk memperbarui CSV
def app():
    st.title('Manajemen Keuangan dan Stok')

    # Menampilkan laporan keuangan
    pemasukan, pengeluaran, saldo_akhir = keuangan.tampilkan_laporan()
    st.subheader("Laporan Keuangan")
    st.write(f"Pemasukan: {pemasukan}")
    st.write(f"Pengeluaran: {pengeluaran}")
    st.write(f"Saldo Akhir: {saldo_akhir}")

    # Menampilkan laporan stok
    st.subheader("Laporan Stok Barang")
    st.write(stok.tampilkan_laporan())

    # Mengedit transaksi keuangan
    st.subheader("Edit Transaksi Keuangan")
    with st.form(key='keuangan_form'):
        tanggal = st.date_input("Tanggal")
        jenis = st.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        jumlah = st.number_input("Jumlah", min_value=0)
        keterangan = st.text_input("Keterangan")
        submit_button = st.form_submit_button(label='Tambah Transaksi')

        if submit_button:
            keuangan.tambah_transaksi(str(tanggal), jenis, jumlah, keterangan)
            keuangan.simpan_transaksi(keuangan_url)
            st.success("Transaksi berhasil ditambahkan!")
    
    # Mengedit stok barang
    st.subheader("Edit Stok Barang")
    with st.form(key='stok_form'):
        kode_barang = st.text_input("Kode Barang")
        jumlah_stok = st.number_input("Jumlah Stok", min_value=0)
        submit_button_stok = st.form_submit_button(label='Update Stok')

        if submit_button_stok:
            stok.update_stok(kode_barang, jumlah_stok)
            stok.simpan_stok(stok_url)
            st.success("Stok berhasil diperbarui!")

    # Analisa Keuangan dan Stok
    total_nilai_stok, saldo, warning = analisa_keuangan_ke_stok(keuangan, stok)
    st.subheader("Analisa Keuangan dan Stok")
    st.write(f"Total Nilai Stok Barang: {total_nilai_stok}")
    st.write(f"Saldo Keuangan: {saldo}")
    if warning:
        st.warning(warning)
    
    # Visualisasi Keuangan
    visualisasi_keuangan(keuangan)

if __name__ == "__main__":
    app()

