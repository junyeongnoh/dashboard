#!/bin/bash
cd ~/Desktop/dashboard
python3 updated_dashboard.py
git add .
git commit -m "auto update \$(date '+%Y-%m-%d')"
git push origin main
