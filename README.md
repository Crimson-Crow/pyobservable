pyobservable
==========

[![PyPI](https://img.shields.io/pypi/v/pyobservable)](https://pypi.org/project/pyobservable/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyobservable)](https://pypi.org/project/pyobservable/)
[![Lines of code](https://img.shields.io/tokei/lines/github/Crimson-Crow/pyobservable)](https://github.com/Crimson-Crow/pyobservable)
[![GitHub](https://img.shields.io/github/license/Crimson-Crow/pyobservable)]((https://github.com/Crimson-Crow/pyobservable/blob/main/LICENSE.txt))

Description
-----------

`pyobservable` provides a simple event system for Python with weak reference support.
This ensures that the event handlers do not stay in memory when they aren't needed anymore. 

Installation
------------

`pyobservable` can be installed using [`pip`](http://www.pip-installer.org/):

    $ pip install pyobservable

Alternatively, you can download the repository and run the following command from within the source directory:

    $ python setup.py install

Usage
-----

For a quick start, a minimal example is:

```python
from pyobservable import Observable


obs = Observable()
obs.add_event('foo')
obs.add_event('bar')

# Event keys can be any object that is hashable
event = object()
obs.add_event(event)


# Binding with decorator usage
@obs.bind('foo')
def foo_handler(foo_number):
    print('foo_handler called:', foo_number)


# Binding with function usage
def bar_handler(bar_list):
    print('bar_handler called:', bar_list)
obs.bind('bar', bar_handler)


obs.notify('foo', 1)
obs.notify('bar', [1, 2, 3])
```

The rationale behind the requirement to add events before binding to them is to ensure the code is less error-prone from mistyping event names.
Also, if a duplicated event key is present, `ValueError` will be raised.\
However, the next example shows that event registration can be simplified using the special `_events_` attribute:

```python
from pyobservable import Observable


class EventEmitter(Observable):
    _events_ = ['foo', 2]
    
    def triggers_foo(self):
        self.notify('foo', 1, 2, 3)


event_emitter = EventEmitter()        


@event_emitter.bind('foo')
def foo_handler(*args):
    print(*args)


event_emitter.triggers_foo()
```
Also note that `_events_` can be defined multiple times in an inheritance tree.
`Observable` scans the MRO for this attribute and adds every event it finds.
Again, a `ValueError` will be raised if a duplicate event key is present. 

Finally, here's an advanced and clean example using [`enum`](https://docs.python.org/3/library/enum.html):

```python
from enum import Enum, auto
from pyobservable import Observable


class EventType(Enum):
    FOO = auto()
    BAR = auto()

class EventEmitter(Observable):
    _events_ = EventType  # Enums are iterable

    def triggers_foo(self):
        self.notify(EventType.FOO, 'foo happened!')


class EventListener:
    def on_foo(self, message):
        print("Here's a message from foo:", message)


event_emitter = EventEmitter()
event_listener = EventListener()
event_emitter.bind(EventType.FOO, event_listener.on_foo)  # pyobservable also supports bound methods


event_emitter.triggers_foo()
```

For more information, please refer to the `Observable` class docstrings.

Tests
-----

The simplest way to run tests:

    $ python tests.py

As a more robust alternative, you can install [`tox`](https://tox.readthedocs.io/en/latest/install.html) (or [`tox-conda`](https://github.com/tox-dev/tox-conda) if you use [`conda`](https://docs.conda.io/en/latest/)) to automatically support testing across the supported python versions, then run:

    $ tox

Issue tracker
-------------

Please report any bugs and enhancement ideas using the [issue tracker](https://github.com/Crimson-Crow/pyobservable/issues).

License
-------

`pyobservable` is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT) (see [LICENSE.txt](https://github.com/Crimson-Crow/pyobservable/blob/main/LICENSE.txt) for more information).