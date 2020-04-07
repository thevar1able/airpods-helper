#!/usr/bin/env python3

import time
import logging

from pydbus import SystemBus, SessionBus
from gi.repository import GLib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

system_bus = SystemBus()
session_bus = SessionBus()
loop = GLib.MainLoop()
airpods = system_bus.get("org.bluez", "/org/bluez/hci0/dev_14_87_6A_13_20_A2")
player = session_bus.get("org.mpris.MediaPlayer2.playerctld", "/org/mpris/MediaPlayer2")

was_playing = player.PlaybackStatus

def handler(address, state, idk):
	global was_playing

	logger.debug('%(address)s %(state)s %(idk)s', {
		'address': address,
		'state': state,
		'idk': idk,
	})

	if address == 'org.bluez.Device1':
		if 'Connected' in state and state['Connected'] == True:
			# FIXME
			time.sleep(0.5)
			airpods.Connect()

			logger.debug('Setting playerctld status: %s', was_playing)
			if was_playing == 'Playing':
				player.Play()

		if 'Connected' in state and state['Connected'] == False:
			was_playing = player.PlaybackStatus
			logger.debug('Saving playerctld status: %s', was_playing)

			player.Pause()

if __name__ == '__main__':
	airpods.PropertiesChanged.connect(handler)

	logger.debug('Starting main loop')
	try:
		loop.run()
	except KeyboardInterrupt:
		logger.debug('Exiting')
		loop.quit()
