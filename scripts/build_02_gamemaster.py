"""build_02_gamemaster.py — Game Master scoring panel. Fix A1 + A4 + A5."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, FIREBASE_PATHS, GROUP_NAMES,
                    AMANAH_PER_ROUND, CSS_ROOT, CSS_BUTTONS, CSS_TOAST, CSS_LOGO_ROW,
                    UTILITY_JS, LOGO_ROW_HTML, FOOTER_TEXT, auth_guard)

OUT = '/home/claude/build/bsi-scoring/gamemaster.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + CSS_LOGO_ROW + """
body { background: var(--cream); }
.shell { max-width: 1280px; margin: 0 auto; padding: 16px; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 16px; box-shadow: var(--shadow-sm); flex-wrap: wrap; gap: 12px; }
.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-left .logo-row { margin: 0; padding: 6px 12px; }
.topbar-left h1 { font-size: 16px; font-weight: 700; color: var(--text); }
.topbar-left h1 small { display: block; font-size: 10.5px; font-weight: 500; color: var(--soft); letter-spacing: 1.2px; text-transform: uppercase; margin-top: 2px; }
.topbar-right { display: flex; align-items: center; gap: 10px; }
.conn { display: flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 600; padding: 6px 11px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 8px; color: var(--mid); }
.conn-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--soft); transition: background .25s; }
.conn.live .conn-dot { background: var(--success); animation: pl 1.6s infinite; }
.conn.live { color: var(--success); border-color: rgba(47,158,102,.25); background: rgba(47,158,102,.07); }
@keyframes pl { 0%,100% { opacity: 1; } 50% { opacity: .45; } }

.round-tabs { display: flex; gap: 8px; padding: 6px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 16px; box-shadow: var(--shadow-sm); overflow-x: auto; }
.round-tab { flex: 1; min-width: 130px; padding: 11px 14px; background: transparent; border: none; border-radius: 8px; font-family: inherit; font-size: 12px; font-weight: 700; color: var(--mid); cursor: pointer; transition: all .2s; text-align: left; line-height: 1.3; }
.round-tab small { display: block; font-size: 10px; font-weight: 500; color: var(--soft); margin-top: 2px; }
.round-tab:hover { background: var(--in-bg); color: var(--text); }
.round-tab.active { background: var(--teal); color: #fff; box-shadow: 0 4px 12px rgba(0,163,157,.28); }
.round-tab.active small { color: rgba(255,255,255,.78); }

.grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px; }
@media (max-width: 1024px) { .grid { grid-template-columns: 1fr; } }

.panel { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px; box-shadow: var(--shadow-sm); }
.panel-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.panel-title { font-size: 13px; font-weight: 700; color: var(--text); letter-spacing: .3px; }
.panel-title .accent { color: var(--teal); }
.timer-block { display: flex; align-items: center; gap: 10px; }
.timer-display { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 700; color: var(--text); padding: 6px 12px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 8px; min-width: 88px; text-align: center; }
.timer-display.warn { color: var(--warn); border-color: var(--warn); animation: pulse-warn 1s infinite; }
.timer-display.danger { color: var(--danger); border-color: var(--danger); animation: pulse-danger .55s infinite; }
@keyframes pulse-warn { 0%,100% { background: var(--in-bg); } 50% { background: rgba(232,155,42,.15); } }
@keyframes pulse-danger { 0%,100% { background: var(--in-bg); } 50% { background: rgba(229,62,62,.18); } }

