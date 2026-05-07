"""build_03_board.py — Visual Board real-time ranking. Fix A1 (correct read path)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, FIREBASE_PATHS, GROUP_NAMES, AMANAH_PER_ROUND,
                    CSS_ROOT, CSS_BUTTONS, CSS_TOAST, CSS_LOGO_ROW,
                    UTILITY_JS, LOGO_ROW_HTML, FOOTER_TEXT, auth_guard)

OUT = '/home/claude/build/bsi-scoring/board.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + CSS_LOGO_ROW + """
body { background: linear-gradient(135deg, #0A1628, #1A2332); color: #fff; min-height: 100vh; }
body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; opacity: .12;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cg fill='none' stroke='%2300A39D' stroke-width='0.4'%3E%3Cpolygon points='30,5 55,30 30,55 5,30'/%3E%3C/g%3E%3C/svg%3E");
}
.shell { position: relative; z-index: 10; max-width: 1400px; margin: 0 auto; padding: 20px; }
.topbar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; padding: 16px 24px; background: rgba(255,255,255,.04); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,.08); border-radius: var(--radius-lg); }
.topbar-left h1 { font-size: 18px; font-weight: 800; letter-spacing: .3px; }
.topbar-left h1 small { display: block; font-size: 10.5px; font-weight: 500; color: rgba(255,255,255,.5); letter-spacing: 1.4px; text-transform: uppercase; margin-top: 3px; }
.topbar-mid { display: flex; gap: 8px; }
.topbar-mid .ind { padding: 6px 12px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.08); border-radius: 8px; font-size: 11px; color: rgba(255,255,255,.65); font-weight: 600; }
.topbar-mid .ind.active { background: var(--teal); color: #fff; border-color: var(--teal); }
.topbar-right { display: flex; align-items: center; gap: 12px; }
.live-pill { display: flex; align-items: center; gap: 7px; padding: 7px 13px; background: rgba(47,158,102,.15); border: 1px solid rgba(47,158,102,.35); border-radius: 999px; font-size: 11.5px; font-weight: 700; color: #6FD89A; }
.live-pill .dot { width: 8px; height: 8px; background: #6FD89A; border-radius: 50%; animation: pl 1.5s infinite; }
@keyframes pl { 0%,100%{opacity:1} 50%{opacity:.45} }

.layout { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
@media(max-width:1024px){ .layout { grid-template-columns: 1fr; } }

.panel { background: rgba(255,255,255,.04); backdrop-filter: blur(14px); border: 1px solid rgba(255,255,255,.08); border-radius: var(--radius-lg); padding: 20px 24px; }
.panel-title { font-size: 12px; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase; color: var(--gold); margin-bottom: 18px; }

.rank-row { display: grid; grid-template-columns: 56px 1fr 130px; gap: 16px; align-items: center; padding: 14px 16px; background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.05); border-radius: 12px; margin-bottom: 10px; transition: all .35s cubic-bezier(.16,1,.3,1); }
.rank-row.rank-1 { background: linear-gradient(90deg, rgba(248,173,60,.18), rgba(248,173,60,.04)); border-color: rgba(248,173,60,.35); }
.rank-row.rank-2 { background: linear-gradient(90deg, rgba(180,180,180,.14), rgba(180,180,180,.03)); border-color: rgba(180,180,180,.28); }
.rank-row.rank-3 { background: linear-gradient(90deg, rgba(205,127,50,.14), rgba(205,127,50,.03)); border-color: rgba(205,127,50,.28); }

.rank-pos { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 800; color: var(--teal); text-align: center; }
.rank-row.rank-1 .rank-pos { color: var(--gold); }
.rank-row.rank-2 .rank-pos { color: #C0C0C0; }
.rank-row.rank-3 .rank-pos { color: #CD7F32; }

.rank-name { font-size: 16px; font-weight: 700; }
.rank-name small { display: block; font-size: 11px; font-weight: 500; color: rgba(255,255,255,.5); margin-top: 2px; letter-spacing: .3px; }

.rank-score { text-align: right; }
.rank-score .total { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: #fff; line-height: 1; }
.rank-score .label { font-size: 10px; font-weight: 600; color: rgba(255,255,255,.5); letter-spacing: 1.2px; text-transform: uppercase; margin-top: 4px; }

.rank-bar-wrap { grid-column: 1/-1; height: 6px; background: rgba(255,255,255,.06); border-radius: 3px; margin-top: 12px; overflow: hidden; }
.rank-bar { height: 100%; background: linear-gradient(90deg, var(--teal), var(--gold)); border-radius: 3px; transition: width .55s cubic-bezier(.16,1,.3,1); }

.breakdown-row { display: grid; grid-template-columns: 1fr repeat(4, 60px) 70px; gap: 8px; align-items: center; padding: 8px 12px; background: rgba(255,255,255,.03); border-radius: 8px; margin-bottom: 6px; font-size: 12.5px; }
.breakdown-row .gname { font-weight: 600; }
.breakdown-row .gname small { display: block; font-size: 10px; color: rgba(255,255,255,.45); margin-top: 1px; }
.breakdown-cell { text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; color: rgba(255,255,255,.85); }
.breakdown-cell.pos { color: #6FD89A; }
.breakdown-cell.neg { color: #FF7B7B; }
.breakdown-total { text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 800; color: var(--gold); }

.breakdown-head { display: grid; grid-template-columns: 1fr repeat(4, 60px) 70px; gap: 8px; padding: 0 12px 8px; font-size: 9.5px; font-weight: 700; color: rgba(255,255,255,.45); letter-spacing: 1.2px; text-transform: uppercase; }
.breakdown-head .h-cell { text-align: center; }
.breakdown-head .h-total { text-align: right; }

.koin-card { padding: 14px 16px; background: linear-gradient(135deg, rgba(248,173,60,.12), rgba(248,173,60,.02)); border: 1px solid rgba(248,173,60,.25); border-radius: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.koin-card .gname { font-size: 14px; font-weight: 700; }
.koin-card .gname small { display: block; font-size: 10px; color: rgba(255,255,255,.5); margin-top: 2px; }
.koin-card .kcount { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 800; color: var(--gold); }
.koin-card .kcount small { font-size: 10px; color: rgba(255,255,255,.5); margin-left: 4px; font-weight: 500; letter-spacing: 0.6px; }

.dim { padding: 10px 14px; background: rgba(0,163,157,.08); border: 1px solid rgba(0,163,157,.2); border-radius: 8px; font-size: 11px; color: rgba(255,255,255,.85); margin-bottom: 8px; line-height: 1.5; }
.dim strong { color: var(--teal); }
"""

JS = FIREBASE_CONFIG + FIREBASE_PATHS + GROUP_NAMES + AMANAH_PER_ROUND + UTILITY_JS + auth_guard('board') + """
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

const state = {
  currentRound: 1,
  bpm_gm: { 1:{}, 2:{}, 3:{}, 4:{} },
  bpm_leader: { 1:{}, 2:{}, 3:{}, 4:{} },
  amanah: { 1:{}, 2:{}, 3:{}, 4:{} }
};

// ============================================================
// FIREBASE LISTENERS (FIX A1: read paths matching GM write paths)
// ============================================================
db.ref('session').on('value', snap => {
  const s = snap.val() || {};
  if (s.currentRound) state.currentRound = s.currentRound;
  document.querySelectorAll('.ind').forEach(ind => {
    const r = parseInt(ind.dataset.round);
    ind.classList.toggle('active', r === state.currentRound);
  });
  render();
});

// FIX A1: Read SAMA path yang GM write (bpm_gm/r{R}/g{G})
db.ref('bpm_gm').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    state.bpm_gm[r] = {};
    const round = data['r' + r] || {};
    for (let g = 1; g <= 5; g++) {
      state.bpm_gm[r][g] = Number(round['g' + g]) || 0;
    }
  }
  render();
});

// Aggregate leader peer scores (rata-rata penilaian dari kelompok lain ke kelompok target)
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
      state.bpm_leader[r][toG] = scores.length > 0
        ? scores.reduce((a, b) => a + b, 0) / scores.length
        : 0;
    }
  }
  render();
});

db.ref('amanah_coins').on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    state.amanah[r] = {};
    const round = data['r' + r] || {};
    for (let g = 1; g <= 5; g++) {
      state.amanah[r][g] = Number(round['g' + g]) || 0;
    }
  }
  render();
});

