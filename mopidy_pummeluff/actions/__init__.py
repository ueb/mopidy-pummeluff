'''
Python module for Mopidy Pummeluff tags.
'''

__all__ = (
    'PlayPause',
    'Stop',
    'PreviousTrack',
    'NextTrack',
    'Shutdown',
    'Tracklist',
    'Volume',
    'IncreaseVolume',
    'DecreaseVolume',
)

from .playback import PlayPause, Stop, PreviousTrack, NextTrack
from .shutdown import Shutdown
from .tracklist import Tracklist
from .volume import Volume, DecreaseVolume, IncreaseVolume

ACTIONS = {}
for action in __all__:
    ACTIONS[action] = globals()[action].__doc__.strip()