.group-row { display: grid; grid-template-columns: 28px 1fr 78px auto; gap: 12px; align-items: center; padding: 12px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 8px; transition: border-color .2s, background .2s; }
.group-row:hover { border-color: var(--teal-20); background: rgba(0,163,157,.03); }
.group-num { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: var(--teal); color: #fff; border-radius: 50%; font-size: 12px; font-weight: 700; }
.group-name { font-size: 13px; font-weight: 700; color: var(--text); }
.group-name small { display: block; font-size: 10px; font-weight: 500; color: var(--soft); margin-top: 2px; }
.group-score { display: flex; align-items: center; justify-content: center; padding: 8px 0; background: var(--white); border: 1.5px solid var(--border); border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; color: var(--text); transition: all .2s; }
.group-score.pos { color: var(--success); border-color: rgba(47,158,102,.35); background: rgba(47,158,102,.06); }
.group-score.neg { color: var(--danger); border-color: rgba(229,62,62,.35); background: rgba(229,62,62,.06); }
.bpm-controls { display: flex; gap: 4px; }
.bpm-btn { width: 30px; height: 30px; padding: 0; font-size: 13px; font-weight: 700; border-radius: 6px; }

.ref-card { padding: 14px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 10px; }
.ref-card-title { font-size: 12px; font-weight: 700; color: var(--teal); margin-bottom: 6px; letter-spacing: .4px; text-transform: uppercase; }
.ref-card-body { font-size: 12.5px; line-height: 1.6; color: var(--text); }
.ref-card-body strong { color: var(--teal-dark); }
.ref-card-body ul { margin-left: 16px; margin-top: 4px; }
.ref-card-body li { margin-bottom: 3px; }

.koin-section { margin-top: 16px; padding: 14px; background: linear-gradient(135deg, rgba(248,173,60,.08), rgba(248,173,60,.02)); border: 1px solid rgba(248,173,60,.25); border-radius: 10px; }
.koin-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.koin-title { font-size: 12px; font-weight: 700; color: var(--gold-dark); letter-spacing: .4px; text-transform: uppercase; }
.koin-quota { font-size: 11px; color: var(--mid); font-weight: 600; }
.koin-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; margin-top: 8px; }
.koin-item { padding: 8px 4px; background: var(--white); border: 1px solid var(--border); border-radius: 8px; text-align: center; }
.koin-item-name { font-size: 10px; font-weight: 600; color: var(--mid); margin-bottom: 4px; }
.koin-item-val { font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700; color: var(--gold-dark); }
.koin-item-controls { display: flex; gap: 3px; margin-top: 5px; }
.koin-btn { flex: 1; padding: 4px 0; font-size: 10px; font-weight: 700; border: 1px solid var(--border); background: var(--in-bg); border-radius: 4px; cursor: pointer; transition: background .15s; color: var(--mid); }
.koin-btn:hover { background: rgba(248,173,60,.15); border-color: var(--gold); color: var(--gold-dark); }

.session-bar { display: flex; gap: 10px; margin-top: 16px; padding: 12px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); align-items: center; box-shadow: var(--shadow-sm); }
.session-bar .info { font-size: 12px; color: var(--mid); margin-right: auto; }
.session-bar .info strong { color: var(--text); }

.kbd { display: inline-block; padding: 1px 5px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 3px; font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--mid); }
"""

JS = FIREBASE_CONFIG + FIREBASE_PATHS + GROUP_NAMES + AMANAH_PER_ROUND + UTILITY_JS + auth_guard('gm') + """

// ============================================================
// FIREBASE INIT (FIX A2: setelah CDN load di head)
// ============================================================
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

// ============================================================
// STATE
// ============================================================
const state = {
  currentRound: 1,
  bpm: { 1: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 2: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 3: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 4: { 1:0, 2:0, 3:0, 4:0, 5:0 } },
  amanah: { 1: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 2: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 3: { 1:0, 2:0, 3:0, 4:0, 5:0 }, 4: { 1:0, 2:0, 3:0, 4:0, 5:0 } },
  timer: { running: false, secs: 0, target: 0, intervalId: null },
  locked: false,
  conn: false
};

