"""
build_07_admin.py — Master Admin Dashboard.
Akses: BSI2026ADMIN
Fungsi:
  · Session control (round switch, timer override, lock toggle)
  · Member list editor (groups/g{G}/members) — 6 anggota per kelompok
  · Real-time overview semua kelompok (BPM GM, Leader avg, Coach progress, Amanah)
  · Override BPM GM scores
  · Custom Amanah Points distribution per kelompok
  · Export raw data (JSON download)
  · Reset round / Reset all (destructive guarded)
"""

from common import (
    FIREBASE_CONFIG, ACCESS_MAP, GROUP_NAMES, AMANAH_PER_ROUND,
    BEHAVIOR_DIMENSIONS, CSS_ROOT, GOOGLE_FONTS, FIREBASE_CDN,
    LOGO_ROW_HTML, FIREBASE_PATHS, UTILITY_JS,
    CSS_TOAST, CSS_BUTTONS, CSS_LOGO_ROW, html_head, FOOTER_TEXT,
    auth_guard
)

CSS = CSS_ROOT + CSS_TOAST + CSS_BUTTONS + CSS_LOGO_ROW + """
.shell { max-width: 1280px; margin: 0 auto; padding: 22px 18px 60px; }
.head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; flex-wrap: wrap; gap: 12px; }
.head-left h1 { font-size: 22px; font-weight: 800; letter-spacing: -.4px; color: var(--text); }
.head-left p { font-size: 12px; color: var(--mid); margin-top: 2px; font-weight: 600; }
.head-badge { background: linear-gradient(135deg, var(--teal), var(--teal-dark)); color: #fff; padding: 8px 14px; border-radius: 999px; font-size: 11px; font-weight: 800; letter-spacing: .8px; text-transform: uppercase; box-shadow: 0 4px 14px rgba(0,163,157,.3); }

.tabs { display: flex; gap: 4px; background: var(--white); border: 1px solid var(--border); border-radius: 14px; padding: 5px; margin-bottom: 22px; box-shadow: var(--shadow-sm); overflow-x: auto; }
.tab { flex: 1; min-width: 120px; padding: 11px 14px; border: none; background: transparent; border-radius: 10px; font-size: 12.5px; font-weight: 700; color: var(--mid); cursor: pointer; transition: all .2s; white-space: nowrap; }
.tab:hover { background: var(--in-bg); color: var(--text); }
.tab.active { background: linear-gradient(135deg, var(--teal), var(--teal-dark)); color: #fff; box-shadow: 0 4px 12px rgba(0,163,157,.32); }

.panel { display: none; }
.panel.active { display: block; }

.card { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 22px; box-shadow: var(--shadow-sm); margin-bottom: 18px; }
.card-h { font-size: 14px; font-weight: 800; color: var(--text); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.card-h .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--teal); }
.card-sub { font-size: 12px; color: var(--mid); font-weight: 500; line-height: 1.55; margin-bottom: 14px; }

.session-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
.session-cell { background: var(--in-bg); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px; }
.session-cell label { display: block; font-size: 10.5px; font-weight: 800; color: var(--soft); text-transform: uppercase; letter-spacing: .8px; margin-bottom: 8px; }
.session-cell .val { font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 8px; font-variant-numeric: tabular-nums; }
.session-cell select, .session-cell input { width: 100%; padding: 9px 11px; border: 1.5px solid var(--border); border-radius: 8px; font-size: 13px; font-weight: 700; background: var(--white); font-family: inherit; }
.session-cell select:focus, .session-cell input:focus { border-color: var(--teal); outline: none; }

.lock-row { display: flex; align-items: center; gap: 12px; padding: 12px 16px; background: var(--in-bg); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-top: 14px; }
.lock-row .label { font-size: 13px; font-weight: 700; flex: 1; color: var(--text); }
.lock-row .label small { display: block; font-size: 11px; color: var(--mid); font-weight: 500; margin-top: 2px; }
.toggle { position: relative; width: 50px; height: 26px; background: var(--soft); border-radius: 999px; cursor: pointer; transition: background .2s; flex-shrink: 0; }
.toggle::after { content: ''; position: absolute; left: 3px; top: 3px; width: 20px; height: 20px; background: #fff; border-radius: 50%; transition: left .2s; box-shadow: 0 2px 4px rgba(0,0,0,.2); }
.toggle.on { background: var(--success); }
.toggle.on::after { left: 27px; }

.member-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
.group-block { background: var(--in-bg); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px; }
.group-block h3 { font-size: 13px; font-weight: 800; color: var(--teal-dark); margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.member-input { width: 100%; padding: 8px 11px; border: 1.5px solid var(--border); border-radius: 7px; font-size: 12.5px; background: var(--white); margin-bottom: 6px; font-family: inherit; }
.member-input:focus { border-color: var(--teal); outline: none; }
.member-num { display: inline-block; width: 22px; font-size: 11px; font-weight: 700; color: var(--soft); }

.overview-table { width: 100%; border-collapse: collapse; }
.overview-table th { text-align: left; padding: 10px 12px; font-size: 11px; font-weight: 800; color: var(--soft); text-transform: uppercase; letter-spacing: .8px; border-bottom: 2px solid var(--border); background: var(--in-bg); }
.overview-table td { padding: 12px; font-size: 13px; border-bottom: 1px solid var(--border); font-variant-numeric: tabular-nums; }
.overview-table td.gname { font-weight: 700; color: var(--teal-dark); }
.overview-table td.score { font-weight: 800; }
.overview-table td.score.pos { color: var(--success); }
.overview-table td.score.neg { color: var(--danger); }
.overview-table td.amanah { font-weight: 800; color: var(--gold-dark); }
.overview-table tr:hover td { background: rgba(0,163,157,.03); }

.override-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 12px; }
.override-cell { background: var(--in-bg); border: 1px solid var(--border); border-radius: 8px; padding: 10px; }
.override-cell label { display: block; font-size: 10.5px; font-weight: 800; color: var(--soft); text-transform: uppercase; margin-bottom: 6px; letter-spacing: .6px; }
.override-cell input { width: 100%; padding: 7px 9px; border: 1.5px solid var(--border); border-radius: 6px; font-size: 13px; font-weight: 700; text-align: center; background: var(--white); font-family: inherit; }

.danger-zone { background: rgba(229,62,62,.04); border: 1px dashed var(--danger); border-radius: var(--radius-sm); padding: 16px; margin-top: 16px; }
.danger-zone h4 { font-size: 12px; color: var(--danger); font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .8px; }
.danger-zone p { font-size: 11.5px; color: var(--mid); margin-bottom: 10px; line-height: 1.5; }
.danger-actions { display: flex; gap: 8px; flex-wrap: wrap; }

.actions-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.export-info { font-size: 11.5px; color: var(--mid); flex: 1; min-width: 200px; }

footer { text-align: center; font-size: 11px; color: var(--soft); margin-top: 28px; padding-top: 16px; border-top: 1px dashed var(--border); }

@media (max-width: 700px) {
  .override-grid { grid-template-columns: repeat(2, 1fr); }
  .session-grid { grid-template-columns: 1fr; }
}
"""

