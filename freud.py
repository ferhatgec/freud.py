#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# freud[dot]py - python implementation of Freud (fpaper (an e-paper file format) renderer)
# (executable, library)
#
# github.com/ferhatgec/freud.py
# github.com/ferhatgec/fpaper.py
# github.com/ferhatgec/fpaper
# github.com/ferhatgec/totem
# github.com/ferhatgec/totem.py
# github.com/ferhatgec/freud

import os
import sys
import termios
import tty

escape = 27
up = 65
down = 66


def get_terminal_size() -> (int, int):
    from fcntl import ioctl
    from struct import pack, unpack

    with open(os.ctermid(), 'r') as fd:
        packed = ioctl(fd, termios.TIOCGWINSZ, pack('HHHH', 0, 0, 0, 0))
        rows, cols, h_pixels, v_pixels = unpack('HHHH', packed)

    return rows, cols


class FPaperMarkers:
    START_MARKER = b'\x02'
    START_MARKER_2 = b'\x46'
    START_MARKER_3 = b'\x50'
    START_MARKER_4 = b'\x61'
    START_MARKER_5 = b'\x67'
    START_MARKER_6 = b'\x65'

    START_OF_TEXT = b'\x26'
    END_OF_TEXT = b'\x15'

    STYLE_MARKER = b'\x1A'
    LIGHT_SET = b'\x30'
    BOLD_SET = b'\x31'
    DIM_SET = b'\x32'
    ITALIC_SET = b'\x33'
    UNDERLINED_SET = b'\x34'
    BLINK_SET = b'\x35'
    RAPID_BLINK_SET = b'\x36'

    COLOR_RESET = b'\x72'

    # These styles must be rendered by renderer implementation
    ALIGN_LEFT_SET = b'\x7B'
    ALIGN_CENTER_SET = b'\x7C'
    ALIGN_RIGHT_SET = b'\x7D'
    ALIGN_RESET = b'\x7E'

    def __init__(self):
        pass

    def is_start_marker(self, ch) -> bool:
        return True if ch == self.START_MARKER else False

    def is_start_marker_2(self, ch) -> bool:
        return True if ch == self.START_MARKER_2 else False

    def is_start_marker_3(self, ch) -> bool:
        return True if ch == self.START_MARKER_3 else False

    def is_start_marker_4(self, ch) -> bool:
        return True if ch == self.START_MARKER_4 else False

    def is_start_marker_5(self, ch) -> bool:
        return True if ch == self.START_MARKER_5 else False

    def is_start_marker_6(self, ch) -> bool:
        return True if ch == self.START_MARKER_6 else False

    def is_start_of_text(self, ch) -> bool:
        return True if ch == self.START_OF_TEXT else False

    def is_end_of_text(self, ch) -> bool:
        return True if ch == self.END_OF_TEXT else False

    def is_style_marker(self, ch) -> bool:
        return True if ch == self.STYLE_MARKER else False

    def is_light_marker(self, ch) -> bool:
        return True if ch == self.LIGHT_SET else False

    def is_bold_marker(self, ch) -> bool:
        return True if ch == self.BOLD_SET else False

    def is_dim_marker(self, ch) -> bool:
        return True if ch == self.DIM_SET else False

    def is_italic_marker(self, ch) -> bool:
        return True if ch == self.ITALIC_SET else False

    def is_underlined_marker(self, ch) -> bool:
        return True if ch == self.UNDERLINED_SET else False

    def is_blink_marker(self, ch) -> bool:
        return True if ch == self.BLINK_SET else False

    def is_rapid_marker(self, ch) -> bool:
        return True if ch == self.RAPID_BLINK_SET else False

    def is_color_reset(self, ch) -> bool:
        return True if ch == self.COLOR_RESET else False

    def is_left_align(self, ch) -> bool:
        return True if ch == self.ALIGN_LEFT_SET else False

    def is_center_align(self, ch) -> bool:
        return True if ch == self.ALIGN_CENTER_SET else False

    def is_right_align(self, ch) -> bool:
        return True if ch == self.ALIGN_RIGHT_SET else False

    def is_reset_align(self, ch) -> bool:
        return True if ch == self.ALIGN_RESET else False


