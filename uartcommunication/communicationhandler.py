import serial


class SerialHandler:
	def __init__(self, port='/dev/ttyAMA0', timeout=0.1, baud_rate=9600, encoding='utf-8'):
		self.handler = serial.Serial(port, baud_rate, timeout=timeout)
		self.encoding = encoding
	
	def read(self):
		text = self.handler.read()
		return text.decode(self.encoding)
		
		
	def read_line(self):
		line = self.handler.readline()
		return line.decode(self.encoding)
	
	def write(self, text):
		try:
			to_send = text.encode(self.encoding)
		except (UnicodeDecodeError, AttributeError):
			pass
		self.handler.write(to_send)
		
	def write_line(self, line):
		to_send_line = ""
		try:
			to_send_line = line.encode(self.encoding)
		except (UnicodeEncodeError, AttributeError):
			print("UnicodeEncodeError")
			pass
			
		if not to_send_line.endswith('\n'.encode(self.encoding)):
			to_send_line.append('\n'.encode(self.encoding))
			
			
		self.handler.write(to_send_line)
