#!/usr/bin/env python3

import logging
from gi.repository import GLib

from . import AirpodsConnectionManager, PlayercltdPlayerManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main() -> int:
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

    return 0


if __name__ == '__main__':
    sys.exit(main())
