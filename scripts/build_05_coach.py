"""build_05_coach.py — Branch Coach scoring panel: 6D behavior + narrative."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, FIREBASE_PATHS, GROUP_NAMES,
                    BEHAVIOR_DIMENSIONS,
                    CSS_ROOT, CSS_BUTTONS, CSS_TOAST, CSS_LOGO_ROW,
                    UTILITY_JS, LOGO_ROW_HTML, FOOTER_TEXT, auth_guard)

OUT = '/home/claude/build/bsi-scoring/coach.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + CSS_LOGO_ROW + """
body { background: var(--cream); }
.shell { max-width: 1200px; margin: 0 auto; padding: 16px; }
.topbar { display: flex; align-items: center; justify-content: space-between; padding: 14px 20px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 14px; flex-wrap: wrap; gap: 12px; box-shadow: var(--shadow-sm); }
.topbar h1 { font-size: 16px; font-weight: 700; }
.topbar h1 small { display: block; font-size: 11px; font-weight: 500; color: var(--soft); letter-spacing: 1.2px; text-transform: uppercase; margin-top: 2px; }
.group-badge { display: inline-flex; align-items: center; gap: 7px; padding: 5px 11px; background: var(--teal); color: #fff; border-radius: 999px; font-size: 11.5px; font-weight: 700; letter-spacing: .4px; margin-top: 6px; }

.tabs { display: flex; gap: 6px; margin-bottom: 14px; padding: 5px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); overflow-x: auto; }
.tab { flex: 1; min-width: 100px; padding: 10px 8px; background: transparent; border: none; border-radius: 8px; font-family: inherit; font-size: 11.5px; font-weight: 700; color: var(--mid); cursor: pointer; text-align: center; transition: all .2s; }
.tab small { display: block; font-size: 10px; font-weight: 500; color: var(--soft); margin-top: 2px; }
.tab:hover { background: var(--in-bg); color: var(--text); }
.tab.active { background: var(--teal); color: #fff; }
.tab.active small { color: rgba(255,255,255,.78); }

.member-grid { display: grid; grid-template-columns: 200px 1fr; gap: 14px; }
@media(max-width:900px){ .member-grid { grid-template-columns: 1fr; } }

.member-list { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 8px; box-shadow: var(--shadow-sm); height: fit-content; max-height: 70vh; overflow-y: auto; }
.member-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; transition: background .2s; font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
.member-item:hover { background: var(--in-bg); }
.member-item.active { background: var(--teal-10); color: var(--teal-dark); border-left: 3px solid var(--teal); padding-left: 9px; }
.member-num { width: 22px; height: 22px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: var(--in-bg); color: var(--mid); border-radius: 50%; font-size: 10px; font-weight: 700; }
.member-item.active .member-num { background: var(--teal); color: #fff; }
.member-status { margin-left: auto; font-size: 9px; padding: 2px 6px; background: var(--cream); color: var(--soft); border-radius: 4px; font-weight: 700; letter-spacing: .4px; }
.member-status.scored { background: rgba(47,158,102,.15); color: var(--success); }

.scoring-panel { background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 22px; box-shadow: var(--shadow-sm); }
.member-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid var(--border); }
.member-head h2 { font-size: 18px; font-weight: 700; color: var(--text); }
.member-head h2 small { display: block; font-size: 11.5px; font-weight: 500; color: var(--soft); margin-top: 3px; letter-spacing: .4px; }
.save-status { font-size: 11px; color: var(--success); font-weight: 600; padding: 4px 10px; background: rgba(47,158,102,.1); border-radius: 6px; }

.dim-block { margin-bottom: 16px; padding: 14px; background: var(--in-bg); border: 1px solid var(--border); border-radius: 10px; transition: border-color .2s; }
.dim-block:hover { border-color: var(--teal-20); }
.dim-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.dim-label { font-size: 13px; font-weight: 700; color: var(--text); }
.dim-label small { display: block; font-size: 10.5px; font-weight: 500; color: var(--soft); margin-top: 2px; letter-spacing: .3px; text-transform: uppercase; }
.dim-weight { font-size: 10px; padding: 3px 7px; background: var(--white); border: 1px solid var(--border); border-radius: 4px; color: var(--mid); font-weight: 600; }

.scale-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
.scale-btn { padding: 11px 0; border: 1.5px solid var(--border); background: var(--white); border-radius: 8px; cursor: pointer; transition: all .15s; font-family: inherit; }
.scale-btn:hover { border-color: var(--teal); }
.scale-btn .num { display: block; font-size: 16px; font-weight: 800; color: var(--text); line-height: 1; }
.scale-btn .lbl { display: block; font-size: 9px; font-weight: 600; color: var(--soft); margin-top: 4px; letter-spacing: .4px; }
.scale-btn.selected { background: var(--teal); border-color: var(--teal); }
.scale-btn.selected .num, .scale-btn.selected .lbl { color: #fff; }

.token-block { padding: 14px; background: linear-gradient(135deg, rgba(248,173,60,.08), rgba(248,173,60,.02)); border: 1px solid rgba(248,173,60,.25); border-radius: 10px; margin-bottom: 16px; }
.token-block .lbl-head { font-size: 11px; font-weight: 700; color: var(--gold-dark); letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 8px; }
.token-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; }
@media(max-width:600px){ .token-grid { grid-template-columns: repeat(2, 1fr); } }
.token-btn { padding: 8px 6px; background: var(--white); border: 1px solid var(--border); border-radius: 6px; cursor: pointer; font-size: 10.5px; font-weight: 600; color: var(--mid); transition: all .15s; text-align: left; line-height: 1.3; }
.token-btn:hover { border-color: var(--gold); color: var(--gold-dark); }
.token-btn.selected { background: var(--gold); border-color: var(--gold); color: #fff; }

.narrative-block { margin-top: 16px; }
.narrative-block label { display: block; font-size: 11px; font-weight: 700; color: var(--mid); letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px; }
.narrative-block textarea { width: 100%; min-height: 80px; padding: 10px 12px; background: var(--in-bg); border: 1.5px solid var(--border); border-radius: 8px; font-family: inherit; font-size: 13px; color: var(--text); resize: vertical; transition: border-color .2s; line-height: 1.55; }
.narrative-block textarea:focus { outline: none; border-color: var(--teal); background: var(--white); }

.summary-bar { display: flex; gap: 14px; margin-top: 16px; padding: 14px; background: linear-gradient(135deg, rgba(0,163,157,.06), rgba(0,163,157,.02)); border: 1px solid rgba(0,163,157,.18); border-radius: 10px; }
.summary-item { flex: 1; text-align: center; }
.summary-item .lbl { font-size: 9.5px; font-weight: 700; color: var(--mid); letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 4px; }
.summary-item .val { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 800; color: var(--teal-dark); }
"""

JS = FIREBASE_CONFIG + FIREBASE_PATHS + GROUP_NAMES + BEHAVIOR_DIMENSIONS + UTILITY_JS + auth_guard('coach') + """
firebase.initializeApp(FIREBASE_CONFIG);
const db = firebase.database();

const myGroup = parseInt(localStorage.getItem('bsi_group'));
const myGname = localStorage.getItem('bsi_gname');
const myLabel = localStorage.getItem('bsi_label');

const SILABUS_TOKENS = [
  { code: 'BO',  name: 'Banking Operation' },
  { code: 'OC',  name: 'Operation Control' },
  { code: 'FA',  name: 'Financing Analysis' },
  { code: 'PK',  name: 'Product Knowledge' },
  { code: 'AT',  name: 'Accounting & Tax' },
  { code: 'FM',  name: 'Financial Management' },
  { code: 'SP',  name: 'Sales Performance' },
  { code: 'TL',  name: 'Transition to Leadership' },
  { code: 'BBS', name: 'Branch Banking Simulation' }
];

const SCALE_LABELS = ['Belum', 'Mulai', 'Cukup', 'Baik', 'Konsisten'];

const state = {
  currentRound: 1,
  currentMember: 1,
  members: ['Anggota 1', 'Anggota 2', 'Anggota 3', 'Anggota 4', 'Anggota 5', 'Anggota 6'],
  data: {} // data[round][memberId] = { dim: {qoa:..,al:..}, token: 'OC', narrative: '...' }
};

// Init data structure
for (let r = 1; r <= 4; r++) {
  state.data[r] = {};
  for (let m = 1; m <= 6; m++) state.data[r][m] = { dim: {}, token: '', narrative: '' };
}

// ============================================================
// FIREBASE LISTENERS
// ============================================================
db.ref('session/currentRound').on('value', snap => {
  state.currentRound = snap.val() || 1;
  document.querySelectorAll('.round-tab').forEach(t => {
    t.classList.toggle('active', parseInt(t.dataset.round) === state.currentRound);
  });
  renderScoring();
});

db.ref(`coach_data/g${myGroup}`).on('value', snap => {
  const data = snap.val() || {};
  for (let r = 1; r <= 4; r++) {
    const round = data['r' + r] || {};
    for (let m = 1; m <= 6; m++) {
      const md = round['m' + m] || {};
      state.data[r][m] = {
        dim: md.dim || {},
        token: md.token || '',
        narrative: md.narrative || ''
      };
    }
  }
  renderMembers();
  renderScoring();
});

db.ref(`groups/g${myGroup}/members`).on('value', snap => {
  const list = snap.val();
  if (Array.isArray(list) && list.length === 6) {
    state.members = list;
    renderMembers();
  }
});

// ============================================================
// RENDER
// ============================================================
function renderTabs() {
  document.querySelectorAll('.member-tab').forEach(t => {
    t.classList.toggle('active', parseInt(t.dataset.member) === state.currentMember);
  });
}

function renderMembers() {
  const list = document.getElementById('memberList');
  list.innerHTML = '';
  for (let m = 1; m <= 6; m++) {
    const r = state.currentRound;
    const md = state.data[r][m];
    const dimsCount = Object.values(md.dim).filter(v => v > 0).length;
    const isComplete = dimsCount >= 6 && md.token;
    const isPartial = dimsCount > 0 || md.token;
    const status = isComplete ? 'scored' : '';
    const label = isComplete ? 'Selesai' : (isPartial ? 'Draft' : 'Kosong');
    list.innerHTML += `
      <div class="member-item ${m === state.currentMember ? 'active' : ''}" data-member="${m}" onclick="switchMember(${m})">
        <div class="member-num">${m}</div>
        <div>${escapeHTML(state.members[m-1] || 'Anggota ' + m)}</div>
        <div class="member-status ${status}">${label}</div>
      </div>`;
  }
}

function renderScoring() {
  const r = state.currentRound;
  const m = state.currentMember;
  const md = state.data[r][m];

  document.getElementById('memberName').textContent = state.members[m-1] || 'Anggota ' + m;
  document.getElementById('memberMeta').textContent = `${myGname} · Ronde ${r}`;

  // 6 dimensi
  const dimsContainer = document.getElementById('dimsContainer');
  dimsContainer.innerHTML = BEHAVIOR_DIMENSIONS.map(d => {
    const cur = md.dim[d.key] || 0;
    return `
    <div class="dim-block">
      <div class="dim-head">
        <div class="dim-label">${d.label}<small>${d.short}</small></div>
        <div class="dim-weight">${(d.weight*100).toFixed(0)}% bobot</div>
      </div>
      <div class="scale-row">
        ${[1,2,3,4,5].map(v => `
          <button class="scale-btn ${cur === v ? 'selected' : ''}" onclick="setDim('${d.key}', ${v})">
            <span class="num">${v}</span>
            <span class="lbl">${SCALE_LABELS[v-1]}</span>
          </button>`).join('')}
      </div>
    </div>`;
  }).join('');

  // Token (silabus dominan)
  const tokenContainer = document.getElementById('tokenContainer');
  tokenContainer.innerHTML = SILABUS_TOKENS.map(t => `
    <button class="token-btn ${md.token === t.code ? 'selected' : ''}" onclick="setToken('${t.code}')">
      <strong>${t.code}</strong> · ${t.name}
    </button>`).join('');

  // Narrative
  document.getElementById('narrativeInput').value = md.narrative;

  // Summary
  let sumW = 0, sumWeights = 0;
  for (const d of BEHAVIOR_DIMENSIONS) {
    if (md.dim[d.key]) {
      sumW += md.dim[d.key] * d.weight;
      sumWeights += d.weight;
    }
  }
  const avg = sumWeights > 0 ? sumW / sumWeights : 0;
  // Convert 1-5 scale to 0-100 score
  const score = avg > 0 ? ((avg - 1) / 4) * 100 : 0;
  document.getElementById('sumAvg').textContent = avg > 0 ? avg.toFixed(2) : '—';
  document.getElementById('sumScore').textContent = score > 0 ? score.toFixed(0) : '—';
  const filled = Object.values(md.dim).filter(v => v > 0).length;
  document.getElementById('sumFilled').textContent = filled + '/6';
}

// ============================================================
// ACTIONS
// ============================================================
function switchRound(r) {
  state.currentRound = r;
  db.ref('session/currentRound').set(r).catch(()=>{}); // best effort, may fail if not authorized
  document.querySelectorAll('.round-tab').forEach(t => {
    t.classList.toggle('active', parseInt(t.dataset.round) === r);
  });
  renderMembers();
  renderScoring();
}

function switchMember(m) {
  state.currentMember = m;
  renderMembers();
  renderScoring();
}

function setDim(key, val) {
  const r = state.currentRound;
  const m = state.currentMember;
  state.data[r][m].dim[key] = val;
  saveMember();
  renderScoring();
}

function setToken(code) {
  const r = state.currentRound;
  const m = state.currentMember;
  state.data[r][m].token = state.data[r][m].token === code ? '' : code;
  saveMember();
  renderScoring();
}

let saveTimer = null;
function saveMember() {
  const r = state.currentRound;
  const m = state.currentMember;
  const md = state.data[r][m];
  // Debounce
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    db.ref(`coach_data/g${myGroup}/r${r}/m${m}`).set(md).then(() => {
      flashSave();
    }).catch(e => toast('Gagal sync: ' + e.message, 'error'));
  }, 350);
}

