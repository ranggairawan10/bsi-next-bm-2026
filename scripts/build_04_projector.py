"""build_04_projector.py — Layar Proyektor untuk peserta. Read-only display."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, FIREBASE_PATHS, GROUP_NAMES, AMANAH_PER_ROUND,
                    CSS_ROOT, CSS_BUTTONS, CSS_TOAST,
                    UTILITY_JS, FOOTER_TEXT, auth_guard)

OUT = '/home/claude/build/bsi-scoring/projector.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + """
body { background: linear-gradient(135deg, #0A1628, #1A2332); color: #fff; min-height: 100vh; overflow: hidden; }
body::before { content: ''; position: fixed; inset: 0; opacity: .15; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cg fill='none' stroke='%2300A39D' stroke-width='0.5'%3E%3Cpolygon points='60,10 110,60 60,110 10,60'/%3E%3Cpolygon points='60,30 90,60 60,90 30,60'/%3E%3C/g%3E%3C/svg%3E"); }
.shell { position: relative; z-index: 10; height: 100vh; display: flex; flex-direction: column; padding: 32px 48px; }
.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; }
.brand { font-size: 13px; font-weight: 700; letter-spacing: 2.6px; text-transform: uppercase; color: var(--gold); }
.brand small { display: block; font-size: 11px; font-weight: 500; color: rgba(255,255,255,.55); letter-spacing: 1.6px; margin-top: 4px; }
.timer-big { font-family: 'JetBrains Mono', monospace; font-size: 56px; font-weight: 800; color: #fff; padding: 14px 28px; background: rgba(255,255,255,.06); border: 2px solid rgba(255,255,255,.1); border-radius: 16px; line-height: 1; min-width: 220px; text-align: center; transition: all .3s; }
.timer-big.warn { color: var(--gold); border-color: var(--gold); background: rgba(248,173,60,.08); }
.timer-big.danger { color: var(--danger); border-color: var(--danger); background: rgba(229,62,62,.12); animation: shake .55s infinite; }
@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-3px)} 75%{transform:translateX(3px)} }

.center { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
.round-label { font-size: 14px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: var(--teal); margin-bottom: 14px; }
.round-title { font-size: clamp(36px, 5vw, 64px); font-weight: 800; line-height: 1.1; margin-bottom: 18px; max-width: 1100px; }
.round-type { font-size: 18px; color: rgba(255,255,255,.65); font-weight: 500; letter-spacing: 1.2px; margin-bottom: 38px; }
.duration { display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px; background: rgba(0,163,157,.12); border: 1px solid var(--teal); border-radius: 999px; font-size: 14px; font-weight: 700; color: var(--teal); letter-spacing: 1.2px; margin-bottom: 36px; }

.standings { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; max-width: 1100px; margin: 0 auto; }
.stand-card { padding: 16px 12px; background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.1); border-radius: 14px; text-align: center; transition: all .35s; }
.stand-card.lead { background: linear-gradient(135deg, rgba(248,173,60,.18), rgba(248,173,60,.04)); border-color: var(--gold); transform: scale(1.06); }
.stand-name { font-size: 13px; font-weight: 700; color: rgba(255,255,255,.85); margin-bottom: 6px; }
.stand-score { font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 800; color: #fff; }
.stand-card.lead .stand-score { color: var(--gold); }

.bottombar { display: flex; justify-content: space-between; align-items: center; margin-top: 28px; font-size: 12px; color: rgba(255,255,255,.5); letter-spacing: .5px; }
.live-pill { display: inline-flex; align-items: center; gap: 6px; }
.live-pill .dot { width: 8px; height: 8px; background: #6FD89A; border-radius: 50%; animation: pl 1.5s infinite; }
@keyframes pl { 0%,100%{opacity:1} 50%{opacity:.4} }
"""

JS = FIREBASE_CONFIG + FIREBASE_PATHS + GROUP_NAMES + AMANAH_PER_ROUND + UTILITY_JS + auth_guard('projector') + """
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

const ROUND_DATA = {
  1: { title: 'Selisih Kas Pak Bagus', type: 'Operasional · Internal Control', duration: 25 },
  2: { title: 'Pembiayaan Pondok Pesantren Rp 4M', type: 'Pembiayaan · Akad & Risk', duration: 35 },
  3: { title: 'Restruktur Konflik Tim Mikro', type: 'Leadership · Organization Development', duration: 30 },
  4: { title: 'Crisis Compliance · Audit OJK', type: 'Capstone · Multi-faceted Decision', duration: 40 }
};

const state = {
  currentRound: 1,
  bpm_gm: { 1:{}, 2:{}, 3:{}, 4:{} },
  bpm_leader: { 1:{}, 2:{}, 3:{}, 4:{} }
};

db.ref('session/currentRound').on('value', snap => {
  state.currentRound = snap.val() || 1;
  renderRound();
});

db.ref('bpm_gm').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    state.bpm_gm[r] = {};
    const round = data['r' + r] || {};
    for (let g = 1; g <= 5; g++) state.bpm_gm[r][g] = Number(round['g' + g]) || 0;
  }
  renderStandings();
});