const REF_DATA = {
  1: {
    title: 'R1 · Selisih Kas Pak Bagus',
    type: 'Operasional · Internal Control',
    duration: 25,
    body: `<p><strong>Kasus:</strong> Selisih kas Rp 2,8 juta di laci Pak Bagus (Teller Senior) Cabang Garuda. Discrepancy ditemukan H+1 saat reconciliation.</p>
<p><strong>Keputusan kunci:</strong></p><ul>
<li>Investigasi internal silent (kelola sendiri, tutup di buku)</li>
<li>Eskalasi formal ke Internal Audit + lapor BOM</li>
<li>Suspend Teller pending investigation</li>
<li>Run pattern analysis 30 hari ke belakang</li>
</ul>
<p><strong>Probing trigger:</strong> Tanya tentang akad amanah, asas kehati-hatian, fiqh muamalah ta'awun vs zalim.</p>
<p><strong>Sinyal kategorisasi:</strong> Operation Control (primary), Banking Operation (secondary), Leadership transition (trap).</p>`
  },
  2: {
    title: 'R2 · Pondok Pesantren Rp 4M',
    type: 'Pembiayaan · Akad & Risk',
    duration: 35,
    body: `<p><strong>Kasus:</strong> Kyai Romli mengajukan pembiayaan Rp 4M untuk perluasan pesantren. Kelayakan teknis OK, tapi cashflow agak tipis dan agunan 90% LTV.</p>
<p><strong>Keputusan kunci:</strong></p><ul>
<li>Akad: Murabahah / Musyarakah Mutanaqishah / Ijarah Muntahia Bittamlik</li>
<li>Approval di-cabang vs eskalasi Regional</li>
<li>Tenor 5 tahun vs 7 tahun</li>
<li>Asuransi pembiayaan: wajib atau opsional</li>
</ul>
<p><strong>Probing trigger:</strong> Apakah objek pembiayaan termasuk amal jariyah? Bagaimana fiqh murabahah versus musyarakah untuk fasilitas mendidik?</p>
<p><strong>Sinyal kategorisasi:</strong> Financing Analysis (primary), Product Knowledge (primary), Sharia Compliance (secondary), Sales Performance (trap).</p>`
  },
  3: {
    title: 'R3 · Restruktur Konflik',
    type: 'Leadership · OD',
    duration: 30,
    body: `<p><strong>Kasus:</strong> Pak Hartanto (RM Mikro Senior) konflik terbuka dengan Bu Sekar (BSM baru). Hartanto refuse joint visit, Sekar lapor BOM. Tim mikro dengar selisih nilai bisnis vs nilai compliance.</p>
<p><strong>Keputusan kunci:</strong></p><ul>
<li>Mediasi BM langsung vs delegate ke BOM</li>
<li>Restruktur reporting line atau tetap</li>
<li>Coaching Hartanto on transition vs reposisi</li>
<li>Komunikasi tim: silent atau open dialog</li>
</ul>
<p><strong>Probing trigger:</strong> Bagaimana akad mu'amalah dalam konteks workplace conflict? Asas musyawarah dalam SOP BSI?</p>
<p><strong>Sinyal kategorisasi:</strong> Transition to Leadership (primary), Sales Performance Management (secondary), Sharia Awareness (secondary), Operation Control (trap).</p>`
  },
  4: {
    title: 'R4 · Crisis Compliance',
    type: 'Capstone · Multi-faceted',
    duration: 40,
    body: `<p><strong>Kasus:</strong> Audit OJK random found 3 transaksi remittance Rp 200jt yang tidak ter-CDD properly. Pelaku: nasabah lama recommend by RM senior. Audit memberi 14 hari respon.</p>
<p><strong>Keputusan kunci:</strong></p><ul>
<li>Self-reporting OJK atau patch dulu lalu lapor</li>
<li>Suspend transaction nasabah affected</li>
<li>RM senior: warning, demosi, atau dimissal</li>
<li>SOP review cabang: superficial atau holistic</li>
<li>Komunikasi internal: managed atau transparent</li>
</ul>
<p><strong>Probing trigger:</strong> Asas amanah dalam pelaporan otoritas. Risiko reputasional vs fiqh kebenaran.</p>
<p><strong>Sinyal kategorisasi:</strong> Operation Control + Financial Management + Branch Banking Simulation + Transition to Leadership (semua primary, integrative).</p>`
  }
};

