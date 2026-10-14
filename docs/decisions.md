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

## ADR-004 — OCR + LLM sebagai baseline, LayoutLMv3/Donut sebagai pembanding
- **Status:** Accepted
- **Konteks:** OCR+LLM tercepat dibangun; model layout-aware memberi bahan perbandingan riset.
- **Keputusan:** Bangun OCR+LLM dulu, bandingkan metode lain di M5 bila waktu cukup.
- **Konsekuensi:** Angka baseline cepat tersedia.

## Template

```
## ADR-XXX — Judul
- Status: Proposed | Accepted | Superseded by ADR-YYY
- Konteks:
- Keputusan:
- Konsekuensi:
```
