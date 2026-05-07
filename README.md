# BSI Next BM School 2026
## Branch Banking Simulation Based Assessment — Sistem Penilaian Real-Time

---

## Setup Firebase (10 menit, gratis)

### Step 1 — Buat Project Firebase
1. Buka https://console.firebase.google.com
2. Klik **"Add project"** → beri nama misalnya `bsi-bm-school-2026`
3. Disable Google Analytics (tidak perlu) → **Create project**

### Step 2 — Aktifkan Realtime Database
1. Di sidebar kiri, klik **Build → Realtime Database**
2. Klik **"Create Database"**
3. Pilih lokasi: **Singapore (asia-southeast1)**
4. Mode awal: pilih **"Start in test mode"** (kita akan secure setelah testing)
5. Klik **Enable**

### Step 3 — Copy Config
1. Di sidebar kiri, klik ikon **⚙️ (Project Settings)**
2. Scroll ke bawah ke bagian **"Your apps"**
3. Klik ikon **`</>`** (Web app)
4. Register app dengan nama apapun, lanjut
5. Copy blok `firebaseConfig` yang muncul — bentuknya seperti ini:
```js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "bsi-bm-school-2026.firebaseapp.com",
  databaseURL: "https://bsi-bm-school-2026-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "bsi-bm-school-2026",
  storageBucket: "bsi-bm-school-2026.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};
```

### Step 4 — Paste Config ke Semua File HTML
Di setiap file HTML (index.html, admin.html, gamemaster.html, dll), cari blok:
```js
const FIREBASE_CONFIG = {
  apiKey: "GANTI_DENGAN_API_KEY_FIREBASE",
  ...
```
Ganti semua nilai `"GANTI_..."` dengan nilai dari Firebase config Anda.

**File yang perlu diupdate:**
- [ ] index.html
- [ ] admin.html
- [ ] gamemaster.html
- [ ] projector.html
- [ ] coach.html
- [ ] leader.html
- [ ] board.html

### Step 5 — Deploy ke Vercel
1. Push semua file ke GitHub repository
2. Buka https://vercel.com → Import repository
3. Deploy — selesai, URL live otomatis tersedia

---

## Kode Akses Default

| Role | Kode Akses | Catatan |
|------|-----------|---------|
| Master Admin | `BSI2026ADMIN` | Ganti sebelum event |
| Game Master | `BSI2026GM` | |
| Layar Proyektor | `BSI2026LAYAR` | |
| Visual Board | `BSI2026BOARD` | |
| Branch Coach Kel. 1 | `COACH2026G1` | |
| Branch Coach Kel. 2 | `COACH2026G2` | |
| Branch Coach Kel. 3 | `COACH2026G3` | |
| Branch Coach Kel. 4 | `COACH2026G4` | |
| Branch Coach Kel. 5 | `COACH2026G5` | |
| Group Leader Kel. 1 | `LEADER2026G1` | |
| Group Leader Kel. 2 | `LEADER2026G2` | |
| Group Leader Kel. 3 | `LEADER2026G3` | |
| Group Leader Kel. 4 | `LEADER2026G4` | |
| Group Leader Kel. 5 | `LEADER2026G5` | |

Kode akses bisa diubah di blok `ACCESS_MAP` di masing-masing HTML.

---

## Nama Kelompok Default
| Kelompok | Nama Cabang Simulasi |
|----------|---------------------|
| 1 | Cabang Borobudur |
| 2 | Cabang Prambanan |
| 3 | Cabang Diponegoro |
| 4 | Cabang Gajah Mada |
| 5 | Cabang Majapahit |

Nama bisa diubah di blok `GROUP_NAMES` di setiap file HTML.

---

## Struktur File
```
bsi-scoring/
├── index.html          ← Login router
├── admin.html          ← Master Admin dashboard
├── gamemaster.html     ← Game Master scoring panel
├── projector.html      ← Layar proyektor GM (fullscreen)
├── coach.html          ← Branch Coach scoring
├── leader.html         ← Group Leader peer scoring
├── board.html          ← Visual Board real-time ranking
├── vercel.json
└── README.md
```

---

*BSI Corporate University Group · Dokumen Internal · HCR.ID 2026*
