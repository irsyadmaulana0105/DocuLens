# Vibe Coding Guide

Cara bekerja dengan AI coding assistant (Claude Code, Cursor, dll.) agar hasilnya rapi, dapat dipertanggungjawabkan, dan tetap **proyekmu**.

## Prinsip
1. **Dokumen dulu, kode kemudian.** SRS dan schema adalah sumber kebenaran. Ubah dokumen dulu bila kebutuhan berubah.
2. **Satu tugas kecil per sesi.** Contoh baik: "Buat modul OCR dengan interface `OcrEngine` dan implementasi PaddleOCR + test." Contoh buruk: "Bangun backend-nya."
3. **Satu milestone = satu branch.** Merge ke `main` hanya bila DoD tercapai.
4. **Evaluasi dulu, UI belakangan.** Angka baseline lebih berharga daripada tampilan.
5. **Pahami semua kode yang kamu commit.** Di interview, kamu harus bisa menjelaskannya. Minta AI menjelaskan bagian yang belum kamu paham.
6. **Jangan biarkan AI mengubah SRS/schema diam-diam.** Perubahan harus kamu setujui dan dicatat di `docs/decisions.md`.

## Alur Kerja per Tugas
1. Buat branch: `git checkout -b m1-ocr-module`
2. Beri konteks: "Baca `CLAUDE.md`, `docs/SRS.md` bagian FR-21, dan `docs/architecture.md` bagian 3."
3. Minta **rencana** dulu, setujui, baru minta implementasi.
4. Minta **test** bersamaan dengan kode.
5. Jalankan sendiri: lint, test, dan coba manual.
6. Review diff (`git diff`) sebelum commit.
7. Commit kecil dengan pesan jelas, lalu merge saat DoD terpenuhi.

## Template Prompt

**Memulai tugas**
```
Baca CLAUDE.md dan docs/SRS.md (FR-xx). Tugas: <satu hal spesifik>.
Batasan: jangan ubah file di luar <folder>. Sertakan unit test.
Beri rencana langkah singkat dulu, tunggu persetujuan saya sebelum menulis kode.
```

**Debug**
```
Test ini gagal: <paste error>. Jelaskan penyebab sebenarnya dulu,
lalu usulkan perbaikan minimal. Jangan refactor hal lain.
```

**Review**
```
Review diff ini terhadap SRS (FR-xx, NFR-xx). Cari bug, celah keamanan,
dan hal yang melanggar arsitektur. Jangan menulis ulang, cukup daftar temuan.
```

## Konvensi Git
- Branch: `m<nomor>-<deskripsi>` (mis. `m2-upload-endpoint`)
- Commit (Conventional Commits): `feat: add paddleocr engine`, `fix: handle empty ocr result`, `docs: update SRS FR-25`, `test:`, `refactor:`, `chore:`
- Commit sering, kecil, dan satu tujuan.
- Tag rilis di akhir milestone: `git tag v0.1-m1`

## Guardrail Kualitas
- Jangan commit `.env`, dataset besar, atau dokumen asli.
- Selalu jalankan lint + test sebelum commit.
- Jangan terima kode yang menangkap exception lalu diam saja.
- Waspadai AI yang "mengarang" nama library/fungsi; cek dokumentasi resmi.
- Setiap angka di README harus bisa direproduksi dari `eval/`.

## Checklist Sebelum Merge
- [ ] DoD milestone terpenuhi
- [ ] Test lolos, lint bersih
- [ ] Dokumen (SRS/README/decisions) sudah selaras dengan kode
- [ ] Tidak ada secret/data sensitif di diff
- [ ] Kamu bisa menjelaskan setiap bagian kode utama
