import logging

from pydbus import SessionBus

logger = logging.getLogger(__name__)


class PlayercltdPlayerManager:
    PLAYERCTLD_BUS = 'org.mpris.MediaPlayer2.playerctld'
    MEDIA_PLAYER_PATH = '/org/mpris/MediaPlayer2'

    def __init__(self):
        session_bus = SessionBus()

        self.player = session_bus.get(
            self.PLAYERCTLD_BUS,
            self.MEDIA_PLAYER_PATH,
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
