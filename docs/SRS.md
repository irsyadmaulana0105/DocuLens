# Software Requirements Specification (SRS)

**Proyek:** DocuLens
**Versi:** 0.1 (draft)
**Status:** Aktif — ubah dokumen ini lebih dulu sebelum mengubah perilaku sistem.

---

## 1. Pendahuluan

### 1.1 Tujuan
Mendefinisikan apa yang harus dilakukan sistem DocuLens, agar pengembangan (termasuk dengan AI coding assistant) tetap terarah dan dapat diuji.

### 1.2 Ruang Lingkup
DocuLens memproses dokumen bisnis (fase MVP: **receipt dan invoice**) menjadi data terstruktur melalui OCR, ekstraksi LLM, validasi, confidence scoring, review manusia, lalu menyediakan pencarian dan tanya jawab (RAG) atas dokumen terverifikasi.

### 1.3 Definisi
| Istilah | Arti |
|---|---|
| OCR | Optical Character Recognition: gambar → teks + posisi |
| Field | Satu atribut hasil ekstraksi (mis. `total`, `invoice_date`) |
| Confidence | Skor 0–1 keyakinan sistem atas sebuah field |
| HITL | Human-in-the-loop: manusia memverifikasi hasil yang ragu |
| RAG | Retrieval-Augmented Generation: jawaban LLM berdasar dokumen yang diambil |
| Auto-approve | Dokumen disetujui otomatis karena semua field melewati threshold |

### 1.4 Prioritas (MoSCoW)
**M** = Must (MVP), **S** = Should, **C** = Could, **W** = Won't (tidak sekarang).

---

## 2. Gambaran Umum

### 2.1 Pengguna
| Peran | Deskripsi | Hak utama |
|---|---|---|
| Admin | Pengelola sistem | Semua fitur, kelola user, lihat dashboard |
| Reviewer | Staf finance/admin | Upload, review, edit, approve, cari |
| Viewer | Pembaca | Cari dan lihat dokumen terverifikasi |

### 2.2 Asumsi & Batasan
- Dokumen berupa PDF atau gambar; satu dokumen = satu invoice/receipt (multi-page boleh, maks. 10 halaman).
- Bahasa utama: Indonesia dan Inggris.
- LLM berjalan lokal lewat Ollama (tanpa biaya API); kecepatan bergantung pada perangkat keras pengembangan.
- Data uji adalah dataset publik + data sintetis. **Tidak ada data pribadi nyata di repo.**
- Dikembangkan solo; deploy target adalah Docker Compose lokal.

---

## 3. Kebutuhan Fungsional

### 3.1 Autentikasi & Otorisasi
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-01 | User dapat login dengan email dan password (password di-hash). | M |
| FR-02 | Sistem menerapkan peran Admin, Reviewer, Viewer pada endpoint dan UI. | M |
| FR-03 | Admin dapat membuat dan menonaktifkan user. | S |

### 3.2 Upload & Manajemen Dokumen
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-10 | User dapat mengunggah PDF/JPG/PNG (maks. 10 MB, maks. 10 halaman). | M |
| FR-11 | Sistem memvalidasi tipe dan ukuran file di sisi server. | M |
| FR-12 | Sistem mendeteksi duplikat lewat hash file dan memberi peringatan. | S |
| FR-13 | Dokumen punya status: `uploaded → processing → needs_review → approved / rejected / failed`. | M |
| FR-14 | User dapat melihat daftar dokumen dengan filter status dan tanggal. | M |

