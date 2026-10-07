--Melihat Semua data
SELECT *
FROM produksi

--Menampilkan hasil total penjualan & harga satuan dengan mengelompokkan data sesuai dengan ID_Transaksi
SELECT 
	"ID_Transaksi",
	SUM("Total_Penjualan") AS Hasil_total_penjualan,
	SUM("Harga_Satuan") AS Hasil_total_harga_satuan

FROM produksi
GROUP BY "ID_Transaksi";

--Melihat omzet totl bulanan & omzet rata-rata bulanan
SELECT "Bulan",
	SUM("Total_Penjualan") AS total_omzet_bulanan,
	ROUND(AVG("Total_Penjualan")) AS rata_rata_omzet_perbulan
FROM produksi 
GROUP BY "Bulan", "Nomor_Bulan"
ORDER BY "Nomor_Bulan" ASC;

--Melihat performa bisnis dari setiap kota
SELECT 
	"Kota_Toko",
	COUNT(DISTINCT"ID_Transaksi") AS total_transaksi,
	SUM("Jumlah") AS total_produk_terjual,
	SUM("Total_Penjualan") AS total_pendapatan

FROM produksi
GROUP BY "Kota_Toko"
ORDER BY total_pendapatan DESC;

--Melihat jumlah barang pada setiap produk
SELECT 
	"Produk",
	SUM("Jumlah") AS per_produk

FROM produksi
GROUP BY "Produk"

--Untuk melihat data anomaly pada setiap kolom
SELECT *
FROM produksi
WHERE "Jumlah" <=0 OR "Harga_Satuan" <=0 OR "Total_Penjualan" IS NULL
ORDER BY "ID_Transaksi";

--Melihat 5 teratas produk yang terjual dengan mengurutkan dari yang paling banyak total barang yang terjual 
SELECT 
	"Produk",
	COUNT("ID_Transaksi") AS frekuensi_pembelian,
	SUM("Jumlah") AS total_barang_terjual,
	SUM("Total_Penjualan") AS total_pendapatan
FROM produksi
GROUP BY "Produk"
ORDER BY total_barang_terjual DESC
LIMIT 5;