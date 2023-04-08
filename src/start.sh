#!/bin/bash

echo "Deletion of old logs"
find /src/log/ -regex '\(.*json\|.*log\)' -type f -mtime +15 -delete

echo "Starting process..."
gunicorn -w 1 app:app -b 0.0.0.0:5000 --timeout 30