// ============================================================
// CONNECTION STATUS
// ============================================================
db.ref('.info/connected').on('value', snap => {
  state.conn = snap.val() === true;
  const c = document.getElementById('connStatus');
  c.classList.toggle('live', state.conn);
  c.querySelector('.conn-text').textContent = state.conn ? 'Live · Firebase' : 'Offline';
});

// ============================================================
// FIREBASE LISTENERS (FIX A1: pakai exact path string)
// ============================================================
db.ref('session').on('value', snap => {
  const s = snap.val() || {};
  if (s.currentRound && s.currentRound !== state.currentRound) {
    state.currentRound = s.currentRound;
    renderTabs();
    renderGroups();
  }
  state.locked = !!s.locked;
  document.getElementById('lockState').textContent = state.locked ? 'TERKUNCI' : 'Aktif';
});

db.ref('bpm_gm').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    const round = data['r' + r] || {};
    for (let g = 1; g <= 5; g++) {
      state.bpm[r][g] = Number(round['g' + g]) || 0;
    }
  }
  renderGroups();
});

db.ref('amanah_coins').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    const round = data['r' + r] || {};
    for (let g = 1; g <= 5; g++) {
      state.amanah[r][g] = Number(round['g' + g]) || 0;
    }
  }
  renderKoin();
});

// ============================================================
// RENDER
// ============================================================
function renderTabs() {
  document.querySelectorAll('.round-tab').forEach(t => {
    const r = parseInt(t.dataset.round);
    t.classList.toggle('active', r === state.currentRound);
  });
  const ref = REF_DATA[state.currentRound];
  document.getElementById('refTitle').textContent = ref.title;
  document.getElementById('refType').textContent = ref.type;
  document.getElementById('refBody').innerHTML = ref.body;
  state.timer.target = ref.duration * 60;
  if (!state.timer.running) {
    state.timer.secs = state.timer.target;
    renderTimer();
  }
}

function renderGroups() {
  const r = state.currentRound;
  for (let g = 1; g <= 5; g++) {
    const v = state.bpm[r][g] || 0;
    const cell = document.getElementById('grp_' + g);
    if (cell) {
      cell.textContent = v > 0 ? '+' + v : v.toString();
      cell.classList.remove('pos', 'neg');
      if (v > 0) cell.classList.add('pos');
      else if (v < 0) cell.classList.add('neg');
    }
  }
}

function renderKoin() {
  const r = state.currentRound;
  const quota = AMANAH_PER_ROUND[r];
  const used = Object.values(state.amanah[r]).reduce((a, b) => a + b, 0);
  document.getElementById('koinQuota').textContent = `${used} / ${quota}`;
  for (let g = 1; g <= 5; g++) {
    const v = state.amanah[r][g] || 0;
    const cell = document.getElementById('koin_' + g);
    if (cell) cell.textContent = v.toString();
  }
}

// ============================================================
// BPM ACTIONS (FIX A1: write ke exact path bpm_gm/r{R}/g{G})
// ============================================================
function bumpBPM(g, delta) {
  if (state.locked) { toast('Session terkunci', 'warn'); return; }
  const r = state.currentRound;
  const cur = state.bpm[r][g] || 0;
  const next = Math.max(-10, Math.min(10, cur + delta));
  if (next === cur) {
    toast(delta > 0 ? 'Sudah maksimal +10' : 'Sudah minimal -10', 'warn');
    return;
  }
  // OPTIMISTIC update
  state.bpm[r][g] = next;
  renderGroups();
  // Firebase write
  db.ref(PATHS.bpmGM(r, g)).set(next).catch(e => {
    toast('Gagal sync: ' + e.message, 'error');
    state.bpm[r][g] = cur;
    renderGroups();
  });
}

function setBPM(g, val) {
  if (state.locked) { toast('Session terkunci', 'warn'); return; }
  const r = state.currentRound;
  const next = Math.max(-10, Math.min(10, val));
  state.bpm[r][g] = next;
  renderGroups();
  db.ref(PATHS.bpmGM(r, g)).set(next);
}

