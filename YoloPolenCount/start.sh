#!/usr/bin/env bash
# gunicorn server:server --bind 0.0.0.0:8530 --timeout 0

waitress-serve --listen=0.0.0.0:8530 server:server