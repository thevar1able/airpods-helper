#!/usr/bin/env python3

import sys
import logging
from gi.repository import GLib

from . import AirpodsConnectionManager, PlayercltdPlayerManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1]:
        logger.error('Please pass your Airpods MAC address as an argument')
        return 1

    mac_address = sys.argv[1]

    airpods_manager = AirpodsConnectionManager(mac_address)
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

    return 0


if __name__ == '__main__':
    sys.exit(main())