class FPaper_Extract:
    def __init__(self, filename: str):
        self.check: FPaperMarkers = FPaperMarkers
        self.filename: str = filename
        self.extracted_text: str = ''
        self.get_align_text: str = ''

        self.is_start_marker = False
        self.is_start_marker_2 = False
        self.is_start_marker_3 = False
        self.is_start_marker_4 = False
        self.is_start_marker_5 = False
        self.is_start_marker_6 = False

        self.is_start_of_text = False
        self.is_end_of_text = False

        self.is_style_marker = False

        self.is_align = False
        self.is_left_align = False
        self.is_center_align = False
        self.is_right_align = False
        self.is_reset_align = False

        self.__w__, self.__h__ = get_terminal_size()

    def left(self, width: int, text: str):
        self.extracted_text += text

        for i in range(0, width):
            self.extracted_text += ' '

    def center(self, width: int, text: str):
        for i in range(0, width):
            self.extracted_text += ' '

        self.extracted_text += text

        for i in range(0, width):
            self.extracted_text += ' '

    def right(self, width: int, text: str):
        for i in range(0, width * 2):
            self.extracted_text += ' '

        self.extracted_text += text

    def detect_style(self, ch):
        from platform import system
        # Just waiting for 3.10
        # Not platform specific
        if self.check.is_light_marker(self.check, ch):
            self.extracted_text += '\x1b[0m'
        elif self.check.is_bold_marker(self.check, ch):
            self.extracted_text += '\x1b[1m'
        elif self.check.is_dim_marker(self.check, ch):
            self.extracted_text += '\x1b[2m'
        elif self.check.is_italic_marker(self.check, ch):
            self.extracted_text += '\x1b[3m'
        elif self.check.is_underlined_marker(self.check, ch):
            self.extracted_text += '\x1b[4m'
        elif self.check.is_blink_marker(self.check, ch):
            self.extracted_text += '\x1b[5m'
        elif self.check.is_rapid_marker(self.check, ch):
            if system() == 'Windows':
                self.extracted_text += '\x1b[6m'
        elif self.check.is_left_align(self.check, ch):
            self.is_align = True

            self.is_right_align \
                = self.is_center_align \
                = self.is_reset_align = False
            self.is_left_align = True
        elif self.check.is_center_align(self.check, ch):
            self.is_align = True

            self.is_right_align \
                = self.is_left_align \
                = self.is_reset_align = False
            self.is_center_align = True
        elif self.check.is_right_align(self.check, ch):
            self.is_align = True

            self.is_center_align \
                = self.is_left_align \
                = self.is_reset_align = False
            self.is_right_align = True
        elif self.check.is_reset_align(self.check, ch):
            if self.is_center_align:
                self.center(self.__w__, self.get_align_text)
            elif self.is_left_align:
                self.left(self.__w__, self.get_align_text)
            elif self.is_right_align:
                self.right(self.__w__, self.get_align_text)

            self.is_align = False

            self.is_center_align \
                = self.is_left_align \
                = self.is_reset_align \
                = self.is_right_align = False

            self.get_align_text = ''
        elif self.check.is_color_reset(self.check, ch):
            self.extracted_text += '\x1b[0m'
        else:
            data = ord(ch.decode('utf-8'))
            if (40 <= data <= 49) or (100 <= data <= 109):
                self.extracted_text += f'\x1b[{data - 10}m'

    def detect(self, ch):
        if self.is_style_marker:
            self.detect_style(ch)
            self.is_style_marker = False
            return

        if not self.is_start_marker:
            self.is_start_marker = self.check.is_start_marker(self.check, ch)
        elif not self.is_start_marker_2:
            self.is_start_marker_2 = self.check.is_start_marker_2(self.check, ch)
        elif not self.is_start_marker_3:
            self.is_start_marker_3 = self.check.is_start_marker_3(self.check, ch)
        elif not self.is_start_marker_4:
            self.is_start_marker_4 = self.check.is_start_marker_4(self.check, ch)
        elif not self.is_start_marker_5:
            self.is_start_marker_5 = self.check.is_start_marker_5(self.check, ch)
        elif not self.is_start_marker_6:
            self.is_start_marker_6 = self.check.is_start_marker_6(self.check, ch)
        elif not self.is_start_of_text:
            self.is_start_of_text = self.check.is_start_of_text(self.check, ch)
        elif self.is_start_of_text:
            if self.check.is_style_marker(self.check, ch):
                self.is_style_marker = True
                return

            if self.check.is_end_of_text(self.check, ch):
                self.is_end_of_text = True
                return

            if self.is_align:
                self.get_align_text += ch.decode('utf-8')
            else:
                self.extracted_text += ch.decode('utf-8')

    def extract(self):
        with open(self.filename, 'rb') as file:
            byte = file.read(1)
            while byte:
                if self.is_end_of_text:
                    break
                self.detect(byte)
                byte = file.read(1)

        return self.extracted_text


class Totem:
    def __init__(self, filename: str):
        self.file_data: str = ''
        self.__up__: int = 0
        self.__down__: int = 0
        self.__full_length__: int = 0

        self.extract = FPaper_Extract(filename)
        self.file_data = self.extract.extract()

        self.__down__ = len(self.file_data.splitlines())

        self.__full_length__ = self.__down__
        self.__w__, self.__h__ = get_terminal_size()
        self.old__ = termios.tcgetattr(sys.stdin.fileno())
        self.new__ = termios.tcgetattr(sys.stdin.fileno())

    def init_buffer(self):
        self.clear()
        self.to_up()
        self.__down__ = (self.__h__ / 3.95)
        self.__from__(False)
        self.disable_cursor()

        self.new__[3] = self.new__[3] & ~termios.ECHO
        try:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.new__)
            while True:
                ch = self.getchar()

                if ch.lower() == 'q':
                    break

                ch = self.getchar()
                ch = self.getchar()
                if ch == 'A':
                    if 1 <= self.__up__:
                        self.__up__ -= 1
                        self.__down__ -= 1
                        self.__from__(False)
                        continue
                if ch == 'B':
                    if self.__down__ < self.__full_length__:
                        self.__down__ += 1
                        self.__up__ += 1
                        self.__from__(False)
                        continue
        finally:
            self.enable_cursor()
            self.clear()
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.old__)

    def __from__(self, is_up: bool):
        i = 0
        __new: str = ''
        if is_up:
            for line in self.file_data.splitlines():
                if i >= self.__up__:
                    __new += f'{line}\n'

            i += 1
        else:
            for line in self.file_data.splitlines():
                if i < self.__down__:
                    __new += f'{line}\n'

                i += 1

        self.clear()
        print(end=__new)
        self.up_to(self.__up__)

    @staticmethod
    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    @staticmethod
    def refresh():
        print(end='\x1b[2J')

    @staticmethod
    def clear():
        Totem.refresh()
        print(end='\x1b[H')

    @staticmethod
    def to_up():
        print(end='\x1b[0A')

    @staticmethod
    def up_to(n: int):
        print(end='\x1b[' + str(n) + 'A')

    @staticmethod
    def disable_cursor():
        print(end='\x1b[?25l')

    @staticmethod
    def enable_cursor():
        print(end='\x1b[?25h')


if len(sys.argv) < 2:
    exit(1)

init = Totem(sys.argv[len(sys.argv) - 1])

init.init_buffer()
