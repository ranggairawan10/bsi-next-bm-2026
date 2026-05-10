/**
 * BSI Next BM School · Scoring System v2
 * Firebase Configuration
 * 
 * GANTI NILAI DI BAWAH DENGAN CONFIG FIREBASE ANDA:
 * Firebase Console → Project Settings → Your apps → SDK setup and config
 */

const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyBwc9qm9tuoBK7ba2E7k8IY3bjlXTNRoUc",
  authDomain:        "bsi-next-bm-2026.firebaseapp.com",
  projectId:         "bsi-next-bm-2026",
  storageBucket:     "bsi-next-bm-2026.firebasestorage.app",
  messagingSenderId: "685360057111",
  appId:             "1:685360057111:web:3f2c3fe05b5054727e0552"
};

// Guard: pastikan hanya satu instance
if (!firebase.apps || firebase.apps.length === 0) {
  firebase.initializeApp(FIREBASE_CONFIG);
  console.log("[Firebase] Initialized · project:", FIREBASE_CONFIG.projectId);
} else {
  console.log("[Firebase] Already initialized");
}

// Global Firestore instance — tersedia di semua halaman setelah script ini
const db = firebase.firestore();

// NO enablePersistence() — training context butuh data live, bukan cache
console.log("[Firebase] Firestore ready");
