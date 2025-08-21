import os
import sys
import threading
import socketio
from colorama import init, Style

# Keep truecolor sequences intact
init(autoreset=True, convert=False, strip=False, wrap=True)

sio = socketio.Client()

name = input("Enter your name: ").strip()
color = input("Enter a hex color code for your name (e.g. #FF5733): ").strip()


def normalize_hex(hx: str) -> str:
    hx = (hx or "").strip()
    if not hx:
        return "#FFFFFF"
    if not hx.startswith("#"):
        hx = "#" + hx
    if len(hx) == 4:  # #RGB -> #RRGGBB
        hx = "#" + "".join(ch * 2 for ch in hx[1:])
    if len(hx) != 7:
        return "#FFFFFF"
    try:
        int(hx[1:], 16)
    except ValueError:
        return "#FFFFFF"
    return hx.upper()


def supports_truecolor() -> bool:
    ct = os.environ.get("COLORTERM", "").lower()
    term = os.environ.get("TERM", "").lower()
    return (
        "truecolor" in ct
        or "24bit" in ct
        or "xterm-kitty" in term
        or "wezterm" in term
        or "vscode" in term
        or "windows-terminal" in term
    )


TRUECOLOR = supports_truecolor()
color = normalize_hex(color)


def hex_to_ansi(hx: str) -> str:
    hx = normalize_hex(hx)
    r = int(hx[1:3], 16)
    g = int(hx[3:5], 16)
    b = int(hx[5:7], 16)
    if TRUECOLOR:
        return f"\033[38;2;{r};{g};{b}m"
    # Fallback approximation
    comps = [(r, "r"), (g, "g"), (b, "b")]
    dom = max(comps)[1]
    if dom == "r" and g > 200 and b < 80:
        code = 33
    elif dom == "r":
        code = 31
    elif dom == "g":
        code = 32
    elif dom == "b":
        code = 34
    else:
        code = 37
    return f"\033[{code}m"


def clear_line() -> None:
    # Return to start of line and clear it
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()


@sio.event
def connect():
    print("Connected to server!")
    # No prompt shown


@sio.event
def message(data):
    # Render only the broadcast (including our own)
    user_name = data.get("name", "Unknown")
    user_color = hex_to_ansi(data.get("color", "#FFFFFF"))
    text = data.get("text", "")

    clear_line()
    sys.stdout.write(f"{user_color}{user_name}{Style.RESET_ALL}: {text}\n")
    sys.stdout.flush()


def input_thread():
    # No prompt; user types on a blank line
    while True:
        line = input()
        msg = line.strip()
        if not msg:
            continue
        # Send only; do NOT print locally. Wait for broadcast to show final colored line.
        sio.send({"name": name, "color": color, "text": msg})


sio.connect("http://127.0.0.1:5000")
threading.Thread(target=input_thread, daemon=True).start()
sio.wait()
