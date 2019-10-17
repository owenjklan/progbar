from __future__ import division
import time
import math
import string
import sys
import random

class TextProgressBar:
	def __init__(self, label, width, start, end):
		self.label = label
		self.start = start
		self.end = end
		self.width = width
		self.scale = (width / end)
		self.value = start
		self.complete = False

	def __init__(self, label, width, start, end):
		self.label = label
		if (len(label) > 16):
		 	self.label = label[0:7] + "..." + label[-6:]
		self.start = start
		self.end = end
		self.width = width
		self.scale = (width / end)
		self.value = start
		self.complete = False

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
		sys.stdout.write(redstart + ("="*self.width) + whitestart + "|")
		sys.stdout.write(str(self.value) + " of " + str(self.end))
		sys.stdout.write("\r " + '{: ^20s}'.format(self.label) + " : |")
		
		sys.stdout.write(greenstart)
		for x in range(self.start, count):
			sys.stdout.write("#")
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
		tbr = TextProgressBar(srcfile[0], 80, 0, srcfile[1])
		for temp in range(0, srcfile[1]):
			tbr.add(random.randint(1,50))
			tbr.render()
			time.sleep(0.01)
			if (tbr.complete):
				break