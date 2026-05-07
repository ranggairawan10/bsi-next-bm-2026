# BSI Next BM School 2026 · Scoring System v2

Sistem penilaian real-time untuk Branch Banking Simulation (Next BM School), competitive tender PT Bank Syariah Indonesia × HCR.ID.

## Arsitektur CPI Opsi A (LOCKED)

```
CPI = (Indeks_POST × 2 + Indeks_SIM × 16) / 18
```

| Komponen | Bobot | Sumber | Mekanisme |
|----------|-------|--------|-----------|
| L2 POST  | 2 jam  | Excel BSI Bank Soal Post-Test | Upload via report.html |
| L3 SIM   | 16 jam | Firebase real-time | BPM_combined × 30% + Behavior 6D × 70% |
| Pre-Test | informatif | Excel BSI Pre-Test (opsional) | Untuk Learning Gain saja, tidak masuk CPI |

| Predikat | Rentang | Indeks |
|----------|---------|--------|
| A · Sangat Kompeten | 90-100 | 4 |
| B · Kompeten | 80-89 | 3 |
| C · Cukup Kompeten | 70-79 | 2 |
| D · Belum Kompeten | <70 | 1 |

Target kelulusan: **CPI ≥ 3.00** = LULUS · CPI < 3.00 = BELUM LULUS

## Struktur File (8 HTML Monolitik)

| File | Akses | Peran |
|------|-------|-------|
| index.html | semua | Login router · 15 kode akses |
| admin.html | BSI2026ADMIN | Master Admin · session control · member editor · override · export |
| gamemaster.html | BSI2026GM | Game Master · BPM scoring -10 to +10 · timer · Amanah |
| board.html | BSI2026BOARD | Visual Board · ranking real-time |
| projector.html | BSI2026LAYAR | Layar fullscreen untuk peserta |
| coach.html | COACH2026G1-G5 | Branch Coach · 6D behavior scoring |
| leader.html | LEADER2026G1-G5 | Group Leader · peer BPM scoring |
| report.html | BSI2026REPORT | Report Generator · CPI calculation · Print/PDF |

## 15 Kode Akses

```
Sistem (5):
  BSI2026ADMIN   → admin.html
  BSI2026GM      → gamemaster.html
  BSI2026LAYAR   → projector.html
  BSI2026BOARD   → board.html
  BSI2026REPORT  → report.html

Branch Coach per Kelompok (5):
  COACH2026G1    → Cabang Borobudur
  COACH2026G2    → Cabang Prambanan
  COACH2026G3    → Cabang Diponegoro
  COACH2026G4    → Cabang Gajah Mada
  COACH2026G5    → Cabang Majapahit

Group Leader per Kelompok (5):
  LEADER2026G1   → Cabang Borobudur
  LEADER2026G2   → Cabang Prambanan
  LEADER2026G3   → Cabang Diponegoro
  LEADER2026G4   → Cabang Gajah Mada
  LEADER2026G5   → Cabang Majapahit
```

## Arsitektur Firebase

Project: `bsi-next-bm-2026` · Region: `asia-southeast1` (Singapore)

Path utama:
```
bpm_gm/r{R}/g{G}                         → skor GM per ronde per kelompok (-10..+10)
bpm_leader/r{R}/from_g{X}/to_g{Y}        → { score, note } peer scoring antar kelompok
coach_data/g{G}/r{R}/m{M}                → { qoa, al, sa, rc, ej, pi, token, narrative }
amanah_coins/r{R}/g{G}                   → distribusi koin per ronde
session/currentRound, session/locked     → state sesi global
groups/g{G}/members                      → array 6 nama anggota
l2_scores/g{G}/{member_id}               → { post, name } dari Excel POST
pre_test/g{G}/{member_id}                → { pre, name } dari Excel PRE
```

## 4 Ronde Simulasi

| Ronde | Skenario | Domain | Amanah Quota |
|-------|----------|--------|--------------|
| R1 | Selisih Kas Pak Bagus | Operasional | 50 koin |
| R2 | Pondok Pesantren Rp 4M | Pembiayaan | 65 koin |
| R3 | Restruktur Konflik | Leadership | 80 koin |
| R4 | Crisis Compliance | Capstone | 100 koin |

## 5 Kelompok Simulasi

Borobudur · Prambanan · Diponegoro · Gajah Mada · Majapahit (6 anggota tiap kelompok)

## 6 Dimensi Behavior

| Kode | Label | Bobot |
|------|-------|-------|
| QoA  | Quality of Argument | 25% |
| AL   | Active Listening | 15% |
| SA   | Sharia Awareness | 15% |
| RC   | Risk Calibration | 15% |
| EJ   | Ethical Judgment | 15% |
| PI   | Practical Implementation | 15% |

Skor 1-5, kemudian dinormalisasi ke 0-100 untuk perhitungan L3.

## Setup Deployment

### 1. Firebase Setup

