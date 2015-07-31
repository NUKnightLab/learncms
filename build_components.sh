#!/bin/bash
command -v vulcanize >/dev/null 2>&1 || { echo >&2 "'vulcanize' not found. Install it with 'npm install -g vulcanize'"; exit 1; }
vulcanize components/elements/elements.html > static/webcomponents.html
