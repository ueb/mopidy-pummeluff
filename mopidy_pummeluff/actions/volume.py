'''
Python module for Mopidy Pummeluff volume tag.
'''

__all__ = (
    'Volume',
    'IncreaseVolume',
    'DecreaseVolume'
)

from logging import getLogger

from .base import Action

LOGGER = getLogger(__name__)


class VolumeBase(Action):
    '''
    Provide common validation for all volume Actions.
    '''
    
    def validate(self):
        '''
        Validates if the parameter is an integer between 0 and 100.

        :param mixed parameter: The parameter

        :raises ValueError: When parameter is invalid
        '''
        super().validate()

        try:
            number = int(self.parameter)
            assert 0 <= number <= 100
        except (ValueError, AssertionError):
            raise ValueError('Volume parameter has to be a number between 0 and 100')
    

class Volume(VolumeBase):
    '''
    Sets the volume to the percentage value retreived from the tag's parameter.
    '''

    @classmethod
    def execute(cls, core, volume):  # pylint: disable=arguments-differ
        '''
        Set volume of the mixer.

        :param mopidy.core.Core core: The mopidy core instance
        :param volume: The new (percentage) volume
        :type volume: int|str
        '''
        LOGGER.info('Setting volume to %s', volume)
        try:
            core.mixer.set_volume(int(volume))
        except ValueError as ex:
            LOGGER.error(str(ex))
            
            
class IncreaseVolume(VolumeBase):
    '''
    Increases the volume by the percentage value retreived from the tag's parameter.
    '''

    @classmethod
    def execute(cls, core, volume=5):  # pylint: disable=arguments-differ
        '''
        Set volume of the mixer.

        :param mopidy.core.Core core: The mopidy core instance
        :param volume: The percentage the volume is increased
        :type volume: int|str
        '''
        try:
            currentVolume = core.mixer.get_volume().get()
            newVolume = currentVolume + int(volume)
            newVolume = min(newVolume, 100)
            core.mixer.set_volume(newVolume)
            LOGGER.info('Increase volume from %i to %i', currentVolume, newVolume)        
        except ValueError as ex:
            LOGGER.error(str(ex))


class DecreaseVolume(VolumeBase):
    '''
    Decreases the volume by the percentage value retreived from the tag's parameter.
    '''

    @classmethod
    def execute(cls, core, volume=5):  # pylint: disable=arguments-differ
        '''
        Set volume of the mixer.

        :param mopidy.core.Core core: The mopidy core instance
        :param volume: The percentage the volume is decreased
        :type volume: int|str
        '''
        try:
            currentVolume = core.mixer.get_volume().get()
            newVolume = currentVolume - int(volume)
            newVolume = max(newVolume, 0)
            core.mixer.set_volume(newVolume)
            LOGGER.info('Decrease volume from %i to %i', currentVolume, newVolume)        
        except ValueError as ex:
            LOGGER.error(str(ex))

