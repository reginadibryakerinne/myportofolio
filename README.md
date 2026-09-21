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

### Tugas 3

1. Penggunaan ModelForm kita gunakan pada tugas ini untuk membuat form berdasarkan model Django secara otomatis. Selain itu dengan penggunaan ModelForm akan dilakukan proses validasi tipe data antara field dengan input user beserta constraintnya. Hal ini akan membuat kode lebih sederhana, tidak redundant, dan memastikan form tetap sesuai dengan struktur model. Berbeda dengan HTML yang tidak punya proses validasi otomatis dan proses input data pun harus dilakukan secara manual tiap kali menambah/mengubah field di model. Sehingga hanya mengandalkan penggunaan HTML akan sangat memungkinkan terjadinya human error.

Menambahkan {% csrf_token %} diwajibkan oleh Django untuk semua form dengan method POST/PUT/DELETE secara default (via CsrfViewMiddleware) dengan tujuan menyisipkan token unik dan acak ke dalam form dimana Django akan menyimpan token ini di session dan melakukan validasi apakah token yang dikirim balik saat submit cocok dengan yang ada di session. Dengan regulasi tersebut, situs penyerah tidak bisa mengambil token, sehingga request palsu akan ditolak dengan error 403 Forbiddden

2. - Lebih Ringkas dibanding XML 
XML => tiap elemen butuh opening dan closing tag, menyebabkan struktur lebih verbose
JSON => cukup direpresentasikan sebagai pasangan key-value tanpa tag pembungkus berulang, sehingga size-nya lebih kecil

- Integrasi yang sangat natural dengan JavaScript di sisi frontend
Struktunya yang persis sama dengan object literal di JavaScript membuat  browser bisa langsung menggunakan JSON.parse() respons API jadi object JS tanpa parsing tambahan yang berat. Selain itu, karena frontend modern didominasi JavaScript, kecocokan native ini menjadi alasan praktis terbesar mengapa REST API modern hampir selalu memakai JSON.

- Parser lebih cepat 
JSON => struktur data yang lebih sederhana (cuma object, array, string, number, boolean, null)
XML => namespace, atribut vs elemen, DTD, atau schema validation kompleks
fitur-fitur pada XML tersebut menyebabkan bertambahnya kompleksitas proses parsing   

3. Request dari client diarahkan ke view. Di dalam view itu sendiri, terjadi dua langkah berurutan: pertama, view mengambil data dari database lewat model Django (menghasilkan QuerySet berupa objek Python), lalu langkah kedua, data itu di-serialize (proses mengubah object atau data Django menjadi struktur data yang dapat direpresentasikan dalam format JSON) sebelum dibungkus sebagai HttpResponse dan dikirim balik ke client. Kemudian client menerima response dalam bentuk JSON.

Serialization diperlukan karena object atau model Django tidak secara langsung menggunakan format JSON. JSON hanya dapat merepresentasikan tipe data tertentu seperti object, array, string, number, boolean, dan null. Oleh karena itu, data dari model perlu diubah terlebih dahulu menjadi representasi data yang sesuai dengan JSON sebelum dikirim melalui HTTPResponse.

Dokumentasi & AI Disclosure:

001 / 3 - Commit message yang tepat untuk tugas 3:  https://chatgpt.com/s/t_6ab0d899e8a4819190eda2ffe90e327d

membantu menentukan commit message yang sesuai dengan pereubahan yang saya buat dalam tugas

002 / 3 - Memvalidasi jawaban pertanyaan refleksi: https://chatgpt.com/s/t_6ab0da6fca40819198a3d50eba78ca37

membantu saya untuk memperbaiki alur penulisan jawaban pertanyaan refleksi

003 / 3 - Pemahaman serta solusi dari error: https://chatgpt.com/s/t_6ab0e187e11481919a0e9b178f0a9dc7

membantu saya untuk solving masalah error akibat main GitHub punya commit yang belum ada di lokal branch master saya