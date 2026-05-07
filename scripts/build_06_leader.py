"""build_06_leader.py — Group Leader Peer BPM Scoring."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, FIREBASE_PATHS, GROUP_NAMES,
                    CSS_ROOT, CSS_BUTTONS, CSS_TOAST, CSS_LOGO_ROW,
                    UTILITY_JS, LOGO_ROW_HTML, FOOTER_TEXT, auth_guard)

OUT = '/home/claude/build/bsi-scoring/leader.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + CSS_LOGO_ROW + """
body { background: var(--cream); }
.shell { max-width: 900px; margin: 0 auto; padding: 16px; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 14px; flex-wrap: wrap; gap: 12px; box-shadow: var(--shadow-sm); }
.topbar h1 { font-size: 16px; font-weight: 700; }
.topbar h1 small { display: block; font-size: 11px; font-weight: 500; color: var(--soft); letter-spacing: 1.2px; text-transform: uppercase; margin-top: 2px; }
.group-badge { display: inline-flex; align-items: center; gap: 7px; padding: 5px 11px; background: var(--gold); color: #fff; border-radius: 999px; font-size: 11.5px; font-weight: 700; letter-spacing: .4px; margin-top: 6px; }

.tabs { display: flex; gap: 6px; margin-bottom: 14px; padding: 5px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.tab { flex: 1; padding: 10px 8px; background: transparent; border: none; border-radius: 8px; font-family: inherit; font-size: 11.5px; font-weight: 700; color: var(--mid); cursor: pointer; text-align: center; transition: all .2s; }
.tab small { display: block; font-size: 10px; font-weight: 500; color: var(--soft); margin-top: 2px; }
.tab:hover { background: var(--in-bg); color: var(--text); }
.tab.active { background: var(--gold); color: #fff; }
.tab.active small { color: rgba(255,255,255,.78); }

.notice { padding: 12px 16px; background: rgba(0,163,157,.06); border: 1px solid rgba(0,163,157,.2); border-radius: 10px; font-size: 12.5px; color: var(--mid); margin-bottom: 14px; line-height: 1.55; }
.notice strong { color: var(--text); }

.peer-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 18px; margin-bottom: 12px; box-shadow: var(--shadow-sm); }
.peer-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.peer-name { font-size: 16px; font-weight: 700; }
.peer-name small { display: block; font-size: 11px; font-weight: 500; color: var(--soft); margin-top: 2px; letter-spacing: .3px; text-transform: uppercase; }
.peer-score-display { display: flex; align-items: center; gap: 6px; padding: 7px 14px; background: var(--in-bg); border: 1.5px solid var(--border); border-radius: 8px; }
.peer-score-display .num { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 800; color: var(--text); }
.peer-score-display.pos { background: rgba(47,158,102,.08); border-color: rgba(47,158,102,.3); }
.peer-score-display.pos .num { color: var(--success); }
.peer-score-display.neg { background: rgba(229,62,62,.08); border-color: rgba(229,62,62,.3); }
.peer-score-display.neg .num { color: var(--danger); }

.scale-strip { display: grid; grid-template-columns: repeat(21, 1fr); gap: 2px; margin-bottom: 8px; }
.scale-cell { padding: 12px 0; border: 1px solid var(--border); background: var(--white); border-radius: 4px; cursor: pointer; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: var(--mid); transition: all .12s; text-align: center; }
.scale-cell:hover { border-color: var(--teal); color: var(--teal); }
.scale-cell.zero { color: var(--soft); }
.scale-cell.active { background: var(--teal); border-color: var(--teal); color: #fff; transform: scale(1.08); box-shadow: 0 4px 12px rgba(0,163,157,.3); }
.scale-cell.active.neg { background: var(--danger); border-color: var(--danger); box-shadow: 0 4px 12px rgba(229,62,62,.3); }
.scale-cell.active.pos { background: var(--success); border-color: var(--success); box-shadow: 0 4px 12px rgba(47,158,102,.3); }
.scale-labels { display: flex; justify-content: space-between; font-size: 10px; font-weight: 600; color: var(--soft); letter-spacing: .5px; padding: 0 4px; margin-bottom: 14px; }

.justify-block label { display: block; font-size: 10.5px; font-weight: 700; color: var(--mid); letter-spacing: 1.1px; text-transform: uppercase; margin-bottom: 5px; }
.justify-block textarea { width: 100%; min-height: 50px; padding: 9px 11px; background: var(--in-bg); border: 1.5px solid var(--border); border-radius: 8px; font-family: inherit; font-size: 12.5px; color: var(--text); resize: vertical; transition: border-color .2s; line-height: 1.5; }
.justify-block textarea:focus { outline: none; border-color: var(--teal); background: var(--white); }

@media(max-width:680px){
  .scale-strip { grid-template-columns: repeat(11, 1fr); }
  .scale-cell:nth-child(even) { display: none; }
}
"""

JS = FIREBASE_CONFIG + FIREBASE_PATHS + GROUP_NAMES + UTILITY_JS + auth_guard('leader') + """
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

const myGroup = parseInt(localStorage.getItem('bsi_group'));
const myGname = localStorage.getItem('bsi_gname');
const myLabel = localStorage.getItem('bsi_label');

const state = {
  currentRound: 1,
  scores: { 1:{}, 2:{}, 3:{}, 4:{} },
  notes:  { 1:{}, 2:{}, 3:{}, 4:{} }
};

db.ref('session/currentRound').on('value', snap => {
  state.currentRound = snap.val() || 1;
  document.querySelectorAll('.round-tab').forEach(t => {
    t.classList.toggle('active', parseInt(t.dataset.round) === state.currentRound);
  });
  renderPeers();
});

db.ref(`bpm_leader`).on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    state.scores[r] = {};
    state.notes[r] = {};
    const round = data['r' + r] || {};
    const fromMe = round[`from_g${myGroup}`] || {};
    for (let g = 1; g <= 5; g++) {
      if (g === myGroup) continue;
      const v = fromMe[`to_g${g}`];
      state.scores[r][g] = typeof v === 'number' ? v : (v && typeof v.score === 'number' ? v.score : 0);
      state.notes[r][g]  = (v && typeof v.note === 'string') ? v.note : '';
    }
  }
  renderPeers();
});

