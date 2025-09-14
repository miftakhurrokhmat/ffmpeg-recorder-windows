import os
import subprocess
import datetime
import time

# ===========================
# Konfigurasi
# ===========================
FFMPEG_PATH = r"E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\ffmpeg.exe"
VIDEO_DEVICE = "Integrated Camera"
AUDIO_DEVICE = "Microphone Array (Realtek High Definition Audio(SST))"
SEGMENT_DURATION = 2700  # 45 menit
RECORD_DIR = r"E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\record"
RECONNECT_DELAY = 5  # detik tunggu sebelum coba ulang

CRF = 18
PRESET = "slow"
RESOLUTION = "1280x720"
FRAMERATE = 30

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
# Main Loop
# ===========================
while True:
    folder = today_folder()
    logfile = os.path.join(folder, f"rekam_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
    output_pattern = os.path.join(folder, "journey_%Y-%m-%d_%H-%M-%S.mp4")

    log(f"[{datetime.datetime.now()}] Mulai rekam webcam {VIDEO_DEVICE} + mic {AUDIO_DEVICE}", logfile)

    while True:
        try:
            # Jalankan ffmpeg langsung segment MP4
            subprocess.run([
                FFMPEG_PATH,
                "-f", "dshow",
                "-rtbufsize", "512M",
                "-video_size", RESOLUTION,
                "-framerate", str(FRAMERATE),
                "-pixel_format", "yuyv422",
                "-i", f"video={VIDEO_DEVICE}",
                "-f", "dshow",
                "-rtbufsize", "512M",
                "-i", f"audio={AUDIO_DEVICE}",
                "-ac", "2",
                "-ar", "44100",
                "-af", "highpass=f=200, lowpass=f=3000",
                "-vcodec", "libx264",
                "-crf", str(CRF),
                "-preset", PRESET,
                "-vf", "unsharp=5:5:0.8:3:3:0.4",
                "-acodec", "aac",
                "-b:a", "192k",
                "-f", "segment",
                "-segment_time", str(SEGMENT_DURATION),
                "-reset_timestamps", "1",
                "-strftime", "1",
                output_pattern
            ], capture_output=False, text=True)
            break  # selesai normal, keluar loop ffmpeg_try
        except Exception as e:
            log(f"[{datetime.datetime.now()}] ERROR: {e}, tunggu {RECONNECT_DELAY} detik sebelum coba ulang...", logfile)
            time.sleep(RECONNECT_DELAY)

    log(f"[{datetime.datetime.now()}] Segmen selesai, cek folder {folder}", logfile)
    # Loop ulang otomatis → rekam nonstop
