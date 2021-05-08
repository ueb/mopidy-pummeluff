'''
Python module for the dedicated Mopidy Pummeluff threads.
'''

__all__ = (
    'GPIOHandler',
)

from threading import Thread
from logging import getLogger
import time

import RPi.GPIO as GPIO

from mopidy_pummeluff.actions import (
    Shutdown,
    PlayPause,
    Stop,
    PreviousTrack,
    NextTrack,
    IncreaseVolume,
    DecreaseVolume,
)
from mopidy_pummeluff.sound import play_sound

LOGGER = getLogger(__name__)


class GPIOHandler(Thread):
    '''
    Thread which handles the GPIO ports, which basically means activating the
    LED when it's started and then reacting to button presses.
    '''
    button_names = {
        'button_pin_shutdown': Shutdown,
        'button_pin_play_pause': PlayPause,
        'button_pin_stop': Stop,
        'button_pin_previous_track': PreviousTrack,
        'button_pin_next_track': NextTrack,
        'button_pin_increase_volume': IncreaseVolume,
        'button_pin_decrease_volume': DecreaseVolume,
    }

    led_pin = 8

    def __init__(self, config, core, stop_event):
        '''
        Class constructor.

        :param mopidy.config config: The configuration of this extension
        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super().__init__()

        self.core       = core
        self.stop_event = stop_event

        self.button_pins = {}
        for button_name, action in self.button_names.items():
            pin = config['pummeluff'][button_name]
            if pin is None:
                LOGGER.debug('%s is not configured', button_name)
                continue
            LOGGER.debug('%s is used for %s', pin, button_name)
            self.button_pins[pin] = action

        self.led_pins1 = [int(pin) for pin in config['pummeluff']['led_pins1']]
        self.led_pins2 = [int(pin) for pin in config['pummeluff']['led_pins2']]
        self.led_pins3 = [int(pin) for pin in config['pummeluff']['led_pins3']]

        now             = time.time()
        self.timestamps = {x: now for x in self.button_pins}

    # pylint: disable=no-member
    def run(self):
        '''
        Run the thread.
        '''
        if not self.button_pins and self.led_pin is None:
            LOGGER.debug('No gpio pin configured')
            return

        GPIO.setmode(GPIO.BOARD)

        for pin in self.button_pins:
            LOGGER.debug('Setup pin %s as button pin', pin)
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda pin: self.button_push(pin))  # pylint: disable=unnecessary-lambda

        for pin in self.led_pins1:
            LOGGER.debug('Setup pin %s as LED1 pin', pin)
            GPIO.setup(pin, GPIO.OUT)

        if self.led_pins2:
            time.sleep(1)
            for pin in self.led_pins2:
                LOGGER.debug('Setup pin %s as LED2 pin', pin)
                GPIO.setup(pin, GPIO.OUT)

        if self.led_pins3:
            time.sleep(1)
            for pin in self.led_pins3:
                LOGGER.debug('Setup pin %s as LED3 pin', pin)
                GPIO.setup(pin, GPIO.OUT)

        self.stop_event.wait()
        GPIO.cleanup()  # pylint: disable=no-member

    def button_push(self, pin):
        '''
        Callback method when a button is pushed.

        :param int pin: Pin number
        '''
        now    = time.time()
        before = self.timestamps[pin]

        if (GPIO.input(pin) == GPIO.LOW) and (now - before > 0.25):
            LOGGER.debug('Button at pin %s was pushed', pin)
            play_sound('success.wav')
            self.button_pins[pin].execute(self.core)
            self.timestamps[pin] = now
