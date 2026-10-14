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