### 3.3 Pipeline Pemrosesan
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-20 | Sistem mengklasifikasi dokumen (`receipt`, `invoice`, `other`). | S |
| FR-21 | Sistem menjalankan OCR dan menyimpan teks, bounding box, dan skor OCR per token/baris. | M |
| FR-22 | Sistem mengekstrak field sesuai [extraction schema](extraction-schema.md) lewat LLM dalam output JSON tervalidasi. | M |
| FR-23 | Sistem menjalankan aturan validasi (mis. jumlah item = total, format tanggal, total > 0). | M |
| FR-24 | Sistem menghitung confidence per field dengan menggabungkan skor OCR, hasil validasi, dan konsistensi ekstraksi. | M |
| FR-25 | Dokumen diarahkan: semua field ≥ threshold dan validasi lulus → `approved` (auto); selain itu → `needs_review`. Threshold dapat dikonfigurasi. | M |
| FR-26 | Pemrosesan berjalan asinkron; kegagalan dicatat dan dapat di-retry. | M |
| FR-27 | Sistem mencatat model, versi prompt, latensi, dan jumlah token per dokumen (serta biaya bila memakai provider berbayar). | S |

### 3.4 Review Manusia (HITL)
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-30 | UI menampilkan gambar dokumen berdampingan dengan field hasil ekstraksi. | M |
| FR-31 | Field berconfidence rendah atau gagal validasi ditandai; klik field menyorot bounding box-nya di dokumen. | M |
| FR-32 | Reviewer dapat mengedit nilai field, lalu approve atau reject dokumen. | M |
| FR-33 | Setiap perubahan (siapa, kapan, nilai lama → baru) tercatat di audit log yang tidak dapat diubah lewat UI. | M |
| FR-34 | Koreksi reviewer disimpan sebagai ground truth tambahan untuk evaluasi. | S |

### 3.5 Pencarian & RAG
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-40 | Hanya dokumen `approved` yang diindeks (chunk + embedding) ke pgvector. | M |
| FR-41 | User dapat mencari dokumen dengan kombinasi kata kunci dan semantik, serta filter (vendor, tanggal, rentang total). | M |
| FR-42 | User dapat bertanya dalam bahasa natural; jawaban menyertakan sitasi ke dokumen dan field/halaman sumber. | M |
| FR-43 | Bila bukti tidak cukup, sistem menjawab bahwa informasi tidak ditemukan (tidak mengarang). | M |
| FR-44 | Reranker untuk meningkatkan kualitas retrieval. | C |

### 3.6 Dashboard & Ekspor
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-50 | Dashboard menampilkan jumlah dokumen per status, persentase auto-approve, rata-rata waktu proses. | S |
| FR-51 | Data terverifikasi dapat diekspor sebagai CSV/JSON. | S |

### 3.7 Evaluasi
| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-60 | Tersedia CLI untuk menjalankan evaluasi OCR, ekstraksi, kalibrasi confidence, dan RAG pada dataset uji. | M |
| FR-61 | Hasil evaluasi disimpan (JSON/CSV) dengan konfigurasi dan versi kode sehingga dapat direproduksi. | M |

---

## 4. Kebutuhan Non-Fungsional

| ID | Kategori | Kebutuhan | Target awal |
|---|---|---|---|
| NFR-01 | Performa | Waktu proses satu receipt 1 halaman | Ukur dan laporkan; target sementara p95 < 60 detik (field MVP) di laptop pengembangan, direvisi setelah baseline M1 |
| NFR-02 | Performa | Respons pencarian | p95 < 2 detik |
| NFR-03 | Keamanan | Password di-hash (bcrypt/argon2), JWT atau session aman, secret hanya di env | Wajib |
| NFR-04 | Keamanan | Validasi file upload (tipe, ukuran), nama file disanitasi, tidak dieksekusi | Wajib |
| NFR-05 | Privasi | Tidak ada data nyata/PII di repo; dokumen upload di luar git | Wajib |
| NFR-06 | Keandalan | Job gagal dapat di-retry tanpa duplikasi hasil (idempotent) | Wajib |
| NFR-07 | Observabilitas | Log terstruktur dengan `document_id` pada setiap tahap pipeline | Wajib |
| NFR-08 | Keterbacaan kode | Linter + formatter (ruff, eslint/prettier) lolos di CI | Wajib |
| NFR-09 | Pengujian | Unit test untuk validasi & confidence; integration test untuk alur upload → extract | Cakupan komponen inti ≥ 70% |
| NFR-10 | Portabilitas | Seluruh sistem berjalan dengan `docker compose up` | Wajib |
| NFR-11 | Biaya & sumber daya | Jumlah token, latensi, dan spesifikasi perangkat keras dicatat dan dilaporkan (biaya bila memakai provider berbayar) | Wajib |
| NFR-12 | Reproduktibilitas | Evaluasi memakai seed tetap dan konfigurasi tercatat | Wajib |

