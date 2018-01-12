#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
pushd "$DIR/web"
python3 -m http.server --cgi 80