```bash
# Buka https://console.firebase.google.com
# Pilih project bsi-next-bm-2026
# Buka Realtime Database > Rules tab
# Paste isi file firebase-rules.json
# Publish
```

Lalu buka **Project Settings > General > Your apps > Web app**, copy konfigurasi Firebase, dan ganti placeholder di setiap file HTML:

```js
const FIREBASE_CONFIG = {
  apiKey: "GANTI_DENGAN_API_KEY_FIREBASE",  // ← ganti di sini
  authDomain: "bsi-next-bm-2026.firebaseapp.com",
  databaseURL: "https://bsi-next-bm-2026-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "bsi-next-bm-2026",
  storageBucket: "bsi-next-bm-2026.appspot.com",
  messagingSenderId: "GANTI_SENDER_ID",       // ← ganti
  appId: "GANTI_APP_ID"                       // ← ganti
};
```

Atau ganti sekali di `scripts/common.py` lalu rebuild semua via `python3 build_*.py`.

### 2. Asset Setup

Letakkan file berikut di `assets/images/`:

- `danantara.png` — logo Danantara (height ~26-28px display)
- `bsi.png` — logo Bank Syariah Indonesia (height ~30-32px display)
- `bg-report-cpi.jpg` — background Islamic geometric teal-gold untuk report individual

Logo akan auto-hide via `onerror` jika file tidak ditemukan, jadi sistem tetap berjalan tanpa logo (untuk testing).

### 3. Deploy ke Vercel

```bash
# Via GitHub (recommended)
git remote add origin https://github.com/ranggairawan10/bsi-next-bm-2026.git
git add .
git commit -m "v2 rebuild · CPI Opsi A architecture"
git push origin main

# Lalu di vercel.com, Import Project dari GitHub repo
# Vercel akan auto-detect static site, deploy dalam 30 detik
```

Atau manual via CLI:

```bash
npm i -g vercel
vercel --prod
```

### 4. Workflow Operasional

**Sebelum simulasi:**
1. Login Master Admin (`BSI2026ADMIN`)
2. Tab Daftar Anggota → isi 30 nama peserta (5 kelompok × 6 anggota)
3. Tab Sesi → set Ronde Aktif ke R1 · pastikan Lock OFF

**Saat simulasi:**
4. Distribusikan kode akses ke fasilitator:
   - 1× GM kode → 1 device proyektor besar (untuk Game Master)
   - 1× LAYAR kode → layar peserta
   - 1× BOARD kode → monitor backstage untuk ranking
   - 5× COACH kode (G1-G5) → 5 fasilitator coach per kelompok
   - 5× LEADER kode (G1-G5) → 1 leader per kelompok
5. Game Master scoring per ronde · Coach scoring 6D + token + narrative · Leader peer scoring
6. Admin pindah ronde via Tab Sesi setelah ronde selesai

**Setelah simulasi:**
7. Login Report (`BSI2026REPORT`)
8. Tab Import L2 Excel → upload Post-Test (wajib) dan Pre-Test (opsional)
9. Tab CPI Calculation → review tabel + filter
10. Tab Report Individual → cetak per peserta (Ctrl+P → Save as PDF)
11. Tab Export → bulk CSV / Print Semua

## Build dari Source

```bash
cd scripts/
python3 build_01_index.py
python3 build_02_gamemaster.py
python3 build_03_board.py
python3 build_04_projector.py
python3 build_05_coach.py
python3 build_06_leader.py
python3 build_07_admin.py
python3 build_08_report.py
```

Atau sekaligus:

```bash
cd scripts/
for f in build_*.py; do python3 "$f"; done
```

Output: 8 file HTML monolitik di `bsi-scoring/`.

## Audit Fix v2 (vs v1)

| ID | Issue v1 | Fix v2 |
|----|----------|--------|
| A1 | Firebase path mismatch GM ↔ Board | Single source of truth via `common.py PATHS` constant |
| A2 | SDK load order race | Firebase CDN di `<head>` sebelum Google Fonts, init di akhir body |
| A3 | localStorage auto-cleared on landing | Hanya clear via `?logout=1` URL param |
| A4 | CSS brace orphan di gamemaster | Modular CSS via Python string concatenation |
| A5 | Broken emoji encoding | UTF-8 strict, emoji replaced dengan SVG icon / text |
| A6 | 16 kode (claim) vs 15 actual | Locked ke 15 kode (1 admin + 1 GM + 1 layar + 1 board + 1 report + 5 coach + 5 leader) |
| A7 | Cross-file data contract | `FIREBASE_PATHS` shared constant · semua file pakai path string identik |
| A8 | report.html missing | Built dengan full CPI Opsi A architecture |

## Lisensi & Kontak

Built untuk BSI Next BM School 2026 oleh HCR.ID.

Kontak teknis: Cahyo Tri Haryanto · cahyo@hcr.id  
Project Lead: Kang Rangga · 0813-2220-2221

BSI Corporate University Group · Branch Banking Simulation 2026