// ============================================================
// AMANAH POINTS
// ============================================================
function bumpKoin(g, delta) {
  if (state.locked) { toast('Session terkunci', 'warn'); return; }
  const r = state.currentRound;
  const quota = AMANAH_PER_ROUND[r];
  const used = Object.values(state.amanah[r]).reduce((a, b) => a + b, 0);
  if (delta > 0 && used + delta > quota) {
    toast(`Quota R${r} habis (${quota} koin)`, 'warn');
    return;
  }
  const cur = state.amanah[r][g] || 0;
  const next = Math.max(0, cur + delta);
  state.amanah[r][g] = next;
  renderKoin();
  db.ref(PATHS.amanah(r, g)).set(next);
}

// ============================================================
// ROUND SWITCH
// ============================================================
function switchRound(r) {
  if (state.locked) { toast('Session terkunci', 'warn'); return; }
  state.currentRound = r;
  db.ref(PATHS.sessionRound()).set(r);
  renderTabs();
  renderGroups();
  renderKoin();
  // Reset timer
  pauseTimer();
  state.timer.secs = REF_DATA[r].duration * 60;
  renderTimer();
}

// ============================================================
// TIMER
// ============================================================
function startTimer() {
  if (state.timer.running) return;
  state.timer.running = true;
  state.timer.intervalId = setInterval(() => {
    if (state.timer.secs <= 0) { pauseTimer(); toast('Waktu habis', 'warn'); return; }
    state.timer.secs--;
    renderTimer();
  }, 1000);
  document.getElementById('timerToggle').textContent = 'Pause';
}
function pauseTimer() {
  if (state.timer.intervalId) clearInterval(state.timer.intervalId);
  state.timer.running = false;
  state.timer.intervalId = null;
  document.getElementById('timerToggle').textContent = 'Mulai';
}
function toggleTimer() { state.timer.running ? pauseTimer() : startTimer(); }
function resetTimer() {
  pauseTimer();
  state.timer.secs = REF_DATA[state.currentRound].duration * 60;
  renderTimer();
}
function renderTimer() {
  const m = Math.floor(state.timer.secs / 60);
  const s = state.timer.secs % 60;
  const disp = document.getElementById('timerDisp');
  disp.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
  disp.classList.remove('warn', 'danger');
  if (state.timer.secs > 0 && state.timer.secs <= 60) disp.classList.add('danger');
  else if (state.timer.secs > 0 && state.timer.secs <= 180) disp.classList.add('warn');
}

// ============================================================
// SESSION CONTROL
// ============================================================
function toggleLock() {
  state.locked = !state.locked;
  db.ref(PATHS.sessionLocked()).set(state.locked);
  toast(state.locked ? 'Session terkunci' : 'Session unlocked', state.locked ? 'warn' : 'success');
}

function logout() {
  if (!confirm('Logout dari Game Master?')) return;
  window.location.href = 'index.html?logout=1';
}

// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === '1' || e.key === '2' || e.key === '3' || e.key === '4') switchRound(parseInt(e.key));
  if (e.key === ' ') { e.preventDefault(); toggleTimer(); }
  if (e.key === 'r' && e.ctrlKey) { e.preventDefault(); resetTimer(); }
});

