import serial


class SerialHandler:
	def __init__(self, port='/dev/ttyAMA0', timeout=0.1, baud_rate=9600):
		self.handler = serial.Serial(port, baud_rate, timeout=timeout)
	
	def read(self):
		text = self.handler.read()
		return text.decode('utf-8')
		
		
	def read_line(self):
		line = self.handler.readline()
		return line.decode('utf-8')
	
	def write(self, text):
		try:
			to_send = text.encode('utf-8')
		except (UnicodeDecodeError, AttributeError):
			pass
		self.handler.write(to_send)
		
	def write_line(self, line):
		to_send_line = ""
		try:
			to_send_line = line.encode('utf-8')
		except (UnicodeEncodeError, AttributeError):
			pass
			
		if not to_send_line.endswith('\n'.encode('utf-8')):
			to_send_line.append('\n'.encode('utf-8'))
			
			
		self.handler.write(to_send_line)
		
		
		
