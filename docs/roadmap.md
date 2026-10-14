# Roadmap

Setiap milestone = satu branch + satu PR/merge ke `main`. Tidak lanjut ke milestone berikut sebelum **Definition of Done** terpenuhi.

## M0 — Fondasi (±3 hari)
- [ ] Repo, struktur folder, `.gitignore`, `.env.example`
- [ ] SRS, arsitektur, schema ekstraksi ditinjau ulang
- [ ] Setup lint/format, pre-commit, CI dasar (opsional)
- **DoD:** repo bersih, dokumen disetujui, `CLAUDE.md` terisi

## M1 — Baseline Pipeline tanpa UI (minggu 1–2)
- [ ] Loader SROIE dan konversi ke format internal
- [ ] Modul OCR (PaddleOCR) dengan interface yang dapat diganti
- [ ] Extractor LLM → JSON tervalidasi Pydantic
- [ ] Validator + confidence awal
- [ ] Skrip evaluasi: CER/WER dan field F1
- **DoD:** satu perintah menghasilkan angka CER/WER dan F1 pada dev set; angka dicatat di `eval/reports/`

## M2 — Backend (minggu 3)
- [ ] FastAPI + PostgreSQL + Alembic migrasi
- [ ] Endpoint upload/list/detail, tabel `jobs`, worker
- [ ] Auth dasar + peran
- [ ] Integration test upload → extracted
- **DoD:** upload lewat Swagger menghasilkan dokumen berstatus `needs_review`/`approved`

## M3 — UI Review (minggu 4–5)
- [ ] Halaman login, daftar dokumen, upload
- [ ] Viewer dokumen + panel field + highlight bbox
- [ ] Edit, approve, reject + audit log
- **DoD:** alur penuh upload → review → approve dapat didemokan di browser

## M4 — RAG (minggu 6)
- [ ] Chunking + embedding + pgvector
- [ ] Pencarian hibrid + filter
- [ ] Endpoint `/ask` dengan sitasi dan penolakan bila tak ada bukti
- [ ] Golden set RAG
- **DoD:** golden set berjalan, hasil tercatat

## M5 — Eksperimen & Evaluasi (minggu 7)
- [ ] E1–E5 dijalankan, laporan di `eval/reports/`
- [ ] Tabel hasil dimasukkan ke README
- **DoD:** README berisi angka asli + analisis error

## M6 — Polish (minggu 8)
- [ ] Docker Compose penuh, README lengkap (Quick Start teruji dari repo bersih)
- [ ] Dashboard sederhana + ekspor
- [ ] Video demo / GIF, screenshot
- [ ] Bagian Keterbatasan & Future Work
- **DoD:** orang lain bisa menjalankan proyek hanya dengan membaca README

## Backlog (setelah MVP)
- PO dan tipe dokumen lain · LayoutLMv3/Donut · reranker · Redis queue · RBAC lanjutan · deploy cloud
