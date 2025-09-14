@echo off
setlocal enabledelayedexpansion

:: ================================
:: Konfigurasi
:: ================================
set "FFMPEG_PATH=E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\ffmpeg.exe"
set "VIDEO_DEVICE=Integrated Camera"
set "AUDIO_DEVICE=Microphone Array (Realtek High Definition Audio(SST))"
set "SEGMENT_DURATION=2700"  :: 45 menit
set "RECORD_DIR=E:\MASTER\ffmpeg-2025-03-31-git-35c091f4b7-full_build\bin\record"
set "CRF=18"
set "PRESET=slow"
set "RESOLUTION=1280x720"
set "FRAMERATE=30"
set "RECONNECT_DELAY=5"

:: ================================
:: Persiapan
:: ================================
if not exist "%RECORD_DIR%" mkdir "%RECORD_DIR%"

:rekam_loop
:: Folder per tanggal
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set today=%%i
set "outdir=%RECORD_DIR%\%today%"
if not exist "%outdir%" mkdir "%outdir%"
set "logfile=%outdir%\rekam_%today%.log"

echo [%date% %time%] Mulai rekam webcam: %VIDEO_DEVICE% + mic: %AUDIO_DEVICE% >> "%logfile%"
echo Mulai rekam webcam: %VIDEO_DEVICE% + mic: %AUDIO_DEVICE%

:ffmpeg_try
"%FFMPEG_PATH%" -f dshow -rtbufsize 512M -video_size %RESOLUTION% -framerate %FRAMERATE% -pixel_format yuyv422 -i video="%VIDEO_DEVICE%" ^
 -f dshow -rtbufsize 512M -i audio="%AUDIO_DEVICE%" -ac 2 -ar 44100 -af "highpass=f=200, lowpass=f=3000" ^
 -vcodec libx264 -crf %CRF% -preset %PRESET% -vf "unsharp=5:5:0.8:3:3:0.4" -acodec aac -b:a 192k ^
 -f segment -segment_time %SEGMENT_DURATION% -reset_timestamps 1 -strftime 1 "%outdir%\journey_%today%_%%H-%%M-%%S.mp4" >> "%logfile%" 2>&1

if errorlevel 1 (
    echo [%date% %time%] ERROR: FFmpeg gagal, tunggu %RECONNECT_DELAY% detik sebelum coba ulang... >> "%logfile%"
    timeout /t %RECONNECT_DELAY% /nobreak >nul
    goto ffmpeg_try
)

echo [%date% %time%] Segmen selesai, cek folder %outdir% >> "%logfile%"
goto rekam_loop