db.ref('.info/connected').on('value', snap => {
  const live = snap.val() === true;
  const pill = document.getElementById('livePill');
  pill.style.opacity = live ? 1 : 0.4;
  pill.querySelector('span:last-child').textContent = live ? 'LIVE · Real-time' : 'Reconnecting...';
});

// ============================================================
// COMPUTE BPM_combined per ronde per kelompok
// BPM_combined = (GM + Leader_avg) / 2
// ============================================================
function bpmCombined(r, g) {
  const gm = state.bpm_gm[r][g] || 0;
  const ld = state.bpm_leader[r][g] || 0;
  return (gm + ld) / 2;
}

function bpmTotal(g) {
  let total = 0;
  for (let r = 1; r <= 4; r++) total += bpmCombined(r, g);
  return total;
}

// ============================================================
// RENDER
// ============================================================
function render() {
  // Ranking by total BPM
  const ranking = [];
  for (let g = 1; g <= 5; g++) {
    ranking.push({ g, name: GROUP_NAMES[g], total: bpmTotal(g) });
  }
  ranking.sort((a, b) => b.total - a.total);

  const rankList = document.getElementById('rankList');
  const maxAbs = Math.max(...ranking.map(r => Math.abs(r.total)), 5);
  rankList.innerHTML = ranking.map((row, i) => {
    const pos = i + 1;
    const pct = maxAbs > 0 ? Math.max(8, (Math.abs(row.total) / maxAbs) * 100) : 8;
    return `
      <div class="rank-row rank-${pos}">
        <div class="rank-pos">${pos}</div>
        <div class="rank-name">${row.name}<small>Kelompok ${row.g}</small></div>
        <div class="rank-score">
          <div class="total">${row.total > 0 ? '+' : ''}${row.total.toFixed(1)}</div>
          <div class="label">BPM Combined</div>
        </div>
        <div class="rank-bar-wrap"><div class="rank-bar" style="width:${pct}%"></div></div>
      </div>`;
  }).join('');

  // Breakdown per ronde
  const bd = document.getElementById('breakdown');
  bd.innerHTML = '';
  for (let g = 1; g <= 5; g++) {
    const cells = [];
    for (let r = 1; r <= 4; r++) {
      const v = bpmCombined(r, g);
      const cls = v > 0 ? 'pos' : (v < 0 ? 'neg' : '');
      cells.push(`<div class="breakdown-cell ${cls}">${v > 0 ? '+' : ''}${v.toFixed(1)}</div>`);
    }
    const tot = bpmTotal(g);
    bd.innerHTML += `
      <div class="breakdown-row">
        <div class="gname">${GROUP_NAMES[g]}<small>Kelompok ${g}</small></div>
        ${cells.join('')}
        <div class="breakdown-total">${tot > 0 ? '+' : ''}${tot.toFixed(1)}</div>
      </div>`;
  }

  // Amanah Points
  const koinBox = document.getElementById('koinBox');
  let totalKoin = 0, ranking2 = [];
  for (let g = 1; g <= 5; g++) {
    let sum = 0;
    for (let r = 1; r <= 4; r++) sum += state.amanah[r][g] || 0;
    totalKoin += sum;
    ranking2.push({ g, name: GROUP_NAMES[g], n: sum });
  }
  ranking2.sort((a, b) => b.n - a.n);
  const totalQuota = Object.values(AMANAH_PER_ROUND).reduce((a, b) => a + b, 0);
  koinBox.innerHTML = ranking2.map(row => `
    <div class="koin-card">
      <div class="gname">${row.name}<small>Kelompok ${row.g}</small></div>
      <div class="kcount">${row.n}<small>/ ${totalQuota}</small></div>
    </div>`).join('');
}

