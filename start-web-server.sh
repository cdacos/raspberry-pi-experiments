#!/bin/bash
pushd web
python3 -m http.server --cgi 8000
