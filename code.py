"""
Example implementation of an text input interface to a vt100 terminal with RP2040 CircuitPython.
"""

# Who's to blame: Michael Bridak
# Where to complain: Michael.Bridak@gmail.com or @k6gte@mastodon.radio

import time
import vt100
from edittextfield import EditTextField


def show():
    """
    Process inputs.

    TAB and Shift-TAB to move to different fields.
    Left-Arrow and Right Arrow to move cursor inside input field.
    Delete, deletes character to the right, shifting rest to the left.
    Toggle Radio Button with SPACE, or XxYy1 for on, 0nN for off.
    """
    input_field_focus = 0
    input_fields[input_field_focus].get_focus()
    while True:
        c = vt100.getch()
        if c != -1:
            pass
        if c == vt100.KEY_TAB:
            input_field_focus += 1
            if input_field_focus > len(input_fields) - 1:
                input_field_focus = 0
            input_fields[input_field_focus].get_focus()
            continue
        if c == vt100.KEY_SHIFT_TAB:
            input_field_focus -= 1
            if input_field_focus < 0:
                input_field_focus = len(input_fields) - 1
            input_fields[input_field_focus].get_focus()
            continue
        if c == vt100.KEY_ESCAPE:
            vt100.cls()
            vt100.home()
            return False
        if c == vt100.KEY_ENTER:
            vt100.cls()
            vt100.home()
            return True
        # Pass the input to the edit field for processing.
        input_fields[input_field_focus].getchar(c)


vt100.set80cols()
vt100.cls()
vt100.home()
vt100.cursor_down()

vt100.double_height_top()
print("VT102 Test Screen")
vt100.double_height_bottom()
print("VT102 Test Screen")

vt100.attr_off()
vt100.addstr(10, 1, "Normal")
vt100.attr_bold()
vt100.addstr(11, 1, "Bold")
vt100.attr_off()
vt100.attr_dim()
vt100.addstr(12, 1, "Dim")
vt100.attr_off()
vt100.attr_underline()
vt100.addstr(13, 1, "Underline")
vt100.attr_off()
vt100.attr_reverse()
vt100.addstr(14, 1, "Reverse")
vt100.attr_off()
vt100.attr_blink()
vt100.addstr(15, 1, "Blink")
vt100.attr_off()

vt100.box(4, 10, 4, 18)
vt100.addstr(5, 11, "Input:")
input_alphanum = EditTextField(5, 18, 9)
input_alphanum.allow_lowercase = True
input_alphanum.allow_spaces = True
input_alphanum.set_text("Edit me")

vt100.addstr(6, 11, "Radio Button [_]")
radio_button = EditTextField(6, 25, 1)
radio_button.set_bool(True)

input_fields = [input_alphanum, radio_button]
for item in input_fields:
    item.get_focus()

input_alphanum.get_focus()
result = show()

print(f"The input dialog returned: {result}")
print(f"The input field returned: {input_alphanum.text()}")
print(f"The radio button was set to: {radio_button.get_state()}")