document.addEventListener('input', e => {
  if (e.target.id === 'narrativeInput') {
    const r = state.currentRound;
    const m = state.currentMember;
    state.data[r][m].narrative = e.target.value;
    saveMember();
  }
});

function flashSave() {
  const s = document.getElementById('saveStatus');
  s.textContent = 'Tersimpan';
  s.style.opacity = 1;
  setTimeout(() => { s.style.opacity = 0; }, 1200);
}

function logout() {
  if (!confirm('Logout?')) return;
  window.location.href = 'index.html?logout=1';
}

// Init
document.getElementById('coachLabel').textContent = myLabel || 'Branch Coach';
document.getElementById('coachGroup').textContent = myGname || '';
renderTabs();
renderMembers();
renderScoring();
"""

ROUND_TABS_HTML = ""
for r in range(1, 5):
    titles = ['Selisih Kas', 'Pondok 4M', 'Konflik Tim', 'Crisis']
    durs = [25, 35, 30, 40]
    ROUND_TABS_HTML += f'''<button class="tab round-tab" data-round="{r}" onclick="switchRound({r})">RONDE {r}<small>{titles[r-1]} · {durs[r-1]}m</small></button>'''

HTML = html_head('Branch Coach') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="shell">
  <div class="topbar">
    <div>
      {LOGO_ROW_HTML}
    </div>
    <div>
      <h1 id="coachLabel">Branch Coach</h1>
      <div class="group-badge"><span id="coachGroup">Cabang ...</span></div>
    </div>
    <button class="btn btn-ghost btn-sm" onclick="logout()">Keluar</button>
  </div>

  <div class="tabs">{ROUND_TABS_HTML}</div>

  <div class="member-grid">
    <div class="member-list" id="memberList"></div>

    <div class="scoring-panel">
      <div class="member-head">
        <h2 id="memberName">Anggota 1<small id="memberMeta">Ronde 1</small></h2>
        <div class="save-status" id="saveStatus" style="opacity:0;transition:opacity .25s">Tersimpan</div>
      </div>

      <div style="font-size:11px;font-weight:700;color:var(--mid);letter-spacing:1.2px;text-transform:uppercase;margin-bottom:10px;">6 Dimensi Behavior</div>
      <div id="dimsContainer"></div>

      <div class="token-block" style="margin-top:14px">
        <div class="lbl-head">Decision Token · Silabus Dominan dalam Argumen</div>
        <div class="token-grid" id="tokenContainer"></div>
      </div>

      <div class="narrative-block">
        <label>Narrative Coaching · Observasi Spesifik</label>
        <textarea id="narrativeInput" placeholder="Contoh: Memimpin diskusi pembiayaan, mengaitkan akad murabahah dengan kondisi pesantren. Argumen kuat di SA dan EJ tapi RC perlu dipertajam."></textarea>
      </div>

      <div class="summary-bar">
        <div class="summary-item"><div class="lbl">Filled</div><div class="val" id="sumFilled">0/6</div></div>
        <div class="summary-item"><div class="lbl">Avg (1-5)</div><div class="val" id="sumAvg">—</div></div>
        <div class="summary-item"><div class="lbl">Score (0-100)</div><div class="val" id="sumScore">—</div></div>
      </div>
    </div>
  </div>

  <div style="text-align:center;font-size:10.5px;color:var(--soft);margin-top:18px;padding:14px;">{FOOTER_TEXT}</div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'coach.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
