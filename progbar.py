#!/usr/bin/env python
# -*- coding: latin-1 -*-
from __future__ import division
import time
import sys
from sys import stdout
import random


class TextProgressBar:
    """
    Text-mode progress bar supporting labels, colour and numeric or percent
    output.

    Several styles available:

    """

    STYLE_HASHES = 1
    STYLE_BOXES1 = 2
    STYLE_BOXES2 = 3
    STYLE_UNDERSCORED = 4

    def __init__(self, label, width, start, end, style=STYLE_HASHES,
                 show_percent=False, suffix=None):
        """
        label: will be truncated to 16 characters by default. Shown at left
        width: how many characters wide the progress bar will be
        start: beginning value for the progress bar
        end:   ending value for the progress bar when at "100%"
        style: One of:
            SYTLE_HASHES:      |###====|
            SYTLE_BOXES1:      |▉▉▉▉▉░░|
            SYTLE_BOXES2:      |▉▉▉▉▉░░|
            STYLE_UNDERSCORED: |▉▉▉____|
            STYLE_BOXES2:   -- Not Currently Implemented -- (Dec. 2019)
        show_percent:   False:       20 of 100
                        True:           20%
        suffix:  Text to append to numeric/percentage readout.
                 Example:  suffix="bytes"  ==>    1023 of 2048 bytes
                 Note: Suffix is NOT displayed when 'show_percent' is True
        """
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
        elif style == cls.STYLE_UNDERSCORED:
            return "_"
        else:
            return '='

    def _determine_frontchar(cls, style):
        if style == cls.STYLE_HASHES:
            return '#'
        elif style == cls.STYLE_BOXES1:
            return u"\u2589"
        elif style == cls.STYLE_UNDERSCORED:
            return u"\u2589"
        else:
            return '#'

    def render(self, linenum=None):
        """
        Clear the current line and render the current value of the progress
        bar.

        Optional linenum will move cursor to a given line before rendering.
        The top line is line 0.
        """
        if (self.value >= self.end):
            self.value = self.end
            self.complete = True
        count = int(self.value * self.scale)
        redstart = "\033[31m"
        whitestart = "\033[37m\033[22m"
        greenstart = "\033[32m\033[1m"

        if linenum is not None:
            stdout.write("\033[{}H".format(linenum))
        stdout.write("\r " + '{: ^20s}'.format(self.label) + " |")
        stdout.write(
            redstart + (self.backchar * self.width) + whitestart + "| ")

        # Show the trailing numeric info
        if self.show_percent:
            perc = (self.value / self.end) * 100
            stdout.write("{:3.1f}%".format(perc))
        else:
            stdout.write(str(self.value) + " of " + str(self.end))
            if self.suffix:
                stdout.write(" {}".format(self.suffix))

        # Save cursor position in terminal
        stdout.write("\033[s")

        stdout.write("\r " + '{: ^20s}'.format(self.label) + " |")

        stdout.write(greenstart)
        for x in range(self.start, count):
            stdout.write(self.frontchar)
        stdout.write(whitestart)

        # Restore cursor position to the end of the count/percent text
        stdout.write("\033[u")

        # Clear to end of line
        stdout.write("\033[K")

        stdout.flush()
        if (self.complete):
            print

    def add(self, value):
        """
        Add the supplied value to the progress bar's current value.
        Includes a cap to ensure that a value that is larger than
        the end value cannot be set.
        """
        self.value = self.value + value
        if self.value > self.end:
            self.value = self.end


#
# Test program to demonstrate the progress bar in action
#
# Usage:
#  python progbar.py [style [percent]]
#
#  style:  1-4
#  percent: "percent" to display percentage. Anything else to use X of Y
#  suffix: optional suffix
#

if __name__ == "__main__":
    percent = False
    style = 1
    suffix = None
    if len(sys.argv) > 1:
        style = int(sys.argv[1])
    if len(sys.argv) > 2:
        percent = True if sys.argv[2].lower() == "percent" else False
    if len(sys.argv) > 3:
        suffix = sys.argv[3]

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
            style=style,
            show_percent=percent, suffix=suffix)
        for temp in range(0, srcfile[1]):
            tbr.add(random.randint(1, 50))
            tbr.render()
            time.sleep(0.1)
            if (tbr.complete):
                break

    for srcfile in sourcefiles:
        tbr = TextProgressBar(
            srcfile[0], 80, 0, srcfile[1],
            style=style,
            show_percent=percent, suffix=suffix)
        for temp in range(0, srcfile[1]):
            tbr.add(random.randint(1, 50))
            tbr.render(linenum=10)
            time.sleep(0.1)
            if (tbr.complete):
                break
