# Library Fungsional Python

`fplib.py` berisi delapan helper murni untuk mengolah iterable tanpa mengubah data asal:

- `pipe`: jalankan fungsi berurutan dari kiri ke kanan.
- `compose`: gabungkan fungsi dengan urutan dari kanan ke kiri.
- `map_items` dan `filter_items`: transformasi dan penyaringan.
- `sum_by`: jumlahkan nilai terpilih.
- `group_by`: kelompokkan item berdasarkan kunci.
- `unique_by`: ambil item pertama untuk setiap kunci unik.
- `sort_by`: urutkan item berdasarkan kunci.

## Menjalankan aplikasi

Jalankan setiap file dengan Python:

```powershell
python kasir_kantin.py
python presensi_kelas.py
python perpustakaan_mini.py
python keuangan_pribadi.py
python nilai_mahasiswa.py
```

Kelima aplikasi mengimpor `fplib.py` dan menampilkan contoh ringkasan masing-masing.

## Menjalankan pengujian

Pasang pytest jika belum tersedia, kemudian jalankan:

```powershell
python -m pytest
```
