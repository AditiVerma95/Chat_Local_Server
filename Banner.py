import shutil
from colorama import init, Style

init(autoreset=True)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"

def print_custom_banner(name, symbol="*", border_char="=", align="center", hex_color="#00FF00"):
    columns = shutil.get_terminal_size((80, 20)).columns
    border_line = border_char * columns
    color_code = hex_to_rgb(hex_color)

    if align == "left":
        name_line = f"{symbol} {name}"
    elif align == "right":
        name_line = f"{name} {symbol}".rjust(columns)
    else:
        name_line = f"{symbol} {name} {symbol}".center(columns)
    
    print(border_line)
    print(color_code + Style.BRIGHT + name_line + Style.RESET_ALL)
    print(border_line)
