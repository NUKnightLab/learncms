#!/bin/bash
command -v vulcanize >/dev/null 2>&1 || { echo >&2 "'vulcanize' not found. Install it with 'npm install -g vulcanize'"; exit 1; }
vulcanize --inline-css --inline-scripts components/elements/elements.html > static/webcomponents/webcomponents.html
cp -r components/elements/learn/styles static/webcomponents/
cp -r components/elements/learn/images static/webcomponents/
