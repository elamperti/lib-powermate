#!/usr/bin/env python

'''
    Library to handle Griffin Powermate events
    Copyright (C) 2017 Enrico Lamperti

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

from evdev import InputDevice, ecodes, list_devices
import logging
import errno


class PowerMateWheel():
    def __init__(self, device):
        self.__device = device
        self.__logger = logging.getLogger('lib-powermate')

        self.__wheel_pressed = False
        self.__ignore_multiple_twists = False
        self.__has_twisted = False
        self.__ignore_all_events = False

        # Functions to be called
        self._press = self.__dummy_call
        self._depress = self.__dummy_call
        self._turn_left = self.__dummy_call
        self._turn_right = self.__dummy_call
        self._twist_left = self.__dummy_call
        self._twist_right = self.__dummy_call

    @staticmethod
    def __dummy_call(*args):
        pass

    def ignore_all_events(self, value=True):
        self.__ignore_all_events = value

    def ignore_multiple_twists(self, value=True):
        self.__ignore_multiple_twists = value

    def get_device(self):
        return self.__device

    def is_pressed(self):
        return self.__wheel_pressed

    def has_twisted(self):
        return self.__has_twisted

    def set_logger(self, new_logger):
        self.__logger = new_logger

    def on(self, event_name, your_function):
        if not callable(your_function):
            raise TypeError('Expected a callable')

        if event_name == 'press':
            self._press = your_function
        elif event_name == 'depress' or event_name == 'release':
            self._depress = your_function
        elif event_name == 'turn_left':
            self._turn_left = your_function
        elif event_name == 'turn_right':
            self._turn_right = your_function
        elif event_name == 'twist_left':
            self._twist_left = your_function
        elif event_name == 'twist_right':
            self._twist_right = your_function
        else:
            raise NameError('Event %s not implemented' % event_name)

    def listen(self):
        self.__logger.info('Listening on device %s' % self.__device)
        try:
            for event in InputDevice(self.__device).read_loop():
                # ignore synchronization events
                if self.__ignore_all_events or event.type == ecodes.EV_SYN:
                    continue

                self.__logger.debug('Processing event: ' + str(event))

                # button event
                if event.type == ecodes.EV_KEY:
                    if event.value == 0:
                        self.__wheel_pressed = False
                        self._depress()
                        self.__has_twisted = False
                    else:
                        self.__wheel_pressed = True
                        self._press()

                # turn/twist event
                elif event.type == ecodes.EV_REL:
                    if event.value > 0:
                        if self.is_pressed():
                            if not self.__has_twisted:
                                self._twist_right(abs(event.value))
                                if self.__ignore_multiple_twists:
                                    self.__has_twisted = True
                        else:
                            self._turn_right(abs(event.value))
                    else:
                        if self.is_pressed():
                            if not self.__has_twisted:
                                self._twist_left(abs(event.value))
                                if self.__ignore_multiple_twists:
                                    self.__has_twisted = True
                        else:
                            self._turn_left(abs(event.value))

        except IOError, e:
            if e.errno == errno.ENODEV:
                self.__logger.error('Device unplugged')
                raise IOError('Device not found')
            else:
                self.__logger.error(e.message)
                raise e

        except (KeyboardInterrupt, SystemExit):
            self.__logger.info('Listen aborted on device %s' % self.__device)

        except Exception as e:
            self.__logger.debug('Error: %s' % e)
            raise e


class DeviceNotFound(Exception):
    pass


def find_wheels():
    devices = [InputDevice(fn) for fn in list_devices()]
    wheels = []

    for device in devices:
        if device.name.find('PowerMate') != -1:
            # print ('Device found: ' + device.name + ' (' + device.phys + ')')
            wheels.append(device.fn)

    if len(wheels) == 0:
        raise DeviceNotFound

    return wheels


# Test powermate wheel if library is executed directly
if __name__ == "__main__":
    # Attempt to find a powermate wheel
    try:
        device = find_wheels()
    except DeviceNotFound:
        print("Device not found")

    # Use the first one, as this is just for testing purposes
    my_wheel = PowerMateWheel(device[0])

    # Simple function to print a message on each event
    def print_message(message):
        def dumb_echo(*args):
            print(message)
        return dumb_echo

    # Init variable for the following function
    use_multiple_twists = False

    # Toggle multiple twists on unpress
    def toggle_multitwist():
        print('Wheel unpressed')
        global use_multiple_twists
        if not my_wheel.has_twisted():
            use_multiple_twists = not use_multiple_twists
            my_wheel.ignore_multiple_twists(use_multiple_twists)
            print('Ignore multiple twists: %s' % use_multiple_twists)

    # Add event handlers
    my_wheel.on('press', print_message('Wheel pressed'))
    my_wheel.on('depress', toggle_multitwist)
    my_wheel.on('turn_left', print_message('Wheel turned left'))
    my_wheel.on('turn_right', print_message('Wheel turned right'))
    my_wheel.on('twist_left', print_message('Wheel twisted left'))
    my_wheel.on('twist_right', print_message('Wheel twisted right'))

    # Start listening
    my_wheel.listen()
