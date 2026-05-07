"""
common.py — Shared building blocks untuk 8 file BSI Scoring System.
Semua file pakai modul ini supaya konsisten di Firebase config, CSS, helper JS.
"""

# ============================================================
# FIREBASE CONFIG (LOCKED)
# ============================================================
FIREBASE_CONFIG = """
const FIREBASE_CONFIG = {
  apiKey: "AIzaSyBwc9qm9tuoBK7ba2E7k8IY3bjlXTNRoUc",
  authDomain: "bsi-next-bm-2026.firebaseapp.com",
  databaseURL: "https://bsi-next-bm-2026-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "bsi-next-bm-2026",
  storageBucket: "bsi-next-bm-2026.firebasestorage.app",
  messagingSenderId: "685360057111",
  appId: "1:685360057111:web:3f2c3fe05b5054727e0552"
};
"""

# ============================================================
# 15 KODE AKSES (5 system + 5 coach + 5 leader)
# ============================================================
ACCESS_MAP = """
const ACCESS_MAP = {
  'BSI2026ADMIN':  { role: 'admin',     page: 'admin.html',      label: 'Master Admin' },
  'BSI2026GM':     { role: 'gm',        page: 'gamemaster.html', label: 'Game Master' },
  'BSI2026LAYAR':  { role: 'projector', page: 'projector.html',  label: 'Layar Proyektor' },
  'BSI2026BOARD':  { role: 'board',     page: 'board.html',      label: 'Visual Board' },
  'BSI2026REPORT': { role: 'report',    page: 'report.html',     label: 'Report Generator' },
  'COACH2026G1':   { role: 'coach',     page: 'coach.html',      label: 'Branch Coach Borobudur',  group: 1, gname: 'Cabang Borobudur' },
  'COACH2026G2':   { role: 'coach',     page: 'coach.html',      label: 'Branch Coach Prambanan',  group: 2, gname: 'Cabang Prambanan' },
  'COACH2026G3':   { role: 'coach',     page: 'coach.html',      label: 'Branch Coach Diponegoro', group: 3, gname: 'Cabang Diponegoro' },
  'COACH2026G4':   { role: 'coach',     page: 'coach.html',      label: 'Branch Coach Gajah Mada', group: 4, gname: 'Cabang Gajah Mada' },
  'COACH2026G5':   { role: 'coach',     page: 'coach.html',      label: 'Branch Coach Majapahit',  group: 5, gname: 'Cabang Majapahit' },
  'LEADER2026G1':  { role: 'leader',    page: 'leader.html',     label: 'Group Leader Borobudur',  group: 1, gname: 'Cabang Borobudur' },
  'LEADER2026G2':  { role: 'leader',    page: 'leader.html',     label: 'Group Leader Prambanan',  group: 2, gname: 'Cabang Prambanan' },
  'LEADER2026G3':  { role: 'leader',    page: 'leader.html',     label: 'Group Leader Diponegoro', group: 3, gname: 'Cabang Diponegoro' },
  'LEADER2026G4':  { role: 'leader',    page: 'leader.html',     label: 'Group Leader Gajah Mada', group: 4, gname: 'Cabang Gajah Mada' },
  'LEADER2026G5':  { role: 'leader',    page: 'leader.html',     label: 'Group Leader Majapahit',  group: 5, gname: 'Cabang Majapahit' }
};
"""

# ============================================================
# GROUP NAMES (5 kelompok)
# ============================================================
GROUP_NAMES = """
const GROUP_NAMES = {
  1: 'Cabang Borobudur',
  2: 'Cabang Prambanan',
  3: 'Cabang Diponegoro',
  4: 'Cabang Gajah Mada',
  5: 'Cabang Majapahit'
};
"""

# ============================================================
# AMANAH POINTS PER RONDE (LOCKED dari memory)
# ============================================================
AMANAH_PER_ROUND = """
const AMANAH_PER_ROUND = { 1: 50, 2: 65, 3: 80, 4: 100 };
const ROUND_TITLES = {
  1: 'R1 · Selisih Kas Pak Bagus (Operasional)',
  2: 'R2 · Pondok Pesantren Rp 4M (Pembiayaan)',
  3: 'R3 · Restruktur Konflik (Leadership)',
  4: 'R4 · Crisis Compliance (Capstone)'
};
"""

