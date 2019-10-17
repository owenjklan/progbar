#!/usr/bin/env python
from __future__ import division
import time
import sys
import random


class TextProgressBar:
    """
    Text-mode progress bar supporting labels, colour and numeric output.
    """

    STYLE_HASHES = 1
    STYLE_BOXES1 = 2
    STYLE_BOXES2 = 3

    # def __init__(self, label, width, start, end):
    #     self.label = label
    #     self.start = start
    #     self.end = end
    #     self.width = width
    #     self.scale = (width / end)
    #     self.value = start
    #     self.complete = False

    def __init__(self, label, width, start, end, style=STYLE_HASHES,
                 show_percent=False, suffix=None):
        self.label = label
        if (len(label) > 16):
            self.label = label[0:7] + "..." + label[-6:]
        self.start = start
        self.end = end
        self.width = width
        self.scale = (width / end)
        self.value = start
        self.complete = False
        self.backchar = self._determine_backchar(style)
        self.frontchar = self._determine_frontchar(style)
        self.show_percent = show_percent
        self.suffix = suffix

    def _determine_backchar(cls, style):
        if style == cls.STYLE_HASHES:
            return '='
        elif style == cls.STYLE_BOXES1:
            return u"\u2591"
        else:
            return '='

    def _determine_frontchar(cls, style):
        if style == cls.STYLE_HASHES:
            return '#'
        elif style == cls.STYLE_BOXES1:
            return u"\u2589"
        else:
            return '#'

    def render(self):
        if (self.value >= self.end):
            self.value = self.end
            self.complete = True
        count = int(self.value * self.scale)
        redstart = "\033[31m"
        whitestart = "\033[37m\033[22m"
        greenstart = "\033[32m\033[1m"
        stdout = sys.stdout
        stdout.write("\r " + '{: ^20s}'.format(self.label) + " : |")
        sys.stdout.write(
            redstart + (self.backchar * self.width) + whitestart + "|")

        # Show the trailing numeric info
        if self.show_percent:
            perc = (self.value / self.end) * 100
            sys.stdout.write("{:3.1f}%".format(perc))
        else:
            sys.stdout.write(str(self.value) + " of " + str(self.end))
            if self.suffix:
                sys.stdout.write(" {}".format(self.suffix))

        sys.stdout.write("\r " + '{: ^20s}'.format(self.label) + " : |")

        sys.stdout.write(greenstart)
        for x in range(self.start, count):
            sys.stdout.write(self.frontchar)
        sys.stdout.write(whitestart)

        sys.stdout.flush()
        if (self.complete):
            print

    def add(self, value):
        self.value = self.value + value
        if self.value > self.end:
            self.value = self.end


if __name__ == "__main__":
    random.seed(0xcafedead)
    sourcefiles = [("bag.txt", 39), ("readme.hlp", 123), ("main.cs", 321),
                   ("longassedfilenamasdfasdfasdfasdfe", 100),
                   ("BlogsText.html", 1022),
                   ("secretdata.pdf", 430),
                   ("IEPurger.java", 320),
                   ("moreLongNamedFiles.zip", 1101),
                   ("last.one", 2045)]

    for srcfile in sourcefiles:
        tbr = TextProgressBar(
            srcfile[0], 80, 0, srcfile[1],
            style=TextProgressBar.STYLE_BOXES1,
            show_percent=False, suffix="bytes")
        for temp in range(0, srcfile[1]):
            tbr.add(random.randint(1, 50))
            tbr.render()
            time.sleep(0.1)
            if (tbr.complete):
                break
