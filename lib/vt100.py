"""
Example collection of vt100 terminal convenience functions.
"""

# Who's to blame: Michael Bridak
# Where to complain: Michael.Bridak@gmail.com or @k6gte@mastodon.radio

# Import circuitpython usb_cdc lib
import usb_cdc

serial = usb_cdc.console

# Key definitions sent by vt100 terminal for various key presses.
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
    """Turns on line drawing character set."""
    out("\033(0")


def ug0():
    """Turns on US character set."""
    out("\033(B")


def cls():
    """Clear the screen."""
    out("\033[2J")


def save_screen():
    """Saves screen state internally."""
    out("\033[?47h")


def restore_screen():
    """Recall previously saved screen."""
    out("\033[?47l")


def home():
    """Moves cursor to home."""
    out("\033[H")


def set132cols():
    """Set terminal columns to 132 characters wide."""
    out("\033[?3h")


def set80cols():
    """Set terminal columns to 80 characters wide."""
    out("\033[?3l")


def cursor_down(lines=1):
    """Move cursor down one line. Stops at bottom margin."""
    out(f"\033[{lines}B")


def cursor_up(lines=1):
    """Move cursor up one line. Stops at top margin."""
    out(f"\033[{lines}A")


def cursor_forward(spaces=1):
    """Moves cursor forward, stopping at screen edge."""
    out(f"\033[{spaces}C")


def cursor_back(spaces=1):
    """Moves cursor backward, stopping at screen edge."""
    out(f"\033[{spaces}D")


def next_line():
    """Move to start of next line."""
    out("\033E")


def save_cursor():
    """Save cursor position."""
    out("\0337")


def restore_cursor():
    """Move cursor back to saved position."""
    out("\0338")


def reverse_screen():
    """Reverse foreground and background."""
    out("\033[?5h")


def normal_screen():
    """UnReverse foreground and background."""
    out("\033[?5l")


def lock_keyboard():
    """Locks the keyboard."""
    out("\033[2h")


def unlock_keyboard():
    """Unlocks the keyboard."""
    out("\033[2l")


def echo_on():
    """Turns on local echo."""
    out("\033[12h")


def echo_off():
    """Turns off local echo."""
    out("\033[12l")


def cursor_off():
    """Hides the onscreen cursor."""
    out("\033[?25l")


def cursor_on():
    """Displays on screen cursor."""
    out("\033[?25h")


def g1_special():
    """May drop this..."""
    out("\033)0")


def attr_off():
    """Turn off all attributes"""
    out("\033[m")


def attr_bold():
    """Set output to bold"""
    out("\033[1m")


def attr_dim():
    """Set output to dim"""
    out("\033[2m")


def attr_dim_off():
    """Turn off dim"""
    out("\033[22m")


def attr_underline():
    """Turns on underlining."""
    out("\033[4m")


def attr_underline_off():
    """Turns off underlining."""
    out("\033[24m")


def attr_blink():
    """Turns on blinking characters."""
    out("\033[5m")


def attr_blink_off():
    """Turns off blinking characters."""
    out("\033[25m")


def attr_reverse():
    """Invert the FG and BG colors. Inverse video."""
    out("\033[7m")


def attr_reverse_off():
    """Turns off inverse video."""
    out("\033[27m")


def color(colour: str) -> None:
    """
    Should be renamed. It's more of a general attribute setter.
    Takes a semicolon separated list of attributes.
    FG: 30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white 39=default
    BG: 40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white 49=default

    color("31;1;5")

    After the above command, the following character output will be
    Red Bold and Blinking.
    """
    out(f"\033[{colour}m")


def set_htab():
    out("\033H")


def clear_htab():
    out("\033[g")


def clear_all_htab():
    out("\033[3g")


def double_height_top():
    """
    Sets current line to be the upper half of a double height line.
    Both lines must contain the same text.
    """
    out("\033#3")


