import pandas as penjualan
from sqlalchemy import create_engine

df = penjualan.read_csv(r"D:\Latihan Data Engineer\Data Set\dataset_kotor_500_baris.csv", na_values=["Nan","nan"," "])

#Ubah SEMUA teks '[null]' atau 'null' di SEMUA kolom menjadi nilai kosong asli Python (None)
df = df.replace(["[null]", "null"], None)

print("SELURUH DATA")
df.info()

print("\n 10 baris pertama")
print (df.head(10))

print("\n ringkasan statistik")
print(df.describe())

print("\n jumlah baris dan kolom")
print(df.shape)

# Menghapus nilai kosong/NaN data, tabel yang dipilih
df.dropna(subset=['Harga_Satuan', "ID_Transaksi"], inplace=True)

#1 mengubah kolom menjadi tipe stringer agar fungsi .str bisa berjalan
df["Harga_Satuan"] = df["Harga_Satuan"].astype(str)
#2 mengapus teks "Rp"/berbagai simbol (bila ada)
df["Harga_Satuan"] = df["Harga_Satuan"].str.replace('Rp', '' , case=False)
#3 Hapus tanda "titik" yang memisahkan angka ribuan
df["Harga_Satuan"] = df["Harga_Satuan"].str.replace('.', '' )
#4 Hapus jika ada spasi liar didepan ataupun belakang
df["Harga_Satuan"] = df["Harga_Satuan"].str.strip()
#5 uabh tipe nya menjadi integer (angka bulat) agar dapat diolah
df["Harga_Satuan"] = df["Harga_Satuan"].astype(int)

#6 mengubah format waktu biar selaras
df["Tanggal"] = penjualan.to_datetime(df["Tanggal"], errors='coerce', format='mixed')

#Membuat kolom 'Nomor_Bulan' (mengambil angka 1 - 12)
df["Nomor_Bulan"] = df["Tanggal"].dt.month

#Buat kolom 'Bulan'
nama_bulan_id = {
    1: "Januari", 2: "Ferbruari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7:"Juli", 8: "Agustus", 9: "September",
    10: "Oktober", 11: "November", 12: "Desember"
}

#Menerapkan pemetaan angka bulan ke bahasa indonesia
df["Bulan"] = df["Nomor_Bulan"].map(nama_bulan_id)

#Verifikasi hasil
print(df[["Tanggal","Bulan","Nomor_Bulan"]].head())

# 7 Bersihkan Kolom Produk
# Menghapus spasi liar dan mengubah format menjadi UPPERCASE (Huruf kapital semua)
# Rekomendasi: Gunakan UPPERCASE untuk produk agar spesifikasi teks seperti 'INCH', 'HDMI' terlihat tegas.
df['Produk'] = df['Produk'].str.strip().str.upper()

#8 Bersihkan kolom Kota_Toko
# Menghapus spasi liar di awal/akhir dan mengubah format menjadi Title Case (Huruf besar di awal kata)
df['Kota_Toko'] = df['Kota_Toko'].str.strip().str.title()

#MENYARING BARIS YANG MEMILIKI JUMLAH < 0 ATAU Harga_Satuan < 0
df_aneh = df[(df["Jumlah"] < 0) | (df["Harga_Satuan"] < 0)]

#PROSES CLEANING: MEMPERTAHANKAN DATA YANG NILAINYA DIAATAS 0 PADA KOLOM JUMLAH
df = df[df['Jumlah'] > 0]

#MENGHITUNG TOTAL DUPLIKAT DALAM SELURUH KOLOM
total_duplikat = df.duplicated().sum()
print(f"Jumlah baris duplikat: {total_duplikat}")

#mengitung jumlah rows sebelum dilakukan cleaning duplikat
rows_sebelum = len(df)

#menyisakan 1 data asli 
df_cleaned = df.drop_duplicates(keep='first')

#menghitung jumlah rows sesudah cleaning duplikat
rows_sesudah = len(df_cleaned)

#menghitung berapa banyak data yang dibuang
data_dibuang = rows_sebelum - rows_sesudah


print(f"Rows sebelum cleaning = {rows_sebelum}")
print(f"Rows sesudah cleaning = {rows_sesudah}")
print(f" Total duplikat yang dibuang = {data_dibuang}")

#menyimpan kembali ke variabel df utama 
df = df_cleaned


print("Data aneh ditemukan:")
print(df_aneh)

#MENGHITUNG BERAPA BANYAK DATA ANEHNYA
print(f"Total baris data aneh: {len(df_aneh)}")

#BUAT KOLOM BARU BERNAMA Total_Penjualan dengan mengalikan kolom Jumlah dan Harga_Satuan
df["Total_Penjualan"] = df["Jumlah"] * df["Harga_Satuan"]

print("Data setelah ditambahkan kolom Total-Penjualan")
print(df[["Jumlah","Harga_Satuan","Total_Penjualan"]])



# Atur nilai default yang sesuai dengan karakteristik masing-masing kolom
# Agar kolom teks terisi rapi dan kolom angka tidak berubah jadi teks rusak
nilai_default = {
    "ID_Transaksi" : "TRX-UNKNOWN",
    "Tanggal" : "TANGGAL-UNKNOWN",
    "Produk" : "PRODUK-UNKNOWN",
    "Jumlah" : 0,
}
#Isi semua nilai kosong tersebut berdasarkan aturan di atas
df = df.fillna(value=nilai_default)

# Mengisi NILAI KOSONG di SEMUA KOLOM dengan teks 'Tanpa Data'
df = df.fillna("Tanpa Data")


print("data yang sudah dibersihkan")
print(df.head(10))

engine = create_engine(
    "postgresql://postgres:Rizki17%40@localhost:5432/produksi_db"
)

df.to_sql(
    "produksi",
    engine,
    if_exists="replace",
    index=False
)

print("berhasil dikirim ke warehouse")
