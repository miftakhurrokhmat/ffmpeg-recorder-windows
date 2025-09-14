import os
import subprocess
import datetime
import time

# ===========================
# Konfigurasi
# ===========================
FFMPEG_PATH = r"E:\MASTER\ffmpeg-master-latest-win64-lgpl\bin\ffmpeg.exe"
RTSP_URL = "rtsp://192.168.0.103:554/live/0/MAIN"
SEGMENT_DURATION = 2700   # detik (45 menit)
RECORD_DIR = r"E:\MASTER\ffmpeg-master-latest-win64-lgpl\bin\record"
RECONNECT_DELAY = 5       # detik tunggu jika gagal

# ===========================
# Helper Functions
# ===========================
def today_folder():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join(RECORD_DIR, today)
    os.makedirs(folder, exist_ok=True)
    return folder

def log(message, logfile):
    print(message)
    with open(logfile, "a") as f:
        f.write(f"{message}\n")

# ===========================
# Main Recorder Loop – nonstop
# ===========================
while True:
    folder = today_folder()
    logfile = os.path.join(folder, f"rekam_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")

    output_pattern = os.path.join(folder, "output_%Y-%m-%d_%H-%M-%S.mp4")

    log(f"[{datetime.datetime.now()}] Mulai rekam RTSP ke MP4 dengan segment {SEGMENT_DURATION}s", logfile)

    while True:
        try:
            # Jalankan ffmpeg langsung segment MP4
            subprocess.run([
                FFMPEG_PATH,
                "-rtsp_transport", "tcp",
                "-i", RTSP_URL,
                "-max_delay", "1000000",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "128k",
                "-f", "segment",
                "-segment_time", str(SEGMENT_DURATION),
                "-reset_timestamps", "1",
                "-strftime", "1",
                output_pattern
            ], capture_output=False, text=True)
            break
        except Exception as e:
            log(f"[{datetime.datetime.now()}] ERROR: {e}, tunggu {RECONNECT_DELAY}s...", logfile)
            time.sleep(RECONNECT_DELAY)

    log(f"[{datetime.datetime.now()}] Segmen selesai, cek folder: {folder}", logfile)
    # Loop ulang terus → otomatis rekam hari berikutnya juga