def double_height_bottom():
    """
    Sets current line to be the bottom half of a double height line.
    Both lines must contain the same text.
    """
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
    """Use smooth scrolling if supported."""
    out("\033[?4h")


def jump_scroll():
    """Use jump scrolling."""
    out("\033[?4l")


def scroll_origin():
    """Sets the origin or home, to the scroll region if defined."""
    out("\033[?6h")


def screen_origin():
    """Sets the origin or home, to the screens upper left corner."""
    out("\033[?6l")


def scroll_region(top, bottom):
    """Defines a scroll region given a top and bottom row."""
    out(f"\033[{top};{bottom}r")


def addstr(row=-1, col=-1, text="", attribute=""):
    """
    Outputs text at row and column with optional character attributes.
    if row and col are -1, then text is output at the cursors current
    position. All attribute flags are cleared at the end.
    """
    if col != -1 or row != -1:
        move(row, col)
    if attribute:
        color(attribute)
    out(text)
    if attribute:
        attr_off()


def move(row, col):
    """Moves cursor to new location"""
    out(f"\033[{row};{col}H")


def hline(length=1):
    """
    Makes a horizontal line starting at the cursors current position.
    If no length is given, a single horizontal character is output.
    """
    sg0()
    for _ in range(0, length):
        out("q")
    ug0()


def mvhline(row, col, length):
    """Makes a horizontal line using vt100 line characters"""
    move(row, col)
    hline(length)


def vline(length=1):
    """
    Makes a vertical line starting at the cursors current position.
    If no length is given, a single vertical character is output.
    and the cursor is left positioned below it.
    """
    sg0()
    for _ in range(0, length):
        out("x")
        cursor_down()
        cursor_back()
    ug0()


def mvvline(row, col, length):
    """Makes a vertical line using vt100 line characters"""
    move(row, col)
    sg0()
    for pos in range(0, length):
        move(row + pos, col)
        out("x")
    ug0()


def title(row, col, width, title_text):
    """Position a string to be centered within a given width."""
    position = int((width / 2) - (len(title_text) / 2))
    move(row, col + position)
    ug0()
    out(title_text)


def title2(row, col, width, title_text):
    """
    Position a string to be centered within a given width.
    Adding markers at either side.
    """
    position = int((width / 2) - (len(title_text) / 2))
    move(row, col + position - 1)
    sg0()
    out("u")
    ug0()
    out(title_text)
    sg0()
    out("t")
    ug0()


def box(row, col, height, width, title_text=""):
    """
    Create box with linedrawing characters with an
    optional top centered title.
    """
    move(row, col)
    sg0()
    out("l")
    hline(width - 2)
    sg0()
    out("k")
    if title_text:
        title(row, col, width, title_text)
    mvvline(row + 1, col, height - 2)
    mvvline(row + 1, col + (width - 1), height - 2)
    move(row + height - 1, col)
    sg0()
    out("m")
    hline(width - 2)
    sg0()
    out("j")
    ug0()


def autowrapon():
    """Turns on the terminals auto text wraping"""
    out("\033[?7h")


def autowrapoff():
    """Turns off the terminals auto text wraping"""
    out("\033[?7l")


def rjust(text, count, filler):
    """
    Right justifies 'text' string, padding it to 'count' length,
    padding it with 'filler' characters
    """
    needed = count - len(text)
    return (filler * needed) + text


def ljust(text, count, filler):
    """
    Left justifies 'text' string, padding it to 'count' length,
    padding it with 'filler' characters
    """
    needed = count - len(text)
    return text + (filler * needed)


def out(data):
    """Writes string to serial port."""
    usb_cdc.console.write(data.encode())


def getch():
    """
    Non-blocking.
    Returns -1 if no character is waiting.
    Returns on or more character bytes string otherwise.
    """
    count = usb_cdc.console.in_waiting
    if count:
        character = usb_cdc.console.read(count)
        return character
    else:
        return -1
