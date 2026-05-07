# Asset Files Required

Letakkan file berikut di folder ini sebelum deploy:

## danantara.png
- Logo Danantara
- Format: PNG dengan background transparan
- Ukuran display: ~26-28px tinggi
- Aspect ratio: bebas (auto width)

## bsi.png  
- Logo Bank Syariah Indonesia
- Format: PNG dengan background transparan
- Ukuran display: ~30-32px tinggi (sedikit lebih besar dari Danantara)
- Aspect ratio: bebas (auto width)

## bg-report-cpi.jpg
- Background gradient teal-gold dengan Islamic geometric pattern
- Format: JPG (file size dikompres untuk web)
- Ukuran: minimal 1600×2400px (A4 portrait equivalent)
- Akan ditampilkan dengan opacity 10% di belakang Report Individual
- Akan dicetak ke PDF jika user mengaktifkan Background Graphics di dialog Print

## Fallback

Jika file logo tidak ada, sistem akan menyembunyikan elemen logo otomatis (via onerror).
Jika bg-report-cpi.jpg tidak ada, fallback gradient CSS akan dipakai.

Sistem tetap berjalan tanpa asset ini, tapi report PDF akan kurang professional.