# ============================================================
# 6 DIMENSI BEHAVIOR (LOCKED) + WEIGHTS
# ============================================================
BEHAVIOR_DIMENSIONS = """
const BEHAVIOR_DIMENSIONS = [
  { key: 'qoa', short: 'QoA', label: 'Quality of Argument',  weight: 0.25, color: '#00A39D' },
  { key: 'al',  short: 'AL',  label: 'Active Listening',      weight: 0.15, color: '#0E8A85' },
  { key: 'sa',  short: 'SA',  label: 'Sharia Awareness',      weight: 0.15, color: '#F8AD3C' },
  { key: 'rc',  short: 'RC',  label: 'Risk Calibration',      weight: 0.15, color: '#D88A20' },
  { key: 'ej',  short: 'EJ',  label: 'Ethical Judgment',      weight: 0.15, color: '#7C5295' },
  { key: 'pi',  short: 'PI',  label: 'Practical Implementation', weight: 0.15, color: '#3B5998' }
];
"""

# ============================================================
# CSS ROOT (locked color palette)
# ============================================================
CSS_ROOT = """
:root {
  --teal: #00A39D;
  --teal-dark: #007E79;
  --teal-10: rgba(0,163,157,0.10);
  --teal-20: rgba(0,163,157,0.20);
  --gold: #F8AD3C;
  --gold-dark: #D88A20;
  --cream: #F6F3EE;
  --white: #FFFFFF;
  --text: #1A2332;
  --mid: #4A5568;
  --soft: #9AA5B4;
  --border: #E2DED8;
  --in-bg: #F9F8F5;
  --success: #2F9E66;
  --warn: #E89B2A;
  --danger: #E53E3E;
  --shadow-sm: 0 2px 4px rgba(0,0,0,.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,.08);
  --shadow-lg: 0 16px 48px rgba(0,0,0,.10);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body { min-height: 100vh; font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; background: var(--cream); color: var(--text); -webkit-font-smoothing: antialiased; }
button { font-family: inherit; }
"""

# ============================================================
# GOOGLE FONTS LINK
# ============================================================
GOOGLE_FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">"""

# ============================================================
# FIREBASE CDN SCRIPTS (compat mode untuk simplicity)
# ============================================================
FIREBASE_CDN = """<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-database-compat.js"></script>"""

# ============================================================
# AUTH GUARD (dipasang di setiap halaman role-protected)
# ============================================================
def auth_guard(required_role):
    """Generate auth guard JS untuk halaman role-specific."""
    return f"""
(function authGuard() {{
  const auth = localStorage.getItem('bsi_auth');
  const role = localStorage.getItem('bsi_role');
  if (!auth || role !== '{required_role}') {{
    window.location.replace('index.html');
  }}
}})();
"""

# ============================================================
# LOGO ROW HTML (Danantara kiri | BSI kanan)
# ============================================================
LOGO_ROW_HTML = """
<div class="logo-row">
  <img class="logo-dan" src="assets/images/danantara.png" alt="Danantara" onerror="this.style.display='none'">
  <span class="logo-div"></span>
  <img class="logo-bsi" src="assets/images/bsi.png" alt="BSI" onerror="this.style.display='none'">
</div>
"""

# ============================================================
# FIREBASE PATHS REFERENCE (semua file pakai path string yang sama)
# ============================================================
FIREBASE_PATHS = """
const PATHS = {
  bpmGM:        (r, g) => `bpm_gm/r${r}/g${g}`,
  bpmGMRound:   (r)    => `bpm_gm/r${r}`,
  bpmLeader:    (r, fromG, toG) => `bpm_leader/r${r}/from_g${fromG}/to_g${toG}`,
  bpmLeaderRoot: ()    => `bpm_leader`,
  coachData:    (g, r) => `coach_data/g${g}/r${r}`,
  coachRoot:    ()     => `coach_data`,
  amanah:       (r, g) => `amanah_coins/r${r}/g${g}`,
  amanahRoot:   ()     => `amanah_coins`,
  session:      ()     => `session`,
  sessionRound: ()     => `session/currentRound`,
  sessionLocked: ()    => `session/locked`,
  groups:       ()     => `groups`,
  groupMembers: (g)    => `groups/g${g}/members`,
  l2Scores:     ()     => `l2_scores`,
  l2Member:     (g, m) => `l2_scores/g${g}/${m}`,
  preTest:      (g, m) => `pre_test/g${g}/${m}`,
  customAmanah: (r, g) => `custom_amanah/r${r}/g${g}`
};
"""