// Init
renderTabs();
renderGroups();
renderKoin();
"""

GROUP_ROWS_HTML = ""
for g in range(1, 6):
    gname = ['Borobudur', 'Prambanan', 'Diponegoro', 'Gajah Mada', 'Majapahit'][g-1]
    GROUP_ROWS_HTML += f'''
    <div class="group-row">
      <div class="group-num">{g}</div>
      <div class="group-name">Cabang {gname}<small>Kelompok {g}</small></div>
      <div class="group-score" id="grp_{g}">0</div>
      <div class="bpm-controls">
        <button class="btn btn-ghost bpm-btn" onclick="bumpBPM({g}, -1)">−1</button>
        <button class="btn btn-ghost bpm-btn" onclick="bumpBPM({g}, +1)">+1</button>
      </div>
    </div>'''

KOIN_GRID_HTML = ""
for g in range(1, 6):
    gname = ['Boro.', 'Pram.', 'Dipo.', 'Gajah', 'Maja.'][g-1]
    KOIN_GRID_HTML += f'''
    <div class="koin-item">
      <div class="koin-item-name">{gname}</div>
      <div class="koin-item-val" id="koin_{g}">0</div>
      <div class="koin-item-controls">
        <button class="koin-btn" onclick="bumpKoin({g}, -1)">−</button>
        <button class="koin-btn" onclick="bumpKoin({g}, +1)">+</button>
      </div>
    </div>'''

HTML = html_head('Game Master') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div class="topbar-left">
      {LOGO_ROW_HTML}
      <h1>Game Master Panel<small>Branch Banking Simulation 2026</small></h1>
    </div>
    <div class="topbar-right">
      <div class="conn" id="connStatus"><span class="conn-dot"></span><span class="conn-text">Connecting...</span></div>
      <button class="btn btn-ghost btn-sm" onclick="logout()">Keluar</button>
    </div>
  </div>

  <div class="round-tabs">
    <button class="round-tab" data-round="1" onclick="switchRound(1)">RONDE 1<small>Selisih Kas · 25 menit</small></button>
    <button class="round-tab" data-round="2" onclick="switchRound(2)">RONDE 2<small>Pondok Pesantren · 35 menit</small></button>
    <button class="round-tab" data-round="3" onclick="switchRound(3)">RONDE 3<small>Restruktur Konflik · 30 menit</small></button>
    <button class="round-tab" data-round="4" onclick="switchRound(4)">RONDE 4<small>Crisis Compliance · 40 menit</small></button>
  </div>

  <div class="grid">
    <div>
      <div class="panel">
        <div class="panel-head">
          <div class="panel-title">BPM Scoring · <span class="accent" id="curRoundLabel">Ronde Aktif</span></div>
          <div class="timer-block">
            <div class="timer-display" id="timerDisp">00:00</div>
            <button class="btn btn-sm" id="timerToggle" onclick="toggleTimer()">Mulai</button>
            <button class="btn btn-ghost btn-sm" onclick="resetTimer()">Reset</button>
          </div>
        </div>
        {GROUP_ROWS_HTML}

        <div class="koin-section">
          <div class="koin-head">
            <div class="koin-title">Amanah Points · Distribusi Manual</div>
            <div class="koin-quota" id="koinQuota">0 / 0</div>
          </div>
          <div class="koin-grid">{KOIN_GRID_HTML}</div>
        </div>
      </div>
    </div>

    <div>
      <div class="panel">
        <div class="panel-head">
          <div class="panel-title" id="refTitle">Referensi Skenario</div>
        </div>
        <div style="font-size:11px;color:var(--soft);margin-bottom:10px;font-weight:600;letter-spacing:.4px;text-transform:uppercase;" id="refType"></div>
        <div class="ref-card">
          <div class="ref-card-body" id="refBody"></div>
        </div>
        <div style="margin-top:14px;padding:10px;background:var(--in-bg);border-radius:8px;font-size:11px;color:var(--mid);line-height:1.6;">
          <strong style="color:var(--text)">Shortcut keyboard:</strong>
          <span class="kbd">1</span><span class="kbd">2</span><span class="kbd">3</span><span class="kbd">4</span> ganti ronde ·
          <span class="kbd">Space</span> timer ·
          <span class="kbd">Ctrl+R</span> reset
        </div>
      </div>
    </div>
  </div>

  <div class="session-bar">
    <div class="info">Status session: <strong id="lockState">Aktif</strong></div>
    <button class="btn btn-ghost btn-sm" onclick="toggleLock()">Toggle Lock Session</button>
  </div>

  <div style="text-align:center;font-size:10.5px;color:var(--soft);margin-top:18px;padding:14px;">
    {FOOTER_TEXT}
  </div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'gamemaster.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
