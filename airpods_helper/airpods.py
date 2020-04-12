import logging
from typing import Optional, List, Set, Callable, Dict

from pydbus import SystemBus

logger = logging.getLogger(__name__)


class AirpodsConnectionManager:
    BUS_NAME: str = 'org.bluez'
    DEVICE_PATH_TEMPLATE: str = '/org/bluez/{device}/dev_{mac_address}'

    DEVICE_INTERFACE: str = 'org.bluez.Device1'
    DEVICE_INTERFACE_CONNECTED_PROPERTY_NAME: str = 'Connected'

    connect_event_handlers: Set[Callable] = set()
    disconnect_event_handlers: Set[Callable] = set()

    def __init__(self, mac_address: str, device: str = 'hci0'):
        system_bus = SystemBus()

        mac_address = mac_address.replace(':', '_').upper()

        self.airpods = system_bus.get(
            self.BUS_NAME,
            self.DEVICE_PATH_TEMPLATE.format(
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
        self.airpods.Connect()

    def signal_handler(self, interface_name: str, changed_properties: Dict[str, str],
                       invalidated_properties: List[str]):
        logger.debug('%(interface_name)s %(changed_properties)s %(invalidated_properties)s', {
            'interface_name': interface_name,
            'changed_properties': changed_properties,
            'invalidated_properties': invalidated_properties,
        })

        if interface_name != self.DEVICE_INTERFACE:
            return

        new_device_state = changed_properties.get(self.DEVICE_INTERFACE_CONNECTED_PROPERTY_NAME)
        if new_device_state is None:
            return

        handler_list = []

        if new_device_state is True:
            handler_list = self.connect_event_handlers

        if new_device_state is False:
            handler_list = self.disconnect_event_handlers

        [f() for f in handler_list]
