#!/bin/sh

DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$DIR/src" || exit 1

if command -v kitty >/dev/null 2>&1; then
    exec kitty \
        --override initial_window_width=184c \
        --override initial_window_height=24c \
        sh -c 'cd "$1" && exec python3 main.py' sh "$DIR/src"
fi

exec python3 main.py