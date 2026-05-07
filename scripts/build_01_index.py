"""build_01_index.py — Login router. Fix A3 (auth race condition)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import (html_head, FIREBASE_CONFIG, ACCESS_MAP, GROUP_NAMES,
                    CSS_ROOT, CSS_BUTTONS, CSS_TOAST, CSS_LOGO_ROW,
                    UTILITY_JS, LOGO_ROW_HTML, FOOTER_TEXT)

OUT = '/home/claude/build/bsi-scoring/index.html'

CSS = CSS_ROOT + CSS_BUTTONS + CSS_TOAST + CSS_LOGO_ROW + """
body { background: var(--cream); position: relative; overflow-x: hidden; }
body::before {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Cg fill='none' stroke='%2300A39D' stroke-width='0.55'%3E%3Cpolygon points='40,3 77,40 40,77 3,40' opacity='0.28'/%3E%3Cpolygon points='40,20 60,40 40,60 20,40' opacity='0.18'/%3E%3C/g%3E%3C/svg%3E");
  opacity: .08;
}
body::after {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 50% 40% at 5% 10%, rgba(0,163,157,.06), transparent),
    radial-gradient(ellipse 40% 35% at 95% 90%, rgba(248,173,60,.07), transparent);
}
.page { position: relative; z-index: 10; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px 16px; }
.card { width: 100%; max-width: 440px; background: var(--white); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 36px 32px 30px; box-shadow: var(--shadow-sm), var(--shadow-lg); animation: rise .55s cubic-bezier(.16,1,.3,1) both; }
@keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
.chip { text-align: center; font-size: 9.5px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: var(--teal); margin-bottom: 6px; }
h1 { text-align: center; font-size: 21px; font-weight: 800; line-height: 1.28; margin-bottom: 5px; }
.sub { text-align: center; font-size: 12px; color: var(--soft); margin-bottom: 18px; }
.accent-line { width: 36px; height: 3px; margin: 0 auto 24px; border-radius: 2px; background: linear-gradient(90deg, var(--teal), var(--gold)); }
.lbl { display: block; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--mid); margin-bottom: 6px; }
.iw { position: relative; margin-bottom: 12px; }
.iw input { width: 100%; background: var(--in-bg); border: 1.5px solid var(--border); border-radius: 10px; padding: 12px 44px 12px 14px; font-family: inherit; font-size: 14px; font-weight: 600; color: var(--text); letter-spacing: 1.5px; outline: none; transition: border-color .2s, box-shadow .2s, background .2s; }
.iw input::placeholder { color: var(--soft); letter-spacing: 0; font-weight: 400; }
.iw input:focus { background: var(--white); border-color: var(--teal); box-shadow: 0 0 0 3px var(--teal-10); }
.iw input.ok { border-color: var(--teal); background: rgba(0,163,157,.04); }
.eye { position: absolute; right: 11px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; padding: 4px; color: var(--soft); display: flex; align-items: center; transition: color .2s; }
.eye:hover { color: var(--text); }
.badge { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: rgba(0,163,157,.07); border: 1px solid var(--teal-20); border-radius: 8px; margin-bottom: 14px; opacity: 0; transform: translateY(4px); transition: opacity .25s, transform .25s; pointer-events: none; }
.badge.on { opacity: 1; transform: translateY(0); }
.dot { width: 7px; height: 7px; background: var(--teal); border-radius: 50%; flex-shrink: 0; animation: pd 1.6s infinite; }
@keyframes pd { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: .35; transform: scale(.7); } }
.bt { font-size: 12px; font-weight: 700; color: var(--teal); }
.bg { margin-left: auto; font-size: 11px; font-weight: 500; color: var(--mid); }
.spin { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,.35); border-top-color: #fff; border-radius: 50%; animation: sp .65s linear infinite; }
@keyframes sp { to { transform: rotate(360deg); } }
.btn .spin { display: none; }
.btn.ld .spin { display: block; }
.btn.ld .bl { opacity: .65; }
.err { margin-top: 10px; font-size: 12px; text-align: center; color: var(--danger); min-height: 16px; opacity: 0; transition: opacity .2s; }
.err.on { opacity: 1; }
.foot { margin-top: 18px; font-size: 10.5px; color: var(--soft); text-align: center; line-height: 1.6; }
.foot a { color: var(--teal); text-decoration: none; font-weight: 600; }
@media (max-width: 440px) {
  .card { padding: 26px 20px 22px; }
  h1 { font-size: 18px; }
}
"""

JS = FIREBASE_CONFIG + ACCESS_MAP + GROUP_NAMES + UTILITY_JS + """
// ============================================================
// AUTH FLOW (FIX A3: hanya clear pada explicit logout via ?logout=1)
// ============================================================
(function handleLogout() {
  const params = new URLSearchParams(location.search);
  if (params.get('logout') === '1') {
    ['bsi_auth','bsi_role','bsi_group','bsi_gname','bsi_label','bsi_code'].forEach(k => localStorage.removeItem(k));
    history.replaceState({}, '', location.pathname);
    setTimeout(() => toast('Logout berhasil', 'success'), 100);
    return;
  }
  // Auto-redirect kalau sudah login (tidak clear)
  const auth = localStorage.getItem('bsi_auth');
  const role = localStorage.getItem('bsi_role');
  const code = localStorage.getItem('bsi_code');
  if (auth && role && code && ACCESS_MAP[code]) {
    setTimeout(() => { window.location.href = ACCESS_MAP[code].page; }, 350);
  }
})();