# ============================================================
# UTILITY HELPERS (toast, format, time)
# ============================================================
UTILITY_JS = """
function toast(msg, type) {
  type = type || 'info';
  const t = document.createElement('div');
  t.className = 'toast toast-' + type;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.classList.add('on'), 10);
  setTimeout(() => {
    t.classList.remove('on');
    setTimeout(() => t.remove(), 300);
  }, 2800);
}
function fmtScore(n, decimals) {
  decimals = decimals == null ? 2 : decimals;
  if (n == null || isNaN(n)) return '0' + (decimals > 0 ? '.' + '0'.repeat(decimals) : '');
  return Number(n).toFixed(decimals);
}
function predikatFromScore(score) {
  if (score >= 90) return { code: 'A', label: 'Sangat Kompeten', idx: 4, color: '#2F9E66' };
  if (score >= 80) return { code: 'B', label: 'Kompeten',          idx: 3, color: '#00A39D' };
  if (score >= 70) return { code: 'C', label: 'Cukup Kompeten',    idx: 2, color: '#F8AD3C' };
  return                  { code: 'D', label: 'Belum Kompeten',     idx: 1, color: '#E53E3E' };
}
function escapeHTML(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
"""

# ============================================================
# TOAST CSS
# ============================================================
CSS_TOAST = """
.toast { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(20px); padding: 12px 22px; background: var(--text); color: #fff; border-radius: 10px; font-size: 13px; font-weight: 600; box-shadow: var(--shadow-lg); opacity: 0; transition: opacity .25s, transform .25s; z-index: 9999; pointer-events: none; max-width: 90%; text-align: center; }
.toast.on { opacity: 1; transform: translateX(-50%) translateY(0); }
.toast-success { background: var(--success); }
.toast-warn { background: var(--warn); }
.toast-error { background: var(--danger); }
"""

# ============================================================
# COMMON BUTTON CSS
# ============================================================
CSS_BUTTONS = """
.btn { background: var(--teal); border: none; border-radius: 10px; padding: 11px 18px; font-size: 13px; font-weight: 700; color: #fff; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 7px; box-shadow: 0 4px 14px rgba(0,163,157,.28); transition: transform .15s, box-shadow .15s, background .15s; }
.btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(0,163,157,.36); background: var(--teal-dark); }
.btn:active:not(:disabled) { transform: translateY(0); }
.btn:disabled { opacity: .35; cursor: not-allowed; }
.btn-gold { background: var(--gold); box-shadow: 0 4px 14px rgba(248,173,60,.32); }
.btn-gold:hover:not(:disabled) { background: var(--gold-dark); box-shadow: 0 8px 22px rgba(248,173,60,.42); }
.btn-ghost { background: transparent; color: var(--text); border: 1.5px solid var(--border); box-shadow: none; }
.btn-ghost:hover:not(:disabled) { background: var(--in-bg); border-color: var(--teal); color: var(--teal); }
.btn-danger { background: var(--danger); box-shadow: 0 4px 14px rgba(229,62,62,.28); }
.btn-sm { padding: 7px 12px; font-size: 12px; }
.btn-lg { padding: 14px 22px; font-size: 14px; }
.btn-block { width: 100%; }
"""

# ============================================================
# LOGO ROW CSS
# ============================================================
CSS_LOGO_ROW = """
.logo-row { display: flex; align-items: center; justify-content: center; gap: 18px; padding: 10px 18px; background: var(--cream); border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 22px; }
.logo-dan, .logo-bsi { height: 26px; width: auto; object-fit: contain; }
.logo-bsi { height: 32px; }
.logo-div { width: 1px; height: 30px; background: var(--border); }
"""

# ============================================================
# Common HTML head template
# ============================================================
def html_head(title):
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=2.0">
<meta name="theme-color" content="#00A39D">
<title>{title} · BSI Next BM School 2026</title>
{GOOGLE_FONTS}
{FIREBASE_CDN}
"""

# ============================================================
# Footer text
# ============================================================
FOOTER_TEXT = "BSI Corporate University Group · Branch Banking Simulation 2026 · HCR.ID"