db.ref('bpm_leader').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    state.bpm_leader[r] = {};
    const round = data['r' + r] || {};
    for (let toG = 1; toG <= 5; toG++) {
      let scores = [];
      for (let fromG = 1; fromG <= 5; fromG++) {
        if (fromG === toG) continue;
        const v = round['from_g' + fromG]?.['to_g' + toG];
        if (typeof v === 'number') scores.push(v);
      }
      state.bpm_leader[r][toG] = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    }
  }
  renderStandings();
});

function bpmTotal(g) {
  let t = 0;
  for (let r = 1; r <= 4; r++) {
    t += ((state.bpm_gm[r][g] || 0) + (state.bpm_leader[r][g] || 0)) / 2;
  }
  return t;
}

function renderRound() {
  const r = state.currentRound;
  const data = ROUND_DATA[r];
  document.getElementById('roundLabel').textContent = `RONDE ${r} DARI 4`;
  document.getElementById('roundTitle').textContent = data.title;
  document.getElementById('roundType').textContent = data.type;
  document.getElementById('duration').textContent = `Durasi ${data.duration} menit`;
}

function renderStandings() {
  const ranking = [];
  for (let g = 1; g <= 5; g++) {
    ranking.push({ g, name: GROUP_NAMES[g], total: bpmTotal(g) });
  }
  ranking.sort((a, b) => b.total - a.total);
  const stands = document.getElementById('standings');
  stands.innerHTML = ranking.map((row, i) => `
    <div class="stand-card ${i === 0 ? 'lead' : ''}">
      <div class="stand-name">${row.name}</div>
      <div class="stand-score">${row.total > 0 ? '+' : ''}${row.total.toFixed(1)}</div>
    </div>`).join('');
}

// Local timer (sync from session/timerStart in Firebase if needed)
let timerInterval = null;
function startLocalTimer() {
  const r = state.currentRound;
  let secs = (ROUND_DATA[r]?.duration || 25) * 60;
  const disp = document.getElementById('timerBig');
  function tick() {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    disp.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    disp.classList.remove('warn', 'danger');
    if (secs > 0 && secs <= 60) disp.classList.add('danger');
    else if (secs > 0 && secs <= 180) disp.classList.add('warn');
    if (secs > 0) secs--;
  }
  tick();
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(tick, 1000);
}

renderRound();
renderStandings();
startLocalTimer();

// Keyboard: F11 fullscreen hint, Escape unlock
document.addEventListener('keydown', e => {
  if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});
"""

HTML = html_head('Layar Proyektor') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div class="brand">BSI Next BM School 2026<small>Branch Banking Simulation</small></div>
    <div class="timer-big" id="timerBig">25:00</div>
  </div>

  <div class="center">
    <div class="round-label" id="roundLabel">RONDE 1 DARI 4</div>
    <h1 class="round-title" id="roundTitle">Selisih Kas Pak Bagus</h1>
    <div class="round-type" id="roundType">Operasional · Internal Control</div>
    <div class="duration" id="duration">Durasi 25 menit</div>

    <div class="standings" id="standings"></div>
  </div>

  <div class="bottombar">
    <div class="live-pill"><span class="dot"></span><span>Live · Sync via Firebase</span></div>
    <div>Tekan F untuk fullscreen · Layar otomatis update</div>
  </div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'projector.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
