# Decision Log (ADR ringan)

Catat setiap keputusan teknis penting di sini. Format: **Konteks → Keputusan → Konsekuensi**. Jangan hapus keputusan lama; beri status `Superseded` bila diganti.

---

## ADR-001 — pgvector alih-alih database vektor terpisah
- **Status:** Accepted
- **Konteks:** Skala data portofolio kecil; ingin infrastruktur minimal dan filter metadata (vendor, tanggal) bersamaan dengan pencarian vektor.
- **Keputusan:** Pakai PostgreSQL + pgvector. Qdrant ditunda.
- **Konsekuensi:** Satu database untuk semuanya, lebih mudah di-deploy. Bila skala/fitur butuh, migrasi ke Qdrant dapat dilakukan lewat lapisan `rag/retrieval`.

## ADR-002 — Mulai tanpa Redis
- **Status:** Accepted
- **Konteks:** Pemrosesan asinkron dibutuhkan, tetapi beban rendah.
- **Keputusan:** Worker membaca tabel `jobs` di PostgreSQL (atau `BackgroundTasks` di awal).
- **Konsekuensi:** Lebih sedikit komponen. Redis/RQ ditambah bila perlu retry dan antrean lanjutan.

## ADR-003 — Fokus satu jenis dokumen di MVP
- **Status:** Accepted
- **Konteks:** Scope terlalu lebar menghambat penyelesaian.
- **Keputusan:** MVP hanya receipt/invoice; PO dan lainnya masuk backlog.
- **Konsekuensi:** Evaluasi lebih bersih dan proyek lebih mungkin selesai.

## ADR-004 — OCR + LLM sebagai baseline, model lain sebagai pembanding
- **Status:** Accepted (pembanding diubah oleh ADR-007)
- **Konteks:** OCR+LLM tercepat dibangun; model layout-aware memberi bahan perbandingan riset.
- **Keputusan:** Bangun OCR+LLM dulu, bandingkan metode lain di M5 bila waktu cukup. (Pembanding aktual: VLM lokal, lihat ADR-007.)
- **Konsekuensi:** Angka baseline cepat tersedia.

## ADR-005 — Ollama sebagai LLM utama lewat interface `LLMClient`
- **Status:** Accepted
- **Konteks:** Tidak ada akses ke API berbayar; data dokumen sebaiknya tetap lokal.
- **Keputusan:** Pakai Ollama (`hermes3:latest` untuk ekstraksi dan RAG, `bge-m3` untuk embedding). Semua panggilan lewat interface `LLMClient` agar provider dapat diganti.
- **Konsekuensi:** Gratis dan privat; kualitas JSON model kecil kurang konsisten, sehingga wajib memakai structured output, validasi Pydantic, dan retry. Nama model persis dicantumkan di README untuk reproduktibilitas.

## ADR-006 — Target latensi disesuaikan dengan pengukuran lokal
- **Status:** Accepted
- **Konteks:** Pengukuran `hermes3:latest` di laptop pengembangan: saat hangat prompt eval ±221 tok/s, generate ±12,7 tok/s, load ±5 detik; cold start pertama jauh lebih lambat (load ±34 detik, prompt eval ±6 tok/s).
- **Keputusan:** NFR-01 menjadi "ukur dan laporkan"; target sementara p95 < 60 detik per receipt (field MVP).
- **Konsekuensi:** Output dijaga ringkas (tahap generate adalah bottleneck), hasil LLM di-cache per (dokumen, model, versi prompt), `OLLAMA_KEEP_ALIVE` diaktifkan, pemrosesan tetap asinkron, evaluasi awal memakai subset dev.

## ADR-007 — VLM lokal sebagai pembanding E2, bukan jalur utama
- **Status:** Accepted
- **Konteks:** Melatih LayoutLMv3/Donut kurang realistis di laptop; `qwen2.5vl:7b` sudah tersedia. UI review membutuhkan bounding box dan skor OCR, yang tidak diberikan VLM secara andal.
- **Keputusan:** Pipeline utama tetap OCR + LLM. `qwen2.5vl:7b` (gambar → JSON langsung) dipakai sebagai pembanding di E2. LayoutLMv3/Donut pindah ke backlog.
- **Konsekuensi:** Perbandingan metode tetap ada tanpa mengorbankan fitur review dan confidence.

## Template

```
## ADR-XXX — Judul
- Status: Proposed | Accepted | Superseded by ADR-YYY
- Konteks:
- Keputusan:
- Konsekuensi:
```
