# FFmpeg Recorder for Windows

Repository ini berisi skrip untuk **merekam video dari webcam dan CCTV (RTSP)** menggunakan FFmpeg di **Windows 11**.  
Setiap skrip menggunakan build FFmpeg yang sesuai dengan jenis perangkat.

---

## 📁 Struktur Repository

```
/bin
├─ record_cam.bat        # Skrip batch untuk merekam webcam
├─ record_cam.py         # Skrip Python untuk merekam webcam
├─ record.bat            # Skrip batch untuk merekam RTSP (CCTV)
├─ record.py             # Skrip Python untuk merekam RTSP (CCTV)
``

---

## ⚙️ Persiapan FFmpeg

1. Download FFmpeg build Windows sesuai kebutuhan:
   - **Webcam (local recording)**: full build (misal: `ffmpeg-2025-03-31-git-35c091f4b7-full_build.zip`)  
   - **CCTV (RTSP recording)**: LGPL Win64 Latest (misal: `ffmpeg-master-latest-win64-lgpl.zip`)

2. Extract ke folder pilihan, contoh:
```
E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin
E:\MASTER\ffmpeg-master-latest-win64-lgpl\bin
```

3. Sesuaikan path FFmpeg di skrip:
```bat
set "FFMPEG_PATH=E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\ffmpeg.exe"
```
atau di Python:
```python
FFMPEG_PATH = r"E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\ffmpeg.exe"
```

---

## 💻 Cara Menggunakan

### 1. Webcam Recording

#### Batch
```bat
record_cam.bat
```

#### Python
```bash
python record_cam.py
```

- File video disimpan di folder `record/YYYY-MM-DD/`.  
- Segmen 45 menit, log aktivitas di `rekam_YYYY-MM-DD.log`.

---

### 2. CCTV (RTSP) Recording

#### Batch
```bat
record.bat
```

#### Python
```bash
python record.py
```

- Sesuaikan RTSP URL:
```bat
set "RTSP_URL=rtsp://192.168.0.103:554/live/0/MAIN"
```
atau di Python:
```python
RTSP_URL = "rtsp://192.168.0.103:554/live/0/MAIN"
```
- File video disimpan di folder `record/YYYY-MM-DD/` dengan segmen 45 menit.  
- Otomatis reconnect jika FFmpeg gagal.  
- Log aktivitas di `rekam_YYYY-MM-DD.log`.

---

## 📌 Tips

- Pastikan kamera / RTSP online sebelum menjalankan skrip.  
- Jangan jalankan dua skrip dengan FFmpeg build yang sama bersamaan.  
- Untuk skrip Python, pastikan **Python 3.x** terinstall dan di PATH.  

---

## 📜 Lisensi

Open-source, bebas digunakan dan dimodifikasi untuk penggunaan pribadi atau belajar.