GROUP_BLOCKS_HTML = ""
for g in range(1, 6):
    gname_full = ["Cabang Borobudur", "Cabang Prambanan", "Cabang Diponegoro", "Cabang Gajah Mada", "Cabang Majapahit"][g-1]
    inputs = ""
    for m in range(1, 7):
        inputs += f'<div><span class="member-num">{m}.</span><input class="member-input" id="member-g{g}-m{m}" data-group="{g}" data-member="{m}" placeholder="Nama Anggota {m}"></div>\n'
    GROUP_BLOCKS_HTML += f'''
<div class="group-block">
  <h3>Kelompok {g} · {gname_full}</h3>
  {inputs}
</div>
'''

OVERRIDE_GRID_HTML = ""
for g in range(1, 6):
    gn = ["Borobudur", "Prambanan", "Diponegoro", "Gajah Mada", "Majapahit"][g-1]
    OVERRIDE_GRID_HTML += f'''
<div class="override-cell">
  <label>{gn}</label>
  <input type="number" id="override-g{g}" min="-10" max="10" step="1" placeholder="0">
</div>
'''

JS = """
""" + FIREBASE_CONFIG + ACCESS_MAP + GROUP_NAMES + AMANAH_PER_ROUND + BEHAVIOR_DIMENSIONS + FIREBASE_PATHS + UTILITY_JS + auth_guard('admin') + """

firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

let state = {
  currentRound: 1,
  locked: false,
  members: {1:[], 2:[], 3:[], 4:[], 5:[]},
  bpmGM: {1:{}, 2:{}, 3:{}, 4:{}},
  bpmLeader: {},
  coachData: {},
  amanah: {1:{}, 2:{}, 3:{}, 4:{}}
};

// =========================================================
// TAB SWITCHING
// =========================================================
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('panel-' + btn.dataset.tab).classList.add('active');
  });
});

// =========================================================
// SESSION CONTROL
// =========================================================
const roundSelect = document.getElementById('roundSelect');
const lockToggle = document.getElementById('lockToggle');
const timerInput = document.getElementById('timerOverride');

db.ref(PATHS.session()).on('value', snap => {
  const s = snap.val() || {};
  state.currentRound = s.currentRound || 1;
  state.locked = !!s.locked;
  if (roundSelect) roundSelect.value = state.currentRound;
  if (lockToggle) lockToggle.classList.toggle('on', state.locked);
  document.getElementById('curRoundVal').textContent = 'R' + state.currentRound;
  document.getElementById('lockStatus').textContent = state.locked ? 'TERKUNCI' : 'AKTIF';
  document.getElementById('lockStatus').style.color = state.locked ? 'var(--danger)' : 'var(--success)';
  refreshOverview();
});

roundSelect.addEventListener('change', () => {
  const r = parseInt(roundSelect.value);
  db.ref(PATHS.sessionRound()).set(r).then(() => {
    toast('Ronde aktif berpindah ke R' + r, 'success');
  });
});

lockToggle.addEventListener('click', () => {
  const newVal = !state.locked;
  db.ref(PATHS.sessionLocked()).set(newVal).then(() => {
    toast(newVal ? 'Sesi DIKUNCI · skor tidak bisa diubah' : 'Sesi DIBUKA', newVal ? 'warn' : 'success');
  });
});

document.getElementById('btnApplyTimer').addEventListener('click', () => {
  const sec = parseInt(timerInput.value);
  if (isNaN(sec) || sec < 0) { toast('Masukkan detik valid', 'error'); return; }
  db.ref('session/timerOverride').set({ seconds: sec, ts: Date.now() }).then(() => {
    toast('Timer override · ' + sec + ' detik dikirim ke Game Master', 'success');
  });
});

// =========================================================
// MEMBER LIST EDITOR
// =========================================================
db.ref(PATHS.groups()).on('value', snap => {
  const g = snap.val() || {};
  for (let i = 1; i <= 5; i++) {
    const mem = (g['g' + i] && g['g' + i].members) || [];
    state.members[i] = mem;
    for (let j = 1; j <= 6; j++) {
      const inp = document.getElementById(`member-g${i}-m${j}`);
      if (inp && inp !== document.activeElement) inp.value = mem[j-1] || '';
    }
  }
});

let memberSaveTimers = {};
document.querySelectorAll('.member-input').forEach(inp => {
  inp.addEventListener('input', () => {
    const g = inp.dataset.group;
    clearTimeout(memberSaveTimers[g]);
    memberSaveTimers[g] = setTimeout(() => saveMemberList(g), 400);
  });
});

function saveMemberList(g) {
  const arr = [];
  for (let j = 1; j <= 6; j++) {
    const v = (document.getElementById(`member-g${g}-m${j}`).value || '').trim();
    arr.push(v);
  }
  db.ref(PATHS.groupMembers(g)).set(arr).then(() => {
    toast('Daftar anggota Kelompok ' + g + ' tersimpan', 'success');
  }).catch(err => toast('Gagal simpan · ' + err.message, 'error'));
}

document.getElementById('btnFillDummy').addEventListener('click', () => {
  if (!confirm('Isi semua nama dengan placeholder dummy (Peserta 1, 2, ...)? Akan menimpa nama yang sudah ada.')) return;
  const updates = {};
  for (let g = 1; g <= 5; g++) {
    const arr = [];
    for (let m = 1; m <= 6; m++) arr.push('Peserta ' + g + '.' + m);
    updates['groups/g' + g + '/members'] = arr;
  }
  db.ref().update(updates).then(() => toast('Placeholder dummy terisi', 'success'));
});

// =========================================================
// REAL-TIME OVERVIEW
// =========================================================
db.ref(PATHS.bpmLeaderRoot()).on('value', s => { state.bpmLeader = s.val() || {}; refreshOverview(); });
db.ref(PATHS.coachRoot()).on('value', s => { state.coachData = s.val() || {}; refreshOverview(); });
db.ref(PATHS.amanahRoot()).on('value', s => { state.amanah = s.val() || {}; refreshOverview(); });

for (let r = 1; r <= 4; r++) {
  db.ref(PATHS.bpmGMRound(r)).on('value', s => { state.bpmGM[r] = s.val() || {}; refreshOverview(); });
}

function refreshOverview() {
  const r = state.currentRound;
  const tbody = document.getElementById('overviewBody');
  if (!tbody) return;
  let rows = '';
  for (let g = 1; g <= 5; g++) {
    const gmScore = (state.bpmGM[r] && state.bpmGM[r]['g' + g]) || 0;
    let leaderSum = 0, leaderCount = 0;
    if (state.bpmLeader && state.bpmLeader['r' + r]) {
      const round = state.bpmLeader['r' + r];
      Object.keys(round).forEach(fromKey => {
        const fromObj = round[fromKey] || {};
        if (fromObj['to_g' + g] && typeof fromObj['to_g' + g].score === 'number') {
          leaderSum += fromObj['to_g' + g].score;
          leaderCount++;
        }
      });
    }
    const leaderAvg = leaderCount > 0 ? leaderSum / leaderCount : 0;
    const combined = (gmScore + leaderAvg) / 2;

    let coachFilled = 0;
    const coachR = state.coachData && state.coachData['g' + g] && state.coachData['g' + g]['r' + r];
    if (coachR) {
      Object.keys(coachR).forEach(mk => {
        const m = coachR[mk] || {};
        const has6D = BEHAVIOR_DIMENSIONS.every(d => typeof m[d.key] === 'number');
        if (has6D) coachFilled++;
      });
    }

    const amanahCustom = (state.amanah[r] && state.amanah[r]['g' + g]) || 0;
    const amanahQuota = AMANAH_PER_ROUND[r];

    rows += `<tr>
      <td class="gname">${escapeHTML(GROUP_NAMES[g])}</td>
      <td class="score ${gmScore > 0 ? 'pos' : (gmScore < 0 ? 'neg' : '')}">${fmtScore(gmScore, 1)}</td>
      <td class="score ${leaderAvg > 0 ? 'pos' : (leaderAvg < 0 ? 'neg' : '')}">${fmtScore(leaderAvg, 1)}</td>
      <td class="score ${combined > 0 ? 'pos' : (combined < 0 ? 'neg' : '')}">${fmtScore(combined, 2)}</td>
      <td>${coachFilled}/6</td>
      <td class="amanah">${amanahCustom}/${amanahQuota}</td>
    </tr>`;
  }
  tbody.innerHTML = rows;
  document.getElementById('overviewRound').textContent = 'R' + r;
}

// =========================================================
// OVERRIDE BPM GM
// =========================================================
document.getElementById('btnApplyOverride').addEventListener('click', () => {
  const r = state.currentRound;
  const updates = {};
  let count = 0;
  for (let g = 1; g <= 5; g++) {
    const inp = document.getElementById('override-g' + g);
    const v = inp.value.trim();
    if (v === '') continue;
    const num = parseFloat(v);
    if (isNaN(num) || num < -10 || num > 10) {
      toast('Skor Kelompok ' + g + ' harus -10 sd +10', 'error');
      return;
    }
    updates['bpm_gm/r' + r + '/g' + g] = num;
    count++;
  }
  if (count === 0) { toast('Tidak ada nilai yang diisi', 'warn'); return; }
  if (!confirm('Override ' + count + ' skor BPM GM untuk R' + r + '? Aksi ini menimpa nilai yang sudah diisi Game Master.')) return;
  db.ref().update(updates).then(() => {
    toast('Override ' + count + ' skor diterapkan untuk R' + r, 'success');
    document.querySelectorAll('.override-cell input').forEach(i => i.value = '');
  }).catch(err => toast('Gagal override · ' + err.message, 'error'));
});

// =========================================================
// CUSTOM AMANAH DISTRIBUTION
// =========================================================
document.getElementById('btnApplyAmanah').addEventListener('click', () => {
  const r = state.currentRound;
  const quota = AMANAH_PER_ROUND[r];
  const updates = {};
  let total = 0;
  const dist = {};
  for (let g = 1; g <= 5; g++) {
    const v = parseInt(document.getElementById('amanah-g' + g).value || '0');
    if (isNaN(v) || v < 0) { toast('Amanah Kelompok ' + g + ' harus 0 atau positif', 'error'); return; }
    dist[g] = v;
    total += v;
  }
  if (total > quota) {
    if (!confirm('Total distribusi (' + total + ') MELEBIHI kuota R' + r + ' (' + quota + '). Lanjutkan?')) return;
  }
  for (let g = 1; g <= 5; g++) updates['amanah_coins/r' + r + '/g' + g] = dist[g];
  db.ref().update(updates).then(() => {
    toast('Amanah Points R' + r + ' tersalurkan · total ' + total + '/' + quota, 'success');
  });
});

// =========================================================
// EXPORT RAW DATA
// =========================================================
document.getElementById('btnExportData').addEventListener('click', () => {
  toast('Mengambil snapshot data...', 'info');
  db.ref().once('value').then(snap => {
    const data = snap.val() || {};
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const ts = new Date().toISOString().slice(0,19).replace(/[:T]/g, '-');
    a.href = url;
    a.download = `bsi-scoring-snapshot-${ts}.json`;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
    toast('Snapshot terunduh', 'success');
  }).catch(err => toast('Gagal export · ' + err.message, 'error'));
});

// =========================================================
// DANGER ZONE
// =========================================================
document.getElementById('btnResetRound').addEventListener('click', () => {
  const r = state.currentRound;
  const conf = prompt(`KONFIRMASI RESET R${r}\\nKetik HAPUS untuk reset semua skor BPM GM, Leader, Coach data, dan Amanah Points untuk R${r}.\\nAksi ini TIDAK BISA dibatalkan.`);
  if (conf !== 'HAPUS') { toast('Reset dibatalkan', 'warn'); return; }
  const updates = {};
  updates['bpm_gm/r' + r] = null;
  updates['bpm_leader/r' + r] = null;
  updates['amanah_coins/r' + r] = null;
  for (let g = 1; g <= 5; g++) updates[`coach_data/g${g}/r${r}`] = null;
  db.ref().update(updates).then(() => toast('R' + r + ' tereset penuh', 'success'));
});

document.getElementById('btnResetAll').addEventListener('click', () => {
  const conf = prompt('KONFIRMASI RESET TOTAL\\nKetik RESET TOTAL untuk menghapus SEMUA data simulasi (BPM, coach, amanah, L2, member).\\nAksi ini TIDAK BISA dibatalkan.');
  if (conf !== 'RESET TOTAL') { toast('Reset dibatalkan', 'warn'); return; }
  const updates = {
    'bpm_gm': null,
    'bpm_leader': null,
    'coach_data': null,
    'amanah_coins': null,
    'l2_scores': null,
    'pre_test': null,
    'session': { currentRound: 1, locked: false }
  };
  db.ref().update(updates).then(() => {
    toast('Reset total selesai', 'success');
    setTimeout(() => location.reload(), 1500);
  });
});

// LOGOUT
document.getElementById('btnLogout').addEventListener('click', () => {
  localStorage.removeItem('bsi_auth');
  localStorage.removeItem('bsi_role');
  localStorage.removeItem('bsi_label');
  localStorage.removeItem('bsi_group');
  localStorage.removeItem('bsi_gname');
  window.location.replace('index.html?logout=1');
});
"""

