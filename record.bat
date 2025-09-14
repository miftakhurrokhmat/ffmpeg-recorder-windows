@echo off
setlocal enabledelayedexpansion

:: ================================
:: Konfigurasi
:: ================================
set "FFMPEG_PATH=E:\MASTER\ffmpeg-master-latest-win64-lgpl\bin\ffmpeg.exe"
set "RTSP_URL=rtsp://192.168.0.103:554/live/0/MAIN"
set "SEGMENT_DURATION=2700"   :: 45 menit
set "RECORD_DIR=E:\MASTER\ffmpeg-master-latest-win64-lgpl\bin\record"
set "RECONNECT_DELAY=5"       :: detik tunggu kalau gagal

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

echo [%date% %time%] Mulai rekam RTSP segment %SEGMENT_DURATION% detik... >> "%logfile%"
echo Mulai rekam RTSP segment %SEGMENT_DURATION% detik...

:ffmpeg_try
"%FFMPEG_PATH%" -rtsp_transport tcp -i "%RTSP_URL%" -max_delay 1000000 ^
 -c:v copy -c:a aac -b:a 128k ^
 -f segment -segment_time %SEGMENT_DURATION% -reset_timestamps 1 -strftime 1 "%outdir%\output_%%Y-%%m-%%d_%%H-%%M-%%S.mp4" >> "%logfile%" 2>&1

if errorlevel 1 (
    echo [%date% %time%] ERROR: Rekaman gagal, tunggu %RECONNECT_DELAY% detik... >> "%logfile%"
    timeout /t %RECONNECT_DELAY% /nobreak >nul
    goto ffmpeg_try
)

echo [%date% %time%] Segmen selesai, cek folder %outdir% >> "%logfile%"
goto rekam_loop
