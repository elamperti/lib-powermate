# :control_knobs: lib-powermate 

This Python library is intended to handle Griffin Powermate wheel(s) events.

## Index

  * [Installation](#installation)
  * [Library documentation](#documentation)
    * [Functions](#functions)
    * [PowerMateWheel class](#powermatewheel-class)
      * [Getters and setters](#getters-and-setters)
        * [Getters](#getters)
        * [Setters](#setters)
      * [Methods](#methods)
      * [Events](#events)
  * [License](#license)
    
---

## Installation

```sh
pip install lib-powermate
```

## Usage
\[To be explained\]

---

# Documentation

## Functions
  * **`find_wheels()`**
    
    Returns an array of PowerMate wheel devices. Raises a `DeviceNotFound` exception if none found.

## PowerMateWheel class
Receives an evdev device as parameter, which can be obtained with the `find_wheels()` function.

### Getters and setters

#### Getters
  * **`get_device()`**
    
    Returns the current instance's device.
    
  * **`is_pressed()`**
    
    `True` if the wheel is currently pressed.
    
  * **`has_twisted()`**
    
    `True` if the current instance is ignoring multiple twists (see `ignore_multiple_twists` method) and the wheel has been pressed, then turned.

#### Setters
  * **`set_logger`**`(<logger new_logger>)`
    
    Changes the logger used by the current instance. Mostly useful for debugging purposes.

### Methods
  * **`ignore_all_events`**`([<bool value=True>])`
    
    Skips all events if True.
  
  * **`ignore_mutiple_twists`**`([<bool value=True>])`
    
    Ignores twist events (in any direction) after the first one until the wheel is unpressed. Useful for discrete operations.
    
  * **`on`**`(<str event_name>, <callable some_function>)`
    
    Define which function (or any other callable) to call when an even occurs. See *Events* for a list of events.
    
  * **`listen()`**
    
    Starts listening for events.

### Events
  * **`press`**: Triggered when the wheel is pressed down.
  * **`depress`**: Triggered when the wheel is unpressed/released. (Alias: `release`)
  * **`turn_left`**: Triggered when the wheel is turned to the left (counter-clockwise).
  * **`turn_right`**: Triggered when the wheel is turned to the right (clockwise).
  * **`twist_left`**: Triggered when the wheel is turned to the left (counter-clockwise) while being pressed down.
  * **`twist_right`**: Triggered when the wheel is turned to the right (clockwise) while being pressed down.

---

## License
GNU GPLv2 - Copyright 2017, Enrico Lamperti.

Please see [LICENSE](./LICENSE) file for more details.
