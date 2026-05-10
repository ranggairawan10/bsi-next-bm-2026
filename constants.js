/**
 * BSI Next BM School · Scoring System v2
 * Shared Constants & Formula Library
 */

// ─── GROUPS ────────────────────────────────────────────────────────────────
const GROUPS = {
  borobudur:  { id: 'borobudur',  name: 'Borobudur',   index: 0, color: '#00A39D', textColor: '#fff' },
  prambanan:  { id: 'prambanan',  name: 'Prambanan',   index: 1, color: '#F8AD3C', textColor: '#1a2332' },
  diponegoro: { id: 'diponegoro', name: 'Diponegoro',  index: 2, color: '#3B82F6', textColor: '#fff' },
  gajahmada:  { id: 'gajahmada',  name: 'Gajah Mada',  index: 3, color: '#10B981', textColor: '#fff' },
  majapahit:  { id: 'majapahit',  name: 'Majapahit',   index: 4, color: '#8B5CF6', textColor: '#fff' }
};
const GROUP_IDS = Object.keys(GROUPS);

// ─── ROUNDS ────────────────────────────────────────────────────────────────
const ROUNDS = {
  r1: { id:'r1', number:1, title:'Selisih Kas Pak Bagus', category:'Operasional', maxAmanah:50 },
  r2: { id:'r2', number:2, title:'Pondok 4M',             category:'Pembiayaan',  maxAmanah:65 },
  r3: { id:'r3', number:3, title:'Restruktur Konflik',    category:'Leadership',  maxAmanah:80 },
  r4: { id:'r4', number:4, title:'Crisis Compliance',     category:'Capstone',    maxAmanah:100 }
};
const ROUND_IDS = ['r1','r2','r3','r4'];

// ─── ACCESS CODES ──────────────────────────────────────────────────────────
const ACCESS_CODES = {
  'BSI2026ADMIN':  { page:'admin.html',       role:'admin',     group:null },
  'BSI2026GM':     { page:'gamemaster.html',  role:'gm',        group:null },
  'BSI2026LAYAR':  { page:'projector.html',   role:'projector', group:null },
  'BSI2026BOARD':  { page:'board.html',       role:'board',     group:null },
  'BSI2026REPORT': { page:'report.html',      role:'report',    group:null },
  'COACH2026G1':   { page:'coach.html',       role:'coach',     group:'borobudur'  },
  'COACH2026G2':   { page:'coach.html',       role:'coach',     group:'prambanan'  },
  'COACH2026G3':   { page:'coach.html',       role:'coach',     group:'diponegoro' },
  'COACH2026G4':   { page:'coach.html',       role:'coach',     group:'gajahmada'  },
  'COACH2026G5':   { page:'coach.html',       role:'coach',     group:'majapahit'  },
  'LEADER2026G1':  { page:'leader.html',      role:'leader',    group:'borobudur'  },
  'LEADER2026G2':  { page:'leader.html',      role:'leader',    group:'prambanan'  },
  'LEADER2026G3':  { page:'leader.html',      role:'leader',    group:'diponegoro' },
  'LEADER2026G4':  { page:'leader.html',      role:'leader',    group:'gajahmada'  },
  'LEADER2026G5':  { page:'leader.html',      role:'leader',    group:'majapahit'  }
};

// ─── BPM WEIGHTS ───────────────────────────────────────────────────────────
const BPM_WEIGHTS = { cm: 0.40, risk: 0.25, people: 0.20, cs: 0.15 };
const BPM_LABELS  = {
  cm:     { label:'Contribution Margin',  shortLabel:'CM',     hat:'Business Leader' },
  risk:   { label:'Risk',                 shortLabel:'Risk',   hat:'Risk Leader' },
  people: { label:'People',               shortLabel:'People', hat:'People Leader' },
  cs:     { label:'Customer Satisfaction',shortLabel:'CS',     hat:'People Leader' }
};

// ─── 6D BEHAVIOR WEIGHTS ───────────────────────────────────────────────────
const BEHAVIOR_6D = {
  qoa: { label:'Quality of Argument',    weight: 0.25 },
  al:  { label:'Adaptive Leadership',    weight: 0.15 },
  sa:  { label:'Situational Awareness',  weight: 0.15 },
  rc:  { label:'Risk Consciousness',     weight: 0.15 },
  ej:  { label:'Ethical Judgment',       weight: 0.15 },
  pi:  { label:'People Influence',       weight: 0.15 }
};
const BEHAVIOR_KEYS = Object.keys(BEHAVIOR_6D);

// ─── FORMULA LIBRARY ───────────────────────────────────────────────────────

/**
 * Compute BPM combined (avg GM + Leader) per indicator
 */
function computeBPMCombined(gmBPM, leaderBPM) {
  const combined = {};
  ['cm','risk','people','cs'].forEach(k => {
    const gv = gmBPM     ? (parseFloat(gmBPM[k])     || 0) : 0;
    const lv = leaderBPM ? (parseFloat(leaderBPM[k]) || 0) : 0;
    combined[k] = leaderBPM ? (gv + lv) / 2 : gv;
  });
  return combined;
}

/**
 * Compute BPM weighted aggregate (-10 to +10)
 */
function computeBPMAggregate(bpmCombined) {
  return (
    (bpmCombined.cm     || 0) * BPM_WEIGHTS.cm     +
    (bpmCombined.risk   || 0) * BPM_WEIGHTS.risk   +
    (bpmCombined.people || 0) * BPM_WEIGHTS.people +
    (bpmCombined.cs     || 0) * BPM_WEIGHTS.cs
  );
}

