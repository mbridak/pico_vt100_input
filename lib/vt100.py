"""
Example collection of vt100 terminal convenience functions.
"""

# Who's to blame: Michael Bridak
# Where to complain: Michael.Bridak@gmail.com or @k6gte@mastodon.radio


import usb_cdc

serial = usb_cdc.console

KEY_LEFT = b"\x1b[D"
KEY_RIGHT = b"\x1b[C"
KEY_UP = b"\x1b[A"
KEY_DOWN = b"\x1b[B"
KEY_BACKSPACE = b"\x7f"
KEY_DC = b"\x1b[3~"
KEY_INSERT = b"\x1b[2~"
KEY_HOME = b"\x1b[1~"
KEY_END = b"\x1b[4~"
KEY_PGUP = b"\x1b[5~"
KEY_PGDOWN = b"\x1b[6~"
KEY_TAB = b"\t"
KEY_SHIFT_TAB = b"\x1b[Z"
KEY_ESCAPE = b"\x1b"
KEY_ENTER = b"\r"


def sg0():
    out("\033(0")


def ug0():
    out("\033(B")


def cls():
    out("\033[2J")


def save_screen():
    out("\033[?47h")


def restore_screen():
    out("\033[?47l")


def home():
    out("\033[H")


def set132cols():
    out("\033[?3h")


def set80cols():
    out("\033[?3l")


def cursor_down():
    out("\033D")


def cursor_up():
    out("\033M")


def cursor_forward(spaces=1):
    distance = rjust(str(spaces), 3, "0")
    out(f"\033[{distance}C")


def cursor_back(spaces=1):
    distance = rjust(str(spaces), 3, "0")
    out(f"\033[{distance}D")


def next_line():
    out("\033E")


def save_cursor():
    out("\0337")


def restore_cursor():
    out("\0338")


def reverse_screen():
    out("\033[?5h")


def normal_screen():
    out("\033[?5l")


def lock_keyboard():
    out("\033[2h")


def unlock_keyboard():
    out("\033[2l")


def echo_on():
    out("\033[12h")


def echo_off():
    out("\033[12l")


def cursor_off():
    out("\033[?25l")


def cursor_on():
    out("\033[?25h")


def g1_special():
    out("\033)0")


def attr_off():
    out("\033[m")


def attr_bold():
    out("\033[1m")


def attr_dim():
    out("\033[2m")


def attr_dim_off():
    out("\033[22m")


def attr_underline():
    out("\033[4m")


def attr_underline_off():
    out("\033[24m")


def attr_blink():
    out("\033[5m")


def attr_blink_off():
    out("\033[25m")


def attr_reverse():
    out("\033[7m")


def attr_reverse_off():
    out("\033[27m")


def color(colour: str) -> None:
    """
    FG: 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white 39=default
    BG: 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white 49=default
    """
    out(f"\033[{colour}m")


def set_htab():
    out("\033H")


def clear_htab():
    out("\033[g")


def clear_all_htab():
    out("\033[3g")


def double_height_top():
    out("\033#3")


def double_height_bottom():
    out("\033#4")


def single_width_line():
    out("\033#5")


def double_width_line():
    out("\033#6")


def erase_after_cursor():
    out("\033[K")


def erase_before_cursor():
    out("\033[1K")


def erase_line():
    print("\033[2K")


def erase_screen_after_cursor():
    out("\033[J")


def erase_screen_upto_cursor():
    out("\033[1J")


def smooth_scroll():
    out("\033[?4h")


def jump_scroll():
    out("\033[?4l")


def scroll_origin():
    out("\033[?6h")


def screen_origin():
    out("\033[?6l")


def scroll_region(top: str, bottom: str):
    out(f"\033[{top};{bottom}r")


def addstr(y=-1, x=-1, text="", attribute=""):
    if x != -1 or y != -1:
        move(y, x)
    if attribute:
        color(attribute)
    out(text)
    if attribute:
        attr_off()


def move(y, x):
    row = rjust(str(y), 3, "0")
    col = rjust(str(x), 3, "0")
    out(f"\033[{row};{col}H")


def hline(length=1):
    sg0()
    for _ in range(0, length):
        out("q")
    ug0()


def mvhline(y, x, length):
    move(y, x)
    hline(length)


def vline(length=1):
    sg0()
    for _ in range(0, length):
        out("x")
        cursor_down()
        cursor_back()
    ug0()


def mvvline(y, x, length):
    move(y, x)
    sg0()
    for pos in range(0, length):
        move(y + pos, x)
        out("x")
    ug0()


def title(y, x, w, title_text):
    position = int((w / 2) - (len(title_text) / 2))
    move(y, x + position)
    ug0()
    out(title_text)


def title2(y, x, w, title_text):
    position = int((w / 2) - (len(title_text) / 2))
    move(y, x + position - 1)
    sg0()
    out("u")
    ug0()
    out(title_text)
    sg0()
    out("t")
    ug0()


def box(y, x, h, w, title_text=""):
    move(y, x)
    sg0()
    out("l")
    hline(w - 2)
    sg0()
    out("k")
    if title_text:
        title(y, x, w, title_text)
    mvvline(y + 1, x, h - 2)
    mvvline(y + 1, x + (w - 1), h - 2)
    move(y + h - 1, x)
    sg0()
    out("m")
    hline(w - 2)
    sg0()
    out("j")
    ug0()


def autowrapon():
    out("\033[?7h")


def autowrapoff():
    out("\033[?7l")


def rjust(text, count, filler):
    needed = count - len(text)
    return (filler * needed) + text


def ljust(text, count, filler):
    needed = count - len(text)
    return text + (filler * needed)


def out(data):
    usb_cdc.console.write(data.encode())


def getch():
    count = usb_cdc.console.in_waiting
    if count:
        character = usb_cdc.console.read(count)
        return character
    else:
        return -1
