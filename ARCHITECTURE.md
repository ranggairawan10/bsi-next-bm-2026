# BSI Next BM School · Scoring System v2
## Firestore Collection Architecture

---

### /session · document: "current"
```
phase         : 'lobby' | 'r1_brief' | 'r1_run' | 'r1_score' | 'r1_debrief'
                  | 'r2_brief' | ... | 'post' | 'ended'
currentRound  : 0-4  (0 = lobby/pre)
timerEnd      : Firestore Timestamp | null
message       : string  (GM broadcast ke projector)
updatedAt     : Timestamp
```

---

### /groups · 5 documents: borobudur | prambanan | diponegoro | gajahmada | majapahit
```
name          : "Borobudur" etc
index         : 0-4
color         : hex
members       : [{id:"m0", name:"..."}, ... x6]  (diisi admin)
totalAmanah   : number  (kumulatif semua ronde)
updatedAt     : Timestamp
```

---

### /rounds · 4 documents: r1 | r2 | r3 | r4
```
number        : 1-4
title         : "Selisih Kas Pak Bagus" etc
category      : "Operasional" | "Pembiayaan" | "Leadership" | "Capstone"
maxAmanah     : 50 | 65 | 80 | 100
status        : 'pending' | 'active' | 'scoring' | 'completed'
```

---

### /scores · 20 documents: {groupId}_{roundId}  e.g. "borobudur_r1"
```
groupId         : string
roundId         : string
round           : number

-- GM inputs --
gm_bpm          : { cm, risk, people, cs }   // each -10 to +10
gm_deltaCM      : number   // juta rupiah, bisa negatif
gm_amanah       : number   // 0 to round maxAmanah
gm_submitted    : boolean
gm_submittedAt  : Timestamp

-- Leader inputs --
leader_bpm      : { cm, risk, people, cs }
leader_submitted : boolean
leader_submittedAt : Timestamp

-- Coach inputs (per anggota) --
coach_behavior  : {
  m0: { name, qoa, al, sa, rc, ej, pi },   // 1-10 each
  m1: { ... }, ... m5: { ... }
}
coach_submitted : boolean
coach_submittedAt : Timestamp

-- Computed (recomputed on every GM/Leader/Coach submit) --
bpm_combined    : { cm, risk, people, cs }   // avg GM+Leader
bpm_aggregate   : number   // weighted -10 to +10
bpm_normalized  : number   // 0-100
avg_6d          : { m0..m5 }  // per member, 0-100
l3_per_member   : { m0..m5 }  // 0-100
l3_group_avg    : number   // 0-100

group_score     : number   // for leaderboard (see formula)
locked          : boolean
updatedAt       : Timestamp
```

---

### /participants · 30 documents: {groupId}_m{0-5}  e.g. "borobudur_m0"
```
name          : string
groupId       : string
memberIndex   : 0-5
postTestScore : number  (0-100, from L2 Bank Soal)
indeksPost    : 1-4     (A=4, B=3, C=2, D=1)
l3Scores      : { r1, r2, r3, r4 }  (0-100 each)
avgL3         : number  (0-100)
indeksSim     : 1-4
cpi           : number
grade         : 'A'|'B'|'C'|'D'
status        : 'LULUS'|'BELUM LULUS'
updatedAt     : Timestamp
```

---

## Formula Implementations

### BPM Combined (per indicator)
```
bpm_combined.X = (gm_bpm.X + leader_bpm.X) / 2
```

### BPM Aggregate Weighted (-10 to +10)
```
bpm_aggregate = 0.40*CM + 0.25*Risk + 0.20*People + 0.15*CS
```

### BPM Normalized (0-100)
```
bpm_normalized = (bpm_aggregate + 10) / 20 * 100
```

### 6D Weighted Score per member (0-100)
```
score_6d = (qoa*0.25 + al*0.15 + sa*0.15 + rc*0.15 + ej*0.15 + pi*0.15) * 10
// Dimension scale: 1-10 → result: 10-100
```

### L3 per member per round (0-100)
```
l3 = (bpm_normalized * 0.30) + (score_6d * 0.70)
```

### IndeksSim (after 4 rounds)
```
avgL3 = (l3_r1 + l3_r2 + l3_r3 + l3_r4) / 4
indeksSim: avgL3 >= 90 → 4, >= 80 → 3, >= 70 → 2, < 70 → 1
```

### CPI
```
cpi = (indeksPost * 2 + indeksSim * 16) / 18
status: cpi >= 3.00 → 'LULUS', else 'BELUM LULUS'
```

### Group Score per round (leaderboard)
```
// ΔCM rupiah = primary anchor (70%)
// BPM weighted normalized = secondary (30%)
// Normalization: relative to max abs value across 5 groups this round
normalized_deltaCM = deltaCM / max(|deltaCM_all_groups|) * 100
group_score = 0.70 * normalized_deltaCM + 0.30 * bpm_normalized
```

### BPM Weighted for group leaderboard (per memory: locked)
```
BPM_weighted_display = 40%*CM + 25%*Risk + 20%*People + 15%*CS
```

---

## Access Code → Role → Group Mapping
```
BSI2026ADMIN   → admin.html     (role: admin,     group: null)
BSI2026GM      → gamemaster.html(role: gm,         group: null)
BSI2026LAYAR   → projector.html (role: projector,  group: null)
BSI2026BOARD   → board.html     (role: board,      group: null)
BSI2026REPORT  → report.html    (role: report,     group: null)
COACH2026G1    → coach.html     (role: coach,      group: borobudur)
COACH2026G2    → coach.html     (role: coach,      group: prambanan)
COACH2026G3    → coach.html     (role: coach,      group: diponegoro)
COACH2026G4    → coach.html     (role: coach,      group: gajahmada)
COACH2026G5    → coach.html     (role: coach,      group: majapahit)
LEADER2026G1   → leader.html    (role: leader,     group: borobudur)
LEADER2026G2   → leader.html    (role: leader,     group: prambanan)
LEADER2026G3   → leader.html    (role: leader,     group: diponegoro)
LEADER2026G4   → leader.html    (role: leader,     group: gajahmada)
LEADER2026G5   → leader.html    (role: leader,     group: majapahit)
```
Total: 15 kode (memory mention 16 — possibly 1 observer/viewer code TBD)

---

## v1 Bug Fix Strategy

Root cause: GM writes tidak propagate ke Board (onSnapshot detach / path mismatch)

v2 mitigations:
1. Semua writes: `db.collection('scores').doc(id).set({...}, {merge:true})`
2. Board reads: `db.collection('scores').onSnapshot(...)` — collection-level listener
3. Single `firebase.initializeApp()` guard across all pages
4. Connection indicator via `firebase.firestore().collection('_ping')` onSnapshot
5. All listeners attached in `window.addEventListener('load', ...)` after full DOM ready
6. No `enablePersistence()` — training context needs live data, not cached

---

## Firestore Security Rules (Test Mode)
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```
Upgrade ke production rules setelah batch 1 complete.