// Firebase init (untuk health check)
try { firebase.initializeApp(FIREBASE_CONFIG); } catch(e) { console.warn('Firebase init:', e.message); }

const $ = s => document.querySelector(s);
const codeInput = $('#code');
const eyeBtn = $('#eyeBtn');
const eyeOn = $('#eyeOn');
const eyeOff = $('#eyeOff');
const badge = $('#badge');
const badgeText = $('#badgeText');
const badgeGroup = $('#badgeGroup');
const submitBtn = $('#submitBtn');
const errBox = $('#err');

let visible = false;

eyeBtn.addEventListener('click', () => {
  visible = !visible;
  codeInput.type = visible ? 'text' : 'password';
  eyeOn.style.display  = visible ? 'block' : 'none';
  eyeOff.style.display = visible ? 'none'  : 'block';
});

codeInput.addEventListener('input', e => {
  const v = e.target.value.toUpperCase().replace(/\\s/g, '');
  e.target.value = v;
  errBox.classList.remove('on');
  const map = ACCESS_MAP[v];
  if (map) {
    badgeText.textContent = map.label;
    badgeGroup.textContent = map.gname || '';
    badge.classList.add('on');
    codeInput.classList.add('ok');
    submitBtn.disabled = false;
  } else {
    badge.classList.remove('on');
    codeInput.classList.remove('ok');
    submitBtn.disabled = true;
  }
});

codeInput.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !submitBtn.disabled) doSubmit();
});

submitBtn.addEventListener('click', doSubmit);

function doSubmit() {
  const code = codeInput.value.trim().toUpperCase();
  const map = ACCESS_MAP[code];
  if (!map) {
    errBox.textContent = 'Kode akses tidak dikenali';
    errBox.classList.add('on');
    return;
  }
  submitBtn.classList.add('ld');
  submitBtn.disabled = true;

  // Simpan auth ke localStorage
  localStorage.setItem('bsi_auth', '1');
  localStorage.setItem('bsi_role', map.role);
  localStorage.setItem('bsi_code', code);
  localStorage.setItem('bsi_label', map.label);
  if (map.group) {
    localStorage.setItem('bsi_group', map.group.toString());
    localStorage.setItem('bsi_gname', map.gname);
  }

  setTimeout(() => { window.location.href = map.page; }, 600);
}

// Auto-focus
setTimeout(() => codeInput.focus(), 250);
"""

HTML = html_head('Login') + f"""
<style>{CSS}</style>
</head>
<body>
<div class="page">
  <div class="card">
    {LOGO_ROW_HTML}
    <div class="chip">BSI Next BM School 2026</div>
    <h1>Branch Banking<br>Simulation</h1>
    <p class="sub">Sistem Penilaian Real-Time</p>
    <div class="accent-line"></div>

    <label class="lbl" for="code">Kode Akses</label>
    <div class="iw">
      <input id="code" type="password" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="Masukkan kode akses" maxlength="20">
      <button class="eye" id="eyeBtn" type="button" aria-label="Tampilkan kode">
        <svg id="eyeOn" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        <svg id="eyeOff" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
      </button>
    </div>

    <div class="badge" id="badge">
      <span class="dot"></span>
      <span class="bt" id="badgeText">Role akan tampil di sini</span>
      <span class="bg" id="badgeGroup"></span>
    </div>

    <button class="btn btn-block btn-lg" id="submitBtn" disabled>
      <span class="bl">Masuk Sistem</span>
      <span class="spin"></span>
    </button>

    <div class="err" id="err">&nbsp;</div>

    <div class="foot">
      {FOOTER_TEXT}<br>
      <small style="opacity:.65">Hubungi Class Leader bila kode tidak dikenali</small>
    </div>
  </div>
</div>

<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'index.html: {len(HTML)} bytes, {HTML.count(chr(10))+1} lines')
