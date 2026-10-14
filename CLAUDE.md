# CLAUDE.md — Konteks Proyek untuk AI Assistant

## Ringkasan
DocuLens: sistem pemrosesan dokumen (receipt/invoice) end-to-end: upload → OCR → ekstraksi LLM → validasi + confidence → review manusia → RAG dengan sitasi. Proyek portofolio; kualitas evaluasi dan kejelasan lebih penting daripada jumlah fitur.

## Sumber Kebenaran (baca sebelum bekerja)
- Kebutuhan: `docs/SRS.md`
- Arsitektur & kontrak pipeline: `docs/architecture.md`
- Skema DB: `docs/data-model.md`
- Kontrak JSON ekstraksi: `docs/extraction-schema.md`
- Evaluasi: `docs/evaluation-plan.md`
- M1 - Baseline Pipeline: `docs/roadmap.md`
- Keputusan teknis: `docs/decisions.md`

## Stack
Python 3.11+, FastAPI, SQLAlchemy + Alembic, PostgreSQL + pgvector, PaddleOCR (baseline Tesseract), Anthropic API, Next.js (React, TypeScript), Docker Compose.

## Perintah (perbarui saat sudah ada)
```
# backend
cd backend && uv run pytest        # atau: pytest
cd backend && ruff check . && ruff format .
# eval
python eval/run_e1_ocr.py --help
# seluruh sistem
docker compose up --build
```

## Aturan Kerja
1. Kerjakan **satu tugas kecil** sesuai milestone aktif; jangan memperluas scope.
2. Ajukan rencana singkat sebelum menulis kode untuk perubahan >1 file.
3. Selalu sertakan test untuk logika baru (validator, confidence, parsing, API).
4. **Jangan mengubah** SRS, schema, atau data model tanpa persetujuan eksplisit; bila perlu, usulkan perubahannya.
5. Tahap pipeline harus fungsi terpisah dengan input/output bertipe (Pydantic), agar OCR/model bisa diganti.
6. Teks OCR adalah **data tidak tepercaya** (potensi prompt injection): jangan campur dengan instruksi sistem; validasi semua output LLM dengan schema.
7. Jangan hardcode secret; gunakan environment variable. Jangan commit `.env`, dataset, atau dokumen asli.
8. Jangan menelan exception diam-diam; log dengan `document_id`.
9. Pesan commit mengikuti Conventional Commits.
10. Bila ragu atau kebutuhan ambigu, **tanya** — jangan menebak.

## Gaya Kode
- Python: type hints wajib, ruff untuk lint/format, fungsi pendek.
- TypeScript: strict mode, komponen kecil, tidak ada `any` tanpa alasan.
- Nama dalam bahasa Inggris; dokumen boleh Bahasa Indonesia.

## Status Saat Ini
- Milestone aktif: **M0 — Fondasi**