function renderPeers() {
  const container = document.getElementById('peers');
  const r = state.currentRound;
  let html = '';
  for (let g = 1; g <= 5; g++) {
    if (g === myGroup) continue;
    const cur = state.scores[r][g] || 0;
    const note = state.notes[r][g] || '';

    let cells = '';
    for (let v = -10; v <= 10; v++) {
      const isActive = cur === v;
      const cls = ['scale-cell'];
      if (v === 0) cls.push('zero');
      if (isActive) {
        cls.push('active');
        if (v > 0) cls.push('pos');
        else if (v < 0) cls.push('neg');
      }
      cells += `<button class="${cls.join(' ')}" onclick="setPeer(${g}, ${v})">${v > 0 ? '+' + v : v}</button>`;
    }

    const dispClass = cur > 0 ? 'pos' : (cur < 0 ? 'neg' : '');
    html += `
      <div class="peer-card">
        <div class="peer-head">
          <div class="peer-name">${GROUP_NAMES[g]}<small>Kelompok ${g}</small></div>
          <div class="peer-score-display ${dispClass}"><span class="num">${cur > 0 ? '+' : ''}${cur}</span></div>
        </div>
        <div class="scale-strip">${cells}</div>
        <div class="scale-labels"><span>−10 (sangat rendah)</span><span>0 (netral)</span><span>+10 (sangat tinggi)</span></div>
        <div class="justify-block">
          <label>Justifikasi singkat (opsional)</label>
          <textarea data-target="${g}" placeholder="Contoh: Argumen kuat di akad, tapi underestimate risiko reputasional..." onblur="setNote(${g}, this.value)">${escapeHTML(note)}</textarea>
        </div>
      </div>`;
  }
  container.innerHTML = html;
}

function switchRound(r) {
  state.currentRound = r;
  document.querySelectorAll('.round-tab').forEach(t => {
    t.classList.toggle('active', parseInt(t.dataset.round) === r);
  });
  renderPeers();
}

function setPeer(targetG, score) {
  const r = state.currentRound;
  const note = state.notes[r][targetG] || '';
  state.scores[r][targetG] = score;
  // Save as object {score, note} for richer payload
  db.ref(`bpm_leader/r${r}/from_g${myGroup}/to_g${targetG}`).set({ score, note }).then(() => {
    renderPeers();
  }).catch(e => toast('Gagal sync: ' + e.message, 'error'));
}

function setNote(targetG, note) {
  const r = state.currentRound;
  const score = state.scores[r][targetG] || 0;
  state.notes[r][targetG] = note;
  db.ref(`bpm_leader/r${r}/from_g${myGroup}/to_g${targetG}`).set({ score, note });
}

function logout() {
  if (!confirm('Logout?')) return;
  window.location.href = 'index.html?logout=1';
}

document.getElementById('leaderLabel').textContent = myLabel || 'Group Leader';
document.getElementById('leaderGroup').textContent = myGname || '';
renderPeers();
"""

ROUND_TABS_HTML = ""
for r in range(1, 5):
    titles = ['Selisih Kas', 'Pondok 4M', 'Konflik', 'Crisis']
    ROUND_TABS_HTML += f'<button class="tab round-tab" data-round="{r}" onclick="switchRound({r})">RONDE {r}<small>{titles[r-1]}</small></button>'

HTML = html_head('Group Leader') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div>{LOGO_ROW_HTML}</div>
    <div>
      <h1 id="leaderLabel">Group Leader</h1>
      <div class="group-badge"><span id="leaderGroup">Cabang ...</span></div>
    </div>
    <button class="btn btn-ghost btn-sm" onclick="logout()">Keluar</button>
  </div>

  <div class="tabs">{ROUND_TABS_HTML}</div>

  <div class="notice">
    <strong>Peer BPM Scoring · Skala −10 hingga +10.</strong> Anda menilai 4 kelompok lain berdasarkan kualitas argumen kelompok mereka di ronde aktif. Kelompok sendiri tidak dinilai. Skor di-save otomatis. Justifikasi singkat membantu kalibrasi inter-rater.
  </div>

  <div id="peers"></div>

  <div style="text-align:center;font-size:10.5px;color:var(--soft);margin-top:18px;padding:14px;">{FOOTER_TEXT}</div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'leader.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
