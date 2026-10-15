# Data

Folder ini **tidak** menyimpan dataset besar di git (lihat `.gitignore`).

## Dataset publik
| Dataset | Dipakai untuk | Catatan |
|---|---|---|
| SROIE | Receipt: OCR + key info extraction | Mulai dari sini (MVP) |
| CORD | Receipt: struktur item & total | Dataset pembanding |
| FUNSD | Form understanding | Opsional (fase lanjut) |
| DocVQA | Document QA | Opsional (fase lanjut) |

## Data lokal (sintetis)
Dokumen invoice/struk berbahasa Indonesia dibuat sintetis dan disimpan di `data/samples/`
beserta ground truth JSON-nya. **Jangan pernah commit dokumen asli yang mengandung data pribadi/perusahaan.**

## Struktur yang disarankan
```
data/
  raw/          # hasil download dataset (gitignored)
  processed/    # hasil konversi ke format internal (gitignored)
  samples/      # beberapa contoh kecil + ground truth (boleh di-commit)
```

## SROIE (yang dipakai saat ini)

| Item | Keterangan |
|---|---|
| Sumber asli | ICDAR 2019 Robust Reading Challenge on Scanned Receipts OCR and Information Extraction (https://rrc.cvc.uab.es/?ch=13&com=downloads) |
| Mirror yang diunduh | Hugging Face `jsdnrs/ICDAR2019-SROIE` (format parquet) |
| Lisensi (menurut mirror) | CC-BY-4.0; NOTICE mirror menyatakan data telah diadaptasi/dimodifikasi oleh maintainer mirror |
| Ukuran split | train: 626 receipt, test: 361 receipt |
| Kolom | `image`, `key`, `image_size`, `entities` (`company`, `date`, `address`, `total`), `words`, `bboxes` |
| Sitasi | Huang et al., "ICDAR2019 Competition on Scanned Receipt OCR and Information Extraction", ICDAR 2019 |

Mirror bukan sumber resmi: cek ulang ketentuan lisensi di situs ICDAR RRC sebelum mempublikasikan hasil, dan cantumkan atribusi di README utama.

### Perintah
```
python scripts/download_sroie.py                      # unduh ke data/raw/sroie (gitignored)
python scripts/prepare_sroie.py --split train --n 50 --seed 42 --out data/processed/sroie_dev
```

Aturan pemakaian split:
- **train** → sumber subset **dev** (menyetel prompt, aturan validasi, threshold).
- **test** → disentuh hanya untuk evaluasi akhir.

Pemetaan label SROIE ke schema internal: `company` → `vendor_name`, `date` → `document_date`, `total` → `total`. Field `address` belum masuk MVP. Format tanggal dan jumlah di SROIE bervariasi, jadi dinormalisasi lebih dulu sebelum dibandingkan (lihat `docs/extraction-schema.md`).