---

## 5. Antarmuka Eksternal

### 5.1 REST API (ringkas)
| Method | Endpoint | Fungsi |
|---|---|---|
| POST | `/auth/login` | Login, mengembalikan token |
| POST | `/documents` | Upload dokumen |
| GET | `/documents` | Daftar dokumen (filter status/tanggal) |
| GET | `/documents/{id}` | Detail dokumen + hasil ekstraksi |
| POST | `/documents/{id}/reprocess` | Jalankan ulang pipeline |
| PATCH | `/documents/{id}/fields/{field}` | Edit nilai field (tercatat di audit log) |
| POST | `/documents/{id}/approve` | Approve |
| POST | `/documents/{id}/reject` | Reject |
| GET | `/documents/{id}/audit` | Audit log dokumen |
| GET | `/search` | Pencarian hibrid |
| POST | `/ask` | Tanya jawab RAG dengan sitasi |
| GET | `/stats` | Data dashboard |
| GET | `/export` | Ekspor CSV/JSON |

Kontrak detail akan di-generate otomatis oleh FastAPI (`/docs`) dan menjadi sumber kebenaran setelah backend ada.

### 5.2 Layanan Eksternal
- Ollama (lokal) untuk ekstraksi, jawaban RAG, dan embedding (`bge-m3`). Provider lain dapat dipasang lewat interface `LLMClient` (lihat [decisions](decisions.md)).

---

## 6. Kebutuhan Data
- Skema database: [data-model.md](data-model.md)
- Kontrak JSON ekstraksi: [extraction-schema.md](extraction-schema.md)
- Retensi: dokumen upload dan hasil ekstraksi disimpan sampai dihapus oleh Admin.

---

## 7. Di Luar Lingkup (Won't, untuk sekarang)
- Multi-tenant / multi-organisasi.
- Integrasi ke sistem ERP/akuntansi.
- Training/fine-tuning model dari nol (boleh eksperimen terbatas di fase lanjut).
- Dukungan tulisan tangan.
- Mobile app.

---

## 8. Kriteria Penerimaan MVP

MVP dianggap selesai bila:
1. Receipt dari dataset uji dapat di-upload dan diproses sampai status akhir tanpa intervensi developer.
2. Field `vendor`, `date`, `total` diekstrak dengan F1 yang tercatat (tanpa target angka tetap; yang wajib adalah angka itu **diukur dan dilaporkan**).
3. Reviewer dapat memperbaiki field dan perubahan muncul di audit log.
4. Pertanyaan pada golden set RAG dijawab dengan sitasi; pertanyaan tanpa bukti ditolak.
5. `docker compose up` menjalankan seluruh sistem dari repo bersih mengikuti README.
6. README memuat tabel hasil eksperimen dan keterbatasan.

## 9. Traceability (diisi bertahap)

| Requirement | Milestone | Test / Evidence |
|---|---|---|
| FR-21, FR-22 | M1 | `eval/` skrip baseline |
| FR-10–FR-14, FR-26 | M2 | integration test upload |
| FR-30–FR-33 | M3 | demo + test audit log |
| FR-40–FR-43 | M4 | golden set RAG |
| FR-60, FR-61 | M5 | `eval/` laporan |