HTML = html_head("Master Admin") + f'''
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  {LOGO_ROW_HTML}

  <div class="head">
    <div class="head-left">
      <h1>Master Admin Dashboard</h1>
      <p>Kontrol penuh sesi simulasi · BSI Next BM School 2026</p>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
      <span class="head-badge">ADMIN MODE</span>
      <button class="btn btn-ghost btn-sm" id="btnLogout">Keluar</button>
    </div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="session">Sesi &amp; Timer</button>
    <button class="tab" data-tab="overview">Overview Real-Time</button>
    <button class="tab" data-tab="members">Daftar Anggota</button>
    <button class="tab" data-tab="override">Override BPM</button>
    <button class="tab" data-tab="export">Export &amp; Reset</button>
  </div>

  <!-- PANEL: SESI -->
  <div class="panel active" id="panel-session">
    <div class="card">
      <div class="card-h"><span class="dot"></span>Kontrol Sesi</div>
      <div class="card-sub">Pindah ronde aktif, kunci sesi untuk melindungi nilai yang sudah final, override timer ke Game Master.</div>
      <div class="session-grid">
        <div class="session-cell">
          <label>Ronde Aktif</label>
          <div class="val" id="curRoundVal">R1</div>
          <select id="roundSelect">
            <option value="1">R1 · Selisih Kas Pak Bagus (Operasional)</option>
            <option value="2">R2 · Pondok Pesantren Rp 4M (Pembiayaan)</option>
            <option value="3">R3 · Restruktur Konflik (Leadership)</option>
            <option value="4">R4 · Crisis Compliance (Capstone)</option>
          </select>
        </div>
        <div class="session-cell">
          <label>Status Lock</label>
          <div class="val" id="lockStatus">AKTIF</div>
          <small style="font-size: 11px; color: var(--mid); font-weight: 500;">Ketika terkunci, GM/Coach/Leader tidak bisa simpan skor baru.</small>
        </div>
        <div class="session-cell">
          <label>Timer Override (detik)</label>
          <input type="number" id="timerOverride" min="0" placeholder="Misal 1800 = 30 menit">
          <button class="btn btn-sm btn-block" id="btnApplyTimer" style="margin-top: 8px;">Kirim ke Game Master</button>
        </div>
      </div>
      <div class="lock-row">
        <div class="label">Kunci Sesi
          <small>Aktifkan setelah simulasi selesai untuk melindungi data dari perubahan tidak sengaja.</small>
        </div>
        <div class="toggle" id="lockToggle"></div>
      </div>
    </div>
  </div>

  <!-- PANEL: OVERVIEW -->
  <div class="panel" id="panel-overview">
    <div class="card">
      <div class="card-h"><span class="dot"></span>Overview Real-Time · <span id="overviewRound">R1</span></div>
      <div class="card-sub">Skor langsung dari Firebase. BPM Combined = (GM + rerata Leader) / 2. Coach progress = jumlah peserta yang sudah dinilai 6 dimensi behavior.</div>
      <table class="overview-table">
        <thead>
          <tr>
            <th>Kelompok</th>
            <th>BPM GM</th>
            <th>BPM Leader (rerata)</th>
            <th>BPM Combined</th>
            <th>Coach 6D</th>
            <th>Amanah Coins</th>
          </tr>
        </thead>
        <tbody id="overviewBody"></tbody>
      </table>
    </div>
  </div>

  <!-- PANEL: ANGGOTA -->
  <div class="panel" id="panel-members">
    <div class="card">
      <div class="card-h"><span class="dot"></span>Daftar Anggota Kelompok</div>
      <div class="card-sub">6 anggota per kelompok. Nama tersimpan otomatis 400ms setelah berhenti mengetik. Coach &amp; Leader akan langsung melihat perubahan ini.</div>
      <div class="member-grid">
        {GROUP_BLOCKS_HTML}
      </div>
      <div style="margin-top: 14px;">
        <button class="btn btn-ghost btn-sm" id="btnFillDummy">Isi Placeholder Dummy</button>
      </div>
    </div>
  </div>

  <!-- PANEL: OVERRIDE -->
  <div class="panel" id="panel-override">
    <div class="card">
      <div class="card-h"><span class="dot"></span>Override BPM Game Master · Ronde Aktif</div>
      <div class="card-sub">Mode darurat ketika perlu mengoreksi skor GM tanpa membuka panel GM. Skor -10 sampai +10. Kosongkan kolom yang tidak ingin diubah.</div>
      <div class="override-grid">
        {OVERRIDE_GRID_HTML}
      </div>
      <div style="margin-top: 14px; display: flex; gap: 10px; justify-content: flex-end;">
        <button class="btn btn-gold" id="btnApplyOverride">Terapkan Override</button>
      </div>
    </div>

    <div class="card">
      <div class="card-h"><span class="dot"></span>Distribusi Amanah Points · Ronde Aktif</div>
      <div class="card-sub">Salurkan kuota Amanah ke kelompok yang berhak menerima. R1 50 koin · R2 65 · R3 80 · R4 100. Total boleh kurang dari kuota.</div>
      <div class="override-grid">
        <div class="override-cell"><label>Borobudur</label><input type="number" id="amanah-g1" min="0" placeholder="0"></div>
        <div class="override-cell"><label>Prambanan</label><input type="number" id="amanah-g2" min="0" placeholder="0"></div>
        <div class="override-cell"><label>Diponegoro</label><input type="number" id="amanah-g3" min="0" placeholder="0"></div>
        <div class="override-cell"><label>Gajah Mada</label><input type="number" id="amanah-g4" min="0" placeholder="0"></div>
        <div class="override-cell"><label>Majapahit</label><input type="number" id="amanah-g5" min="0" placeholder="0"></div>
      </div>
      <div style="margin-top: 14px; display: flex; gap: 10px; justify-content: flex-end;">
        <button class="btn btn-gold" id="btnApplyAmanah">Salurkan Amanah</button>
      </div>
    </div>
  </div>

  <!-- PANEL: EXPORT -->
  <div class="panel" id="panel-export">
    <div class="card">
      <div class="card-h"><span class="dot"></span>Export Data Mentah</div>
      <div class="card-sub">Unduh snapshot lengkap database simulasi dalam format JSON untuk arsip atau analisis di luar sistem.</div>
      <div class="actions-row">
        <span class="export-info">Snapshot mencakup: BPM GM, BPM Leader, Coach data 6D, Amanah Points, L2 scores, daftar anggota, dan state sesi.</span>
        <button class="btn" id="btnExportData">Unduh Snapshot JSON</button>
      </div>
    </div>

    <div class="card">
      <div class="card-h" style="border-bottom-color: var(--danger);"><span class="dot" style="background: var(--danger);"></span>Danger Zone</div>
      <div class="danger-zone">
        <h4>Reset Ronde Aktif</h4>
        <p>Hapus semua skor BPM GM, Leader, Coach data, dan Amanah Points untuk ronde yang sedang aktif. Daftar anggota dan L2 scores tidak terhapus.</p>
        <div class="danger-actions">
          <button class="btn btn-danger btn-sm" id="btnResetRound">Reset Ronde Aktif</button>
        </div>
      </div>
      <div class="danger-zone">
        <h4>Reset Total Simulasi</h4>
        <p>Hapus SELURUH data simulasi (BPM, coach, amanah, L2, daftar anggota). Sistem kembali ke kondisi awal. Konfirmasi memerlukan pengetikan kata kunci.</p>
        <div class="danger-actions">
          <button class="btn btn-danger btn-sm" id="btnResetAll">Reset Total</button>
        </div>
      </div>
    </div>
  </div>

  <footer>{FOOTER_TEXT}</footer>
</div>

<script>
{JS}
</script>
</body>
</html>
'''

OUT = '/home/claude/build/bsi-scoring/admin.html'
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"admin.html: {len(HTML)} bytes, {HTML.count(chr(10))} lines")
