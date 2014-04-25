from __future__ import print_function
import subprocess
import re
from usb_virtual_sensor import USBVirtualSensor
from sensed_event import SensedEvent


class TemperatureVirtualSensor(USBVirtualSensor):
	def __init__(
		self, queue, device,
		daemon_path,
		threshold
	):
		USBVirtualSensor.__init__(self, queue, device)
		self._daemon_path = daemon_path
		self._threshold = threshold
		self._result = None
		self._regexp = re.compile(r'Device ([^:]*): Sensor ([0-9]*): Temperature: ([0-9\.]*)')

	def type(self):
		return "Temperature Sensor"

	def connect(self):
		self._result = subprocess.Popen(
#			self._daemon_path,
			['temperature-streams'],
			shell=True,
			stdout=subprocess.PIPE
		)

	def read(self):
		line = next(iter(self._result.stdout.readline, '')) 
		match = self._regexp.match(line)
		try:
			temperature = float(match.group(3))
		except AttributeError as e:
			print('Error parsing temperature: %s' % e)
#		Notice: Next Statement is just used for debug temp Sensor
#		print(u'Temperature: %.2f\N{DEGREE SIGN}C' % temperature)
		return temperature

	def policy_check(self, data):
		temperature = data
		if temperature > self._threshold:
			return True

	def report_event(self, data):
		temperature = data
		self._queue.put(
			SensedEvent(
				sensor = self.device.device,
#				msg = u'%.2f\N{DEGREE SIGN}C' % temperature,
				msg = "High Temperature: " + str(temperature),
				priority = 50
			)
		)