/**
 * Normalize BPM aggregate (-10..+10) → 0..100
 */
function normalizeBPM(bpmAggregate) {
  return (bpmAggregate + 10) / 20 * 100;
}

/**
 * Compute 6D weighted score for one member (0-100)
 * input: { qoa, al, sa, rc, ej, pi } all 1-10
 */
function computeScore6D(behavior) {
  let total = 0;
  BEHAVIOR_KEYS.forEach(k => {
    total += (parseFloat(behavior[k]) || 1) * BEHAVIOR_6D[k].weight;
  });
  return total * 10; // scale 1-10 → 10-100
}

/**
 * Compute L3 per member per round (0-100)
 */
function computeL3(bpmNormalized, score6D) {
  return (bpmNormalized * 0.30) + (score6D * 0.70);
}

/**
 * Convert score (0-100) to grade index (1-4)
 */
function scoreToIndeks(score) {
  if (score >= 90) return 4;
  if (score >= 80) return 3;
  if (score >= 70) return 2;
  return 1;
}

/**
 * Compute CPI
 */
function computeCPI(indeksPost, indeksSim) {
  return (indeksPost * 2 + indeksSim * 16) / 18;
}

/**
 * Indeks → grade label
 */
function indeksToGrade(indeks) {
  return ['','D','C','B','A'][indeks] || 'D';
}

/**
 * Score (0-100) → grade label
 */
function scoreToGrade(score) {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  return 'D';
}

/**
 * Compute full scores for one group-round document
 */
function computeFullScores(scoreDoc) {
  const result = {};

  // BPM Combined
  const combined = computeBPMCombined(scoreDoc.gm_bpm, scoreDoc.leader_bpm);
  result.bpm_combined = combined;

  // BPM Aggregate + Normalized
  const agg = computeBPMAggregate(combined);
  result.bpm_aggregate  = Math.round(agg * 100) / 100;
  result.bpm_normalized = Math.round(normalizeBPM(agg) * 100) / 100;

  // Per-member 6D + L3
  const avg6D = {};
  const l3PerMember = {};
  if (scoreDoc.coach_behavior) {
    Object.keys(scoreDoc.coach_behavior).forEach(mKey => {
      const b = scoreDoc.coach_behavior[mKey];
      const s6d = computeScore6D(b);
      const l3  = computeL3(result.bpm_normalized, s6d);
      avg6D[mKey]       = Math.round(s6d * 100) / 100;
      l3PerMember[mKey] = Math.round(l3  * 100) / 100;
    });
  }
  result.avg_6d        = avg6D;
  result.l3_per_member = l3PerMember;

  // Group avg L3 (for leaderboard)
  const l3Vals = Object.values(l3PerMember);
  result.l3_group_avg = l3Vals.length
    ? Math.round((l3Vals.reduce((a,b)=>a+b,0) / l3Vals.length) * 100) / 100
    : 0;

  return result;
}

/**
 * Compute group leaderboard scores across all groups
 * Input: array of scoreDoc objects (same round)
 * Adds .group_score (0-100) to each
 */
function computeGroupScores(scoreDocs) {
  const deltaCMs = scoreDocs.map(d => d.gm_deltaCM || 0);
  const maxAbs   = Math.max(...deltaCMs.map(Math.abs), 1); // avoid div/0

  return scoreDocs.map(d => {
    const normDelta   = ((d.gm_deltaCM || 0) / maxAbs) * 100;
    const bpmNorm     = d.bpm_normalized || 50;
    const groupScore  = 0.70 * normDelta + 0.30 * bpmNorm;
    return { ...d, group_score: Math.round(groupScore * 100) / 100 };
  });
}

// ─── SESSION STORAGE HELPERS ───────────────────────────────────────────────
function saveSession(role, group, code) {
  sessionStorage.setItem('bsi_role',  role);
  sessionStorage.setItem('bsi_group', group || '');
  sessionStorage.setItem('bsi_code',  code);
  sessionStorage.setItem('bsi_login', Date.now());
}

function getSession() {
  return {
    role:  sessionStorage.getItem('bsi_role'),
    group: sessionStorage.getItem('bsi_group'),
    code:  sessionStorage.getItem('bsi_code'),
    login: sessionStorage.getItem('bsi_login')
  };
}

function requireSession(expectedRole) {
  const sess = getSession();
  if (!sess.role) { window.location.href = '/index.html'; return null; }
  if (expectedRole && sess.role !== expectedRole) { window.location.href = '/index.html'; return null; }
  return sess;
}

// ─── FIRESTORE SCORE DOCUMENT ID ───────────────────────────────────────────
function scoreDocId(groupId, roundId) {
  return `${groupId}_${roundId}`;
}

// ─── NUMBER FORMATTING ─────────────────────────────────────────────────────
function fmtRupiah(juta) {
  if (juta === null || juta === undefined) return '—';
  const sign = juta >= 0 ? '+' : '';
  return `${sign}${juta.toLocaleString('id-ID')} Jt`;
}

function fmtBPM(val) {
  const sign = val > 0 ? '+' : '';
  return `${sign}${val.toFixed(1)}`;
}

console.log("[Constants] Loaded · Groups:", GROUP_IDS.length, "· Rounds:", ROUND_IDS.length);
