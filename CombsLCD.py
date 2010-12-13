import sys, time, os, tty, termios, serial, urllib2
from xml.dom import minidom

class CombsLCD:
	def __init__(self, x_max, y_max):
		self._home			= "\x01"
		self._hide_cursor	= "\x04"
		self._scroll_off	= "\x14"
		self._clear			= "\x0c"
		self.x_max = x_max
		self.y_max = y_max
		self.y_pointer = 0
		self.x_pointer = 0
		self.currentIndex = 0
		self.currentText = []
#		self.ser = serial.Serial('/dev/cu.usbserial-00001004', 19200, timeout=1)
#		self.ser = serial.Serial('/dev/cu.usbserial-00002006', 19200, timeout=1)

	def display(self):
		#self.displayToLCD()
		self.displayToConsole()

	def displayToLCD(self):
		self.ser.write(self._clear)
		self.ser.write(self._scroll_off)
		self.ser.write(self._hide_cursor)
		for i in range(self.y_pointer,self.y_pointer + self.y_max):
			try:
				for j in self.currentText[self.currentIndex][i]:
					self.ser.write(j)
			except:
				self.ser.write(" " * self.x_max)
	
	def displayToConsole(self):
		os.system('clear')
		print(self.x_pointer, self.y_pointer)
		sys.stdout.write("|" + "-" * self.x_max + "|\n")
		for i in range(self.y_pointer,self.y_pointer + self.y_max):
			try:
				sys.stdout.write("|" + self.currentText[self.currentIndex][i] + "|\n")
			except:
				sys.stdout.write("|" + " " * self.x_max + "|\n")
		sys.stdout.write("|" + "-" * self.x_max + "|\n")

	def addTextBlock(self, t):
		temp = ""
		charCount = 0
		currentBlock = []
		for i in range(len(t)):
			temp += t[i]
			charCount += 1
			if ((charCount % (self.x_max)) == 0):
				currentBlock.append(temp)
				temp = ""
				charCount = 0
			if (i == len(t) - 1):
				temp = temp + (" " * (self.x_max - len(temp)))
				currentBlock.append(temp)
		self.currentText.append(currentBlock)

	def printCurrentText(self):
		print len(self.currentText)

	def yDown(self, howFar):
		if (self.y_pointer < len(self.currentText[self.currentIndex]) - self.y_max):
			self.y_pointer += howFar

	def yUp(self, howFar):
		if (self.y_pointer > 0):
			self.y_pointer -= howFar

	def nextTextBlock(self):
		self.y_pointer = 0
		if (self.currentIndex == len(self.currentText) - 1):
			self.currentIndex = 0
		else:
			self.currentIndex += 1
	
	def prevTextBlock(self):
		self.y_pointer = 0
		if (self.currentIndex == 0):
			self.currentIndex = len(self.currentText) - 1
		else:
			self.currentIndex -= 1

	def closeSerial(self):
		self.ser.close()

def getchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def wsCall(url):
	try:
		data = urllib2.urlopen(url).read()
	except urllib2.HTTPError, e:
		print "HTTP error: %d" % e.code
	except urllib2.URLError, e:
		print "Network error: %s" % e.reason.args[1]
	return minidom.parseString(data)

def main():

	test = wsCall("http://weather.yahooapis.com/forecastrss?w=2502265")
	print(test.childNodes[0].childNodes[1].childNodes[17].attributes["chill"].value)
	exit()

	x = CombsLCD(20,4)

	x.addTextBlock("This is a sample sentence right here to test how the lcd will display this sample sentence right here and here it is.")
	x.addTextBlock("Both set and frozenset support set to set comparisons. Two sets are equal if and only if every element of each set is contained in the other (each is a subset of the other). A set is less than another set if and only if the first set is a proper subset of the second set (is a subset, but is not equal). A set is greater than another set if and only if the first set is a proper superset of the second set (is a superset, but is not equal).  Both set and frozenset support set to set comparisons. Two sets are equal if and only if every element of each set is contained in the other (each is a subset of the other). A set is less than another set if and only if the first set is a proper subset of the second set (is a subset, but is not equal). A set is greater than another set if and only if the first set is a proper superset of the second set (is a superset, but is not equal).  Both set and frozenset support set to set comparisons. Two sets are equal if and only if every element of each set is contained in the other (each is a subset of the other). A set is less than another set if and only if the first set is a proper subset of the second set (is a subset, but is not equal). A set is greater than another set if and only if the first set is a proper superset of the second set (is a superset, but is not equal).")
	x.addTextBlock("Dictionaries can be created by placing a comma-separated list of key: value pairs within braces, for example: {'jack': 4098, 'sjoerd': 4127} or {4098: 'jack', 4127: 'sjoerd'}, or by the dict constructor.")
	x.display()
	while 1:
		c = getchar()
		if (c == "\x1b"):
			c = getchar()
			if (c == "\x5b"):
				c = getchar()
				if (c == "\x41"):
					x.yUp(1)
					x.display()
				elif (c == "\x42"):
					x.yDown(1)
					x.display()
				elif (c == "\x43"):
					x.nextTextBlock()
					x.display()
				elif (c == "\x44"):
					x.prevTextBlock()
					x.display()
		elif (c == "q"):
#			x.closeSerial()
			exit()

if __name__ == "__main__":
	main()
