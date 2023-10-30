#!/bin/bash
set -e

# Start Xvfb
rm -f /tmp/.X99-lock
Xvfb :99 -screen 0 1920x1080x16 & export DISPLAY=:99
sleep 2
x11vnc -forever -rfbport 5900 & fluxbox &

# Start FastAPI app
uvicorn main:app --host 0.0.0.0 --port 80
