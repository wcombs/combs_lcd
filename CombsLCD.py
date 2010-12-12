import sys, time, os, tty, termios, serial


def getchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

class CombsLCD:
	def __init__(self, x_max, y_max):
		self._home = "\x01"
		self._clear = "\x0c"
		self.x_max = x_max
		self.y_max = y_max
		self.y_pointer = 0
		self.x_pointer = 0
		self.currentText = []
		self.ser = serial.Serial('/dev/cu.usbserial-00001004', 19200, timeout=1)
		#self.ser = serial.Serial('/dev/cu.usbserial-00002006', 19200, timeout=1)
	def displayToConsole(self):
		os.system('clear')
		self.ser.write(self._clear)
		print(self.x_pointer, self.y_pointer)
		sys.stdout.write("|" + "-" * self.x_max + "|\n")
		for i in range(self.y_pointer,self.y_pointer + self.y_max):
			try:
				for j in self.currentText[i]:
					self.ser.write(j)
				sys.stdout.write("|" + self.currentText[i] + "|\n")
			except:
				sys.stdout.write("|" + " " * self.x_max + "|\n")
		
		sys.stdout.write("|" + "-" * self.x_max + "|\n")
	def setText(self, t):
		temp = ""
		charCount = 0
		for i in range(len(t)):
			temp += t[i]
			charCount += 1
			if ((charCount % (self.x_max)) == 0):
				self.currentText.append(temp)
				temp = ""
				charCount = 0
			if (i == len(t) - 1):
				temp = temp + (" " * (self.x_max - len(temp)))
				self.currentText.append(temp)
	def printCurrentText(self):
		print self.currentText
	def yDown(self, howFar):
		if (self.y_pointer < len(self.currentText) - self.y_max):
			self.y_pointer += howFar
	def yUp(self, howFar):
		if (self.y_pointer > 0):
			self.y_pointer -= howFar
	def closeSerial(self):
		self.ser.close()

def main():
	x = CombsLCD(20,4)

	x.setText("This is a sample sentence right here to test how the lcd will display this sample sentence right here and here it is.")
	x.displayToConsole()
	while 1:
		c = getchar()
		if (c == "\x1b"):
			c = getchar()
			if (c == "\x5b"):
				c = getchar()
				if (c == "\x41"):
					x.yUp(1)
					x.displayToConsole()
				elif (c == "\x42"):
					x.yDown(1)
					x.displayToConsole()
		elif (c == "q"):
			x.closeSerial()
			exit()

if __name__ == "__main__":
	main()
