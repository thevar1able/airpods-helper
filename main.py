#!/usr/bin/env python3

import time
import logging
from typing import Optional, List, Callable, Set, Dict

from pydbus import SystemBus, SessionBus
from gi.repository import GLib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AirpodsConnectionManager:
    BLUEZ_INTERFACE: str = 'org.bluez'
    BLUEZ_HCI_ADDRESS_TEMPLATE: str = '/org/bluez/{device}/dev_{mac_address}'

    BLUEZ_DEVICE_INTERFACE: str = 'org.bluez.Device1'
    BLUEZ_DEVICE_EVENT_STATE_KEY: str = 'Connected'

    connect_event_handlers: Set[Callable] = set()
    disconnect_event_handlers: Set[Callable] = set()

    def __init__(self, mac_address: str, device: str = 'hci0'):
        system_bus = SystemBus()

        mac_address = mac_address.replace(':', '_').upper()

        self.airpods = system_bus.get(
            self.BLUEZ_INTERFACE,
            self.BLUEZ_HCI_ADDRESS_TEMPLATE.format(
                device=device,
                mac_address=mac_address,
            ))

        self.connect_event_handlers.add(self.connect_handler)
        self.airpods.PropertiesChanged.connect(self.signal_handler)

    def subscribe(self, on_connect: Optional[List[Callable]] = None, on_disconnect: Optional[List[Callable]] = None):
        if on_connect is None:
            on_connect = []
        if on_disconnect is None:
            on_disconnect = []

        self.connect_event_handlers.update(on_connect)
        self.disconnect_event_handlers.update(on_disconnect)

    def connect_handler(self):
        # FIXME
        time.sleep(0.5)
        self.airpods.Connect()

    def signal_handler(self, interface_name: str, changed_properties: Dict[str, str],
                       invalidated_properties: List[str]):
        logger.debug('%(interface_name)s %(changed_properties)s %(invalidated_properties)s', {
            'interface_name': interface_name,
            'changed_properties': changed_properties,
            'invalidated_properties': invalidated_properties,
        })

        if interface_name != self.BLUEZ_DEVICE_INTERFACE:
            return

        new_device_state = changed_properties.get(self.BLUEZ_DEVICE_EVENT_STATE_KEY)
        if new_device_state is None:
            return

        handler_list = []

        if new_device_state is True:
            handler_list = self.connect_event_handlers

        if new_device_state is False:
            handler_list = self.disconnect_event_handlers

        [f() for f in handler_list]


class PlayercltdPlayerManager:
    PLAYERCTL_INTERFACE = 'org.mpris.MediaPlayer2.playerctld'
    MEDIA_PLAYER_ADDRESS = '/org/mpris/MediaPlayer2'

    def __init__(self):
        session_bus = SessionBus()

        self.player = session_bus.get(
            self.PLAYERCTL_INTERFACE,
            self.MEDIA_PLAYER_ADDRESS,
        )

        self.was_playing = self.player.PlaybackStatus

    def on_connect(self):
        logger.debug('Setting playerctld status: %s', self.was_playing)
        if self.was_playing == 'Playing':
            self.player.Play()

    def on_disconnect(self):
        self.was_playing = self.player.PlaybackStatus
        logger.debug('Saving playerctld status: %s', self.was_playing)

        self.player.Pause()


if __name__ == '__main__':
    airpods_manager = AirpodsConnectionManager('14:87:6A:13:20:A2')
    playerctld_manager = PlayercltdPlayerManager()

    airpods_manager.subscribe(
        on_connect=[playerctld_manager.on_connect],
        on_disconnect=[playerctld_manager.on_disconnect],
    )

    loop = GLib.MainLoop()
    logger.debug('Starting main loop')
    try:
        loop.run()
    except KeyboardInterrupt:
        logger.debug('Exiting')
        loop.quit()
