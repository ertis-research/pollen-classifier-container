#!/usr/bin/env bash

# gunicorn server:server --bind 0.0.0.0:8530 --timeout 0 --log-level info
uvicorn server:server --host 0.0.0.0 --port 8530 --timeout-keep-alive 0 --log-level debug --use-colors