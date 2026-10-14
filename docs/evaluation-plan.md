# Evaluation Plan

Bagian ini yang membedakan proyek ini dari "demo upload PDF". Semua klaim di README harus berasal dari sini.

## 1. Prinsip
- Pisahkan data: **dev** (untuk menyetel prompt/threshold) dan **test** (hanya dipakai untuk angka akhir).
- Seed tetap, konfigurasi dan git commit dicatat di setiap run (`eval_runs`).
- Laporkan juga **kegagalan**: contoh error dan kategorinya.

## 2. Dataset
| Dataset | Tugas | Peran |
|---|---|---|
| SROIE | OCR + key info extraction receipt | Utama (MVP) |
| CORD | Struktur receipt (item, total) | Pembanding |
| FUNSD / DocVQA | Layout / QA | Fase lanjut |
| Sintetis Indonesia | Invoice/struk Bahasa Indonesia + ground truth | Uji generalisasi |
| Golden set RAG | 30–50 pasangan pertanyaan–jawaban–dokumen sumber | Evaluasi RAG |

## 3. Metrik
| Area | Metrik |
|---|---|
| OCR | CER, WER |
| Ekstraksi | Field-level precision/recall/F1, exact match per field, normalisasi (tanggal, angka) sebelum dibandingkan |
| Confidence | Expected Calibration Error (ECE), reliability diagram, AUROC "benar vs salah" |
| HITL | % auto-approve, akurasi auto-approve, % field dikoreksi manusia |
| RAG | Retrieval hit@k / MRR, faithfulness (jawaban didukung konteks), citation precision, tingkat penolakan benar saat tak ada bukti |
| Sistem | Latensi p50/p95, biaya per dokumen |

## 4. Eksperimen

| ID | Pertanyaan | Perbandingan | Output |
|---|---|---|---|
| E1 | OCR mana yang lebih baik? | Tesseract vs PaddleOCR | Tabel CER/WER |
| E2 | Seberapa baik OCR + LLM mengekstrak field? | OCR+LLM (baseline); lalu LayoutLMv3 / Donut bila waktu cukup | Tabel F1 per field |
| E3 | Apakah confidence dapat dipercaya? | Sinyal tunggal vs gabungan (OCR + validasi + konsistensi) | ECE + reliability diagram |
| E4 | Berapa kerja manual yang bisa dihemat? | Sapuan threshold 0.5 → 0.99 | Kurva: % auto-approve vs akurasi |
| E5 | Apakah RAG jujur dan akurat? | Dengan vs tanpa reranker; dengan vs tanpa aturan "tolak bila tak ada bukti" | Tabel faithfulness & citation precision |
| E6 (opsional) | Generalisasi ke dokumen Indonesia | SROIE-tuned prompt vs sintetis lokal | Tabel F1 |

## 5. Struktur Folder `eval/`

```
eval/
  README.md            # cara menjalankan
  datasets/            # loader per dataset
  metrics/             # cer_wer.py, field_f1.py, calibration.py, rag.py
  run_e1_ocr.py
  run_e2_extraction.py
  run_e3_calibration.py
  run_e4_autoapprove.py
  run_e5_rag.py
  outputs/             # (gitignored) hasil mentah
  reports/             # ringkasan .md yang di-commit
```

## 6. Format Laporan Tiap Eksperimen
1. Tujuan dan hipotesis
2. Setup (model, versi prompt, data, seed)
3. Hasil (tabel/grafik)
4. Analisis error (minimal 5 contoh kegagalan)
5. Kesimpulan dan keterbatasan
