Nama    : Regina Dibrya Kerinne Purba
NPM     : 2506657296
Kelas   : PBP E

### Tugas 1

1. Saya menggunakan elemen semantik HTMLS5 yaitu <section> ditugas saya. Elemen ini saya gunakan untuk membuat bagian bagian berbeda yang tersedia di navigation bar saya, antara lain Profile, Experience, dan Skills. Elemen ini membantu saya untuk membagi konten halaman menjadi bagian - bagian yang berbeda sehingga lebih rapi, bersih, dan memberikan aksebilitas bagi pengguna. selain itu, section ini juga memberikan heading yang jelas sehingga memudahkan saya untuk mengetahui bahwa konten di dalamnya masih satu topik yang sama.

2. Tantangan utama dalam mengatur CSS agar tetap responsif adalah untuk menyamakan tampilan di web dan di mobile karena adanya perbedaan ukuran device (penyempitan). Menjaga jarak ukuran tulisan dan bentuk list experience yang saya buat cenderung berubah saat diakses lewat mobile. Sebenarnya saya sangat mengupayakan untuk menyamakan persis tampian web dan mobile. Namun, perbedaan ukuran device tetap membuat saya memprioritaskan informasi tentang diri saya lebih penting. Saya juga memprioritaskan kemudahan dalam membaca setiap tulisan yang ada pada text-text dibandingkan memaksakan nilai estetika. Saya membiarkan list experience saya menjadi satu susunan kebawah karena bagi saya yang terpenting hal tersebut masih mudah untuk dibaca

3. Bagi saya yang baru belajar sesungguhnya website static ini sudah memumpuni untuk memenuhi kebutuhan portofolio saya. Apalagi sebenarnya portofolio tidak begitu membutuhkan interaksi pengguna yang begitu kompleks. Namun, saya merasa apabila web portofolio saya dapat dikembangkan menjadi website dinamis yang dapat secara gampang untuk mengupdate pengalaman - pengalaman saya mungkin akan sangat membantu saya dari pada harus menambahkan list list baru di html secara langsung. Penggunaan Django Admin merupakan hal yang paling ingin saya persiapkan untuk ditambahkan pada iterasi proyek saya kedepannya.

Dokumentasi & AI Disclosure:
Chat dengan AI : https://chatgpt.com/share/6a9ed183-1acc-83ec-861e-6582e717d8f9
AI yang saya gunakan dalam pengerjaan Tugas 1 adalah ChatGpt. Adapun penggunaan saya adalah untuk :
- Membantu saya dalam memahami template yang sudah diberikan pada tutorial
- Membantu saya dalam peletakan branch agar sesuai
- Membantu saya mengingat proses add, commit, dan push ke git
- Membantu saya mengetahui cara melakukan hard refresh
- Membantu saya dalam merapikan logo yang saya masukkan sehingga alignnya center
Strategi yang saya gunakan dalam promting adalah membuat sebisa daya + bantuan youtube kemudian jika belum sesuai saya bertanya pada AI. Selain itu saya juga  bertanya apabila saya meragukan permahaman saya akan perintah di website pbp

### Tugas 2

1. Saat localhost:8000/skill/ dijalankan untuk melihat halaman skill pada portofolio saya yang baru saja diupdate, alur yang terjadi adalah browser mengirimkan request ke proyek Django. Django akan mengecek portofolio/urls.py sebagai URL konfigurasi proyek untuk menentukan aplikasi yang menangani URL tersebut dan melemparnya ke main/urls.py(urls.py aplikasi). Kemudian akan ditunjuk view function tertentu yang pada kasus ini adalah show_skill. View bertugas untuk menjalankan logic seperti mengambil data lewat model Skill yang menjadi representasi dari skill database. Setelah data skill diperoleh, view mengirimkannya sebagai context ke template skill.html. Kemudian, template akan menggunakan data skill untuk memproses HTML secara dinamis. HTML hasil rendering selanjutnya dikirim kembali ke browser yang akan menampilkan halaman Skill.

2. - Dengan adanya penggunaan model setiap kali developer ingin untuk mengupdate/ mengubah database tidak perlu untuk mengotak atik kode HTML secara manual (cukup mengubah bagian pada database yang ingin diupdate, dan akan terintegrasi secara otomatis)
- Dengan model data dapat ditambah/dihapus/diedit melalui database atau Django Admin tanpa mengubah kode template. Sedangkan jika langsung ditemplate setiap ingin melakukan perubahan pada data akan membutuhkan developer untuk mengubah kode template
- Dengan penggunaan model maka seperation of concerns akan tercapai dimana template berfokus pada tampilan, model berfokus pada pengelolaan data, dan view menjadi penghubungnya
- Dengan adanya model, setiap tipe data yang digunakan oleh tiap field akan selalu konsisten dengan format yang sesuai (berdasarkan ketentuan)

3. makemigration => digunakan untuk membaca perubahan yang dibuat di models.py dan membuat file migrasi (terdapat di folder migrations) yang berisi instruksi perubahan dari struktur database yang akan diterapkan(belum diaplikasikan ke database).  
migrate => digunakan untuk mengaplikasikan file-file migirasi tersebut kedatabase sesuai instruksi di file migrasi.
contoh pada pekerjaan saya, pembuatan field "category" yang menjadi penanda apakah skill tersebut hardskill atau soft skill. python manage.py makemigrations => memicu Django mendeteksi adanya field category di model skill, yang kemudian akan membuat file migrasi baru. Saat saya menjalankan command python manage.py migrate => Django membaca file migrasi tersebut dan mengupdate database. 
Jika hanya melakukan makemigration tanpa migrate. instruksi perubahan memang ada namun tidak menyebabkan perubahan pada database.

Dokumentasi & AI Disclosure:
Chat dengan AI : https://chatgpt.com/share/6aa813f6-2be4-83ec-8df9-3fd26bd97a12
AI yang saya gunakan dalam pengerjaan Tugas 1 adalah ChatGpt. Adapun penggunaan saya adalah untuk :
- Mengetahui perbedaan dari CharField dan TextField pada models
- Membantu saya dalam mengupdate data yang sebelumnya sudah saya masukkan kedalam shell
- Membantu debugging error yang terjadi akibat perbedaan branch master dan main saya
Strategi yang saya gunakan dalam promting adalah mengusahakan hal-hal yang masih saya pahami dengna panduan dan menonton tutorial youtube. Namun jika terdapat ketidakpahaman yang saya tidak temukan jawabannya tanpa AI, saya akan menggunakan AI untuk membantu saya

Yang saya lakukan pada tugas 2 : 
- Pengimplementasian MVT untuk section skill portofolio saya