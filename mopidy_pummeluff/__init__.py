'''
Mopidy Pummeluff Python module.
'''

import os

import mopidy

from .frontend import PummeluffFrontend
from .web import LatestHandler, RegistryHandler, RegisterHandler, UnregisterHandler, \
    ActionClassesHandler


def app_factory(config, core):  # pylint: disable=unused-argument
    '''
    App factory for the web apps.

    :param mopidy.config config: The mopidy config
    :param mopidy.core.Core: The mopidy core

    :return: The registered app request handlers
    :rtype: list
    '''
    return [
        ('/latest/', LatestHandler),
        ('/registry/', RegistryHandler),
        ('/register/', RegisterHandler),
        ('/unregister/', UnregisterHandler),
        ('/action-classes/', ActionClassesHandler),
    ]


class Extension(mopidy.ext.Extension):
    '''
    Mopidy Pummeluff extension.
    '''

    dist_name = 'Mopidy-Pummeluff'
    ext_name = 'pummeluff'

    def get_default_config(self):  # pylint: disable=no-self-use
        '''
        Return the default config.

        :return: The default config
        '''
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return mopidy.config.read(conf_file)

    def get_config_schema(self):
        '''
        Return the config schema.

        :return: The config schema
        '''
        schema = super().get_config_schema()
        schema["button_pin_shutdown"] = mopidy.config.Integer(optional=True, minimum=0, maximum=40)
        schema["button_pin_play_pause"] = mopidy.config.Integer(
            optional=True, minimum=0, maximum=40)
        schema["button_pin_stop"] = mopidy.config.Integer(optional=True, minimum=0, maximum=40)
        schema["button_pin_previous_track"] = mopidy.config.Integer(
            optional=True, minimum=0, maximum=40)
        schema["button_pin_next_track"] = mopidy.config.Integer(
            optional=True, minimum=0, maximum=40)
        schema["button_pin_increase_volume"] = mopidy.config.Integer(
            optional=True, minimum=0, maximum=100)
        schema["button_pin_decrease_volume"] = mopidy.config.Integer(
            optional=True, minimum=0, maximum=100)
        schema["led_pins1"] = mopidy.config.List(optional=True)
        schema["led_pins2"] = mopidy.config.List(optional=True)
        schema["led_pins3"] = mopidy.config.List(optional=True)
        schema["rfid_pin_rst"] = mopidy.config.Integer(optional=True, minimum=0, maximum=40)
        schema["rfid_pin_irq"] = mopidy.config.Integer(optional=True, minimum=0, maximum=40)

        return schema

    def setup(self, registry):
        '''
        Setup the extension.

        :param mopidy.ext.Registry: The mopidy registry
        '''
        registry.add('frontend', PummeluffFrontend)

        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'webui'),
        })

        registry.add('http:app', {
            'name': self.ext_name,
            'factory': app_factory,
        })
