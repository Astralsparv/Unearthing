import sys
import select
import os
is_windows=os.name=="nt"

if (is_windows):
    import msvcrt
    import ctypes
    import time # linux&slop but only needed for microslop curtains
else:
    import termios
    import tty

class Keyboard:
    def __init__(self):
        if (is_windows):
            self.old_console_mode=None
        else:
            self.fd=sys.stdin.fileno()
            self.old_settings=termios.tcgetattr(self.fd)
        self.has_setup=False
            

    def setup(self):
        if (self.has_setup):
            return
        if (is_windows):
            self.setup_windows()
        else:
            self.setup_unix() # linux / mac? / whatever

        self.has_setup=True

    def setup_windows(self):
        kernel32=ctypes.windll.kernel32

        self._kernel32=kernel32

        STD_INPUT_HANDLE=-10

        self._stdin_handle=kernel32.GetStdHandle(STD_INPUT_HANDLE)

        # get the current console mode
        mode=ctypes.c_uint32()

        if (not kernel32.GetConsoleMode(
            self._stdin_handle,
            ctypes.byref(mode)
        )):
            raise OSError("GetConsoleMode failed")

        self._old_console_mode = mode.value

        # input mode flags (now just one)
        ENABLE_PROCESSED_INPUT=0x0001

        new_mode=ENABLE_PROCESSED_INPUT

        if (not kernel32.SetConsoleMode(
            self._stdin_handle,
            new_mode
        )):
            raise OSError("SetConsoleMode failed")
    
    def setup_unix(self):
        settings=termios.tcgetattr(self.fd)

        # don't print the characters
        # does stop text from being seen when you type it after program ends though,..
        settings[3] &= ~termios.ECHO

        # ctrl+c my beloved
        settings[3] |= termios.ISIG

        termios.tcsetattr(
            self.fd,
            termios.TCSADRAIN,
            settings
        )

        tty.setcbreak(self.fd)

    def restore(self):
        if (is_windows):
            # restore console mode
            if (self._old_console_mode is not None):
                self._kernel32.SetConsoleMode(
                    self._stdin_handle,
                    self._old_console_mode
                )
        else:
            termios.tcsetattr(
                self.fd,
                termios.TCSADRAIN,
                self.old_settings
            )

        self.has_setup=False

    # reads

    def read(self, timeout=None):
        if (is_windows):
            return self.read_windows(timeout)
        else:
            return self.read_unix(timeout)

    def read_windows(self,timeout):
        if (timeout==None):
            return msvcrt.getwch()
        
        end=time.monotonic()+timeout
        while (not msvcrt.kbhit()):
            if (time.monotonic()>=end):
                return None
            time.sleep(0.001) # 1ms
        return msvcrt.getwch()

    def read_unix(self,timeout):
        ready, _, _=select.select(
            [self.fd],
            [],
            [],
            timeout
        )

        if ready:
            return os.read(self.fd, 1).decode(errors="replace")

        return None

    # decoding whats read

    # CSI sequence

    def decode_csi(self):
        sequence=""

        while True:
            c=self.read(0.05)

            if (c==None):
                return "ESC"

            sequence+=c

            # csi final byte, why is there multiple.
            if ("\x40"<=c<="\x7e"):
                break

        # one char sequences
        onechar={
            "A":"UP",
            "B":"DOWN",
            "C":"RIGHT",
            "D":"LEFT",

            "H":"HOME",
            "F":"END",

            "Z":"SHIFT+TAB",
        }

        if (sequence in onechar):
            return onechar[sequence]

        # tilde sequences
        if sequence.endswith("~"):
            number=sequence[:-1]

            return {
                "1":"HOME",
                "2":"INSERT",
                "3":"DELETE",
                "4":"END",
                "5":"PAGEUP",
                "6":"PAGEDOWN",

                # function keys
                "11":"F1",
                "12":"F2",
                "13":"F3",
                "14":"F4",
                "15":"F5",
                "17":"F6",
                "18":"F7",
                "19":"F8",
                "20":"F9",
                "21":"F10",
                "23":"F11",
                "24":"F12",
            }.get(number, "ESC")

        return "ESC"

    def decode_ss3(self):
        c=self.read(0.05)

        if (c==None):
            return "ESC"

        return {
            "A":"UP",
            "B":"DOWN",
            "C":"RIGHT",
            "D":"LEFT",

            "H":"HOME",
            "F":"END",

            "P":"F1",
            "Q":"F2",
            "R":"F3",
            "S":"F4",
        }.get(c, "ESC")

    # ansi escape sequences
    def decode_escape_sequence(self):
        c=self.read(0.05)

        # alone = just escape
        if (c==None):
            return "ESC"

        #ESC[ == CSI sequence
        if (c=="["):
            return self.decode_csi()

        #ESCO == SS3 sequence
        if (c=="O"):
            return self.decode_ss3()

        # ???? neither ss3 or csi
        return "ESC"

    def decode_windows(self,key):
        if (key in ("\x00","\xe0")):
            c=self.read()

            return {
                "H":"UP",
                "P":"DOWN",
                "K":"LEFT",
                "M":"RIGHT",

                "G":"HOME",
                "O":"END",
                "R":"INSERT",
                "S":"DELETE",

                "I":"PAGEUP",
                "Q":"PAGEDOWN",

                ";":"F1",
                "<":"F2",
                "=":"F3",
                ">":"F4",
                "?":"F5",
                "@":"F6",
                "A":"F7",
                "B":"F8",
                "C":"F9",
                "D":"F10",
                "E":"F11",
                "F":"F12",
            }.get(c,"ESC")

        # ctrl+c my beloved (but microslop edition)
        if (key=="\x03"):
            raise KeyboardInterrupt

        # ctrl characters
        if (key in ("\r","\n")):
            return "ENTER"

        if (key=="\x08"):
            return "BACKSPACE"

        if (key=="\t"):
            return "TAB"

        if (key=="\x1b"):
            return "ESC"

        # ctrl+(a-z)
        if ("\x01"<=key<="\x1a"):
            letter=chr(ord("A")+ord(key)-1)
            return f"CTRL+{letter}"

        return key
    
    def decode_unix(self,key):
        if (key=="\x1b"):
            # ANSI escape sequence
            # key does not need feeding, it reads itself
            return self.decode_escape_sequence()

        if (key in ("\n", "\r")):
            return "ENTER"

        if (key in ("\x7f", "\b")):
            return "BACKSPACE"

        if (key=="\t"):
            return "TAB"

        # ctrl+(a-z)
        if ("\x01"<=key<="\x1a"):
            letter=chr(ord("A")+ord(key)-1)
            return f"CTRL+{letter}"

        return key
    
    # what other py files should be using; above is low level
    def get_key(self,timeout=None):
        key=self.read(timeout)

        if (key==None):
            return None

        if is_windows:
            return self.decode_windows(key)

        return self.decode_unix(key)