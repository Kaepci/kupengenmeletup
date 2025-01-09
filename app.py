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
        pemasukan, pengeluaran, saldo_akhir = self.laporan_keuangan()
        return pemasukan, pengeluaran, saldo_akhir

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
    
    st.pyplot(fig)

# Streamlit UI
def app():
    st.title('Manajemen Keuangan dan Stok')

    # Upload file CSV
    keuangan_file = st.file_uploader("Upload File Keuangan (CSV)", type=["csv"])
    stok_file = st.file_uploader("Upload File Stok (CSV)", type=["csv"])

    if keuangan_file and stok_file:
        # Load data dari file CSV
        keuangan = Keuangan(keuangan_file)
        stok = Stok(stok_file)

        # Menampilkan laporan keuangan
        pemasukan, pengeluaran, saldo_akhir = keuangan.tampilkan_laporan()
        st.subheader("Laporan Keuangan")
        st.write(f"Pemasukan: {pemasukan}")
        st.write(f"Pengeluaran: {pengeluaran}")
        st.write(f"Saldo Akhir: {saldo_akhir}")

        # Menampilkan laporan stok
        st.subheader("Laporan Stok Barang")
        st.write(stok.tampilkan_laporan())

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