render();
"""

HTML = html_head('Visual Board') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div class="topbar-left">
      <h1>Visual Board · Real-Time Ranking<small>BSI Next BM School 2026 · Branch Banking Simulation</small></h1>
    </div>
    <div class="topbar-mid">
      <div class="ind" data-round="1">R1</div>
      <div class="ind" data-round="2">R2</div>
      <div class="ind" data-round="3">R3</div>
      <div class="ind" data-round="4">R4</div>
    </div>
    <div class="topbar-right">
      <div class="live-pill" id="livePill"><span class="dot"></span><span>Connecting...</span></div>
    </div>
  </div>

  <div class="layout">
    <div class="panel">
      <div class="panel-title">Ranking BPM Combined · Akumulasi 4 Ronde</div>
      <div id="rankList"></div>
      <div class="dim" style="margin-top:18px"><strong>BPM Combined</strong> = (GM Score + Group Leader Peer Score) / 2 · Skala −10 hingga +10 per ronde · Akumulasi maksimum +40, minimum −40.</div>

      <div class="panel-title" style="margin-top:24px;color:var(--teal)">Breakdown per Ronde</div>
      <div class="breakdown-head">
        <div></div>
        <div class="h-cell">R1</div><div class="h-cell">R2</div><div class="h-cell">R3</div><div class="h-cell">R4</div>
        <div class="h-total">Total</div>
      </div>
      <div id="breakdown"></div>
    </div>

    <div class="panel">
      <div class="panel-title">Amanah Points · Akumulasi</div>
      <div id="koinBox"></div>
      <div class="dim" style="margin-top:14px"><strong>Amanah Points</strong> · Distribusi koin manual oleh Game Master untuk perilaku kompeten · Quota R1 50 · R2 65 · R3 80 · R4 100 · Total 295 koin per batch.</div>
    </div>
  </div>

  <div style="text-align:center;font-size:11px;color:rgba(255,255,255,.4);margin-top:24px;padding:14px;">
    {FOOTER_TEXT}
  </div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'board.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
