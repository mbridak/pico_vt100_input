"""Testing EditField class"""
# pylint: disable=invalid-name


#from curses.ascii import isalnum, isprint
import vt100


class EditTextField:
    """basic text field edit"""

    def __init__(self, y=0, x=0, length=10):
        self.textfield = ""
        self.max_length = length
        self.position_x = x
        self.position_y = y
        self.cursor_position = 0
        self.length = 0
        self.is_bool = False
        self.my_state = False
        self.allow_lowercase = False
        self.allow_spaces = False
        self.is_URL = False

    def isalnum(self, character) -> bool:
        """Return True if alpha numeric"""
        character = character.decode()
        if character in "abcdefghijklmnopqrstuvwxyz":
            return True
        if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return True
        if character in "0123456789":
            return True
        return False
        
    def isprint(self, character) -> bool:
        """Return True if printable character"""
        character = character.decode()
        if character in "!@#$%^&*()_+-=`~[]\\\"{}|;:',<.>/?":
            return True
        return False

    def getchar(self, character) -> None:
        """Process character or control sequence"""
        if character == -1:
            return
        if self.is_bool:
            if character.decode() == " ":
                self.toggle_state()
                self.get_focus()
                return
            try:
                if character.decode() in "XxYy1":
                    self.set_state(True)
                    self.get_focus()
                    return
                if character.decode() in "0nN":
                    self.set_state(False)
                    self.get_focus()
                    return
            except ValueError:
                pass
        else:
            if character == vt100.KEY_LEFT:
                self.cursor_position -= 1
                self.cursor_position = max(self.cursor_position, 0)
            if character == vt100.KEY_RIGHT:
                self.cursor_position += 1
                if self.cursor_position > len(self.textfield):
                    self.cursor_position = len(self.textfield)
            if character == vt100.KEY_BACKSPACE:
                if self.cursor_position > 0:
                    self.textfield = (
                        self.textfield[: self.cursor_position - 1]
                        + self.textfield[self.cursor_position :]
                    )
                    self.cursor_position -= 1
                    self.cursor_position = max(self.cursor_position, 0)
            if character == vt100.KEY_DC:
                self.textfield = (
                    self.textfield[: self.cursor_position]
                    + self.textfield[self.cursor_position + 1 :]
                )
            if (
                self.isalnum(character)
                or character == ord(".")
                or (character.decode() == " " and self.allow_spaces)
                or (self.isprint(character) and self.is_URL)
            ):
                if len(self.textfield) < self.max_length:
                    self.textfield = f"{self.textfield[:self.cursor_position]}{chr(int.from_bytes(character, 'big'))}{self.textfield[self.cursor_position:]}"
                    if not self.allow_lowercase and not self.is_URL:
                        self.textfield = self.textfield.upper()
                    self.cursor_position += 1
            vt100.attr_underline()
            vt100.addstr(
                self.position_y, self.position_x, " " * self.max_length
            )
            vt100.attr_off()
            vt100.addstr(
                self.position_y, self.position_x, self.textfield
            )
            self._movecursor()

    def _movecursor(self) -> None:
        """moves cursor to current position"""
        vt100.move(self.position_y, self.position_x + self.cursor_position)

    def placeholder(self, phtext: str) -> None:
        """Show a placeholder"""
        if self.textfield == "":
            vt100.addnstr(phtext, self.max_length, curses.A_DIM)
            self._movecursor()

    def lowercase(self, allow):
        """Allows a field to have lowercase letters"""
        self.allow_lowercase = bool(allow)

    def spaces(self, allow):
        """Allows a field to have lowercase letters"""
        self.allow_spaces = bool(allow)

    def set_bool(self, is_bool: bool) -> None:
        """Sets behaviour of input to boolian or text input"""
        self.is_bool = is_bool

    def set_url(self, is_url: bool) -> None:
        self.is_URL = is_url

    def get_state(self):
        """Return the boolean state"""
        return self.my_state

    def toggle_state(self):
        """Toggles the logical state if it's a bool"""
        self.set_state(not self.my_state)

    def set_state(self, state):
        """Sets the boolean state"""
        self.my_state = bool(state)
        if self.my_state:
            self.set_text("✓")
        else:
            self.set_text(" ")
 
    def text(self) -> str:
        """Returns contents of field"""
        return self.textfield

    def clearfield(self) -> None:
        """clear the field"""
        self.textfield = ""
        self.cursor_position = 0

    def set_text(self, input_string: str) -> None:
        """Set the contents of the edit field"""
        self.textfield = input_string
        self.cursor_position = len(self.textfield)

    def get_cursor_position(self):
        """return current cursor position"""
        return self.cursor_position

    def set_cursor_position(self, position: int) -> None:
        """set cursor position"""
        self.cursor_position = position

    def get_focus(self):
        """redisplay textfield, move cursor to end"""
        vt100.attr_underline()
        vt100.addstr(self.position_y, self.position_x, " " * self.max_length)
        vt100.attr_off()
        vt100.addstr(self.position_y, self.position_x, self.textfield)
        self.set_cursor_position(len(self.textfield) * (not self.is_bool))
        vt100.move(self.position_y, self.position_x + self.cursor_position)
        
    def logger(self, text):
        vt100.save_cursor()
        vt100.home()
        vt100.out(text)
        vt100.out("     ")
        vt100.restore_cursor()
