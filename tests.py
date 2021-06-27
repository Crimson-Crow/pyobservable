import unittest
from types import MethodType
from unittest.mock import Mock, sentinel, NonCallableMock

from pyobservable import Observable


class EventDispatchTest(unittest.TestCase):

    def test_bind_function(self):
        event_key = 'key'
        args = (sentinel,)
        kwargs = {'keyword': sentinel}
        observable = Observable()
        observable.add_event(event_key)

        handler = Mock()
        observable.bind(event_key, handler)
        observable.notify(event_key, *args, **kwargs)
        handler.assert_called_once_with(*args, **kwargs)

    def test_bind_method(self):
        event_key = 'key'
        args = (sentinel,)
        kwargs = {'keyword': sentinel}
        observable = Observable()
        observable.add_event(event_key)

        class Observer:
            pass

        observer = Observer()
        handler = Mock()
        observer.callback = MethodType(handler, observer)
        handler.__name__ = 'callback'

        observable.bind(event_key, observer.callback)
        observable.notify(event_key, *args, **kwargs)
        handler.assert_called_once_with(observer, *args, **kwargs)

    def test_inheritance(self):
        event_keys = [1, 'key', 2, 'foo']
        args = (sentinel,)
        kwargs = {'keyword': sentinel}

        class Base(Observable):
            _events_ = event_keys

        base = Base()

        handler = Mock()
        for key in event_keys:
            base.bind(key, handler)

        for key in event_keys:
            base.notify(key, *args, **kwargs)
            handler.assert_called_with(*args, **kwargs)

        self.assertEqual(handler.call_count, len(event_keys))

    def test_multiinheritance(self):
        base_event_keys = []
        child1_event_keys = []
        child2_event_keys = []
        multichild_event_keys = []
        event_keys = set()
        event_keys.update(base_event_keys, child1_event_keys, child2_event_keys, multichild_event_keys)

        class Base(Observable):
            _events_ = base_event_keys

        class Child1(Base):
            _events_ = child1_event_keys

        class Child2(Base):
            _events_ = child2_event_keys

        class MultiChild(Child1, Child2):
            _events_ = multichild_event_keys

        multichild = MultiChild()

        self.assertEqual(multichild._event_mapping.keys(), event_keys)

    def test_decorator_bind(self):
        event_key = 'key'
        args = (sentinel,)
        kwargs = {'keyword': sentinel}
        observable = Observable()
        observable.add_event(event_key)

        handler = Mock()

        @observable.bind(event_key)
        def callback(*args, **kwargs):
            handler(*args, **kwargs)

        observable.notify(event_key, *args, **kwargs)
        handler.assert_called_once_with(*args, **kwargs)

    def test_unbind(self):
        event_key = 'key'
        args = (sentinel,)
        kwargs = {'keyword': sentinel}
        observable = Observable()
        observable.add_event(event_key)

        handler = Mock()
        observable.bind(event_key, handler)
        observable.unbind(event_key, handler)
        observable.notify(event_key, *args, **kwargs)
        handler.assert_not_called()

    def test_unbind_all(self):
        event_key = 'key'
        args = (sentinel,)
        kwargs = {'keyword': sentinel}
        observable = Observable()
        observable.add_event(event_key)

        handler = Mock()
        observable.bind(event_key, handler)
        observable.unbind_all()
        observable.notify(event_key, *args, **kwargs)
        handler.assert_not_called()

    def test_non_callable(self):
        event_key = 'key'
        observable = Observable()
        observable.add_event(event_key)

        handler = NonCallableMock()
        self.assertRaises(TypeError, observable.bind, event_key, handler)

    def test_non_existent_event(self):
        observable = Observable()

        handler = Mock()
        self.assertRaises(ValueError, observable.bind, 'foo', handler)
        self.assertRaises(ValueError, observable.unbind, 'foo', handler)

    def test_non_existent_handler(self):
        event_key = 'key'
        observable = Observable()
        observable.add_event(event_key)

        handler = Mock()
        self.assertRaises(ValueError, observable.unbind, event_key, handler)


if __name__ == '__main__':
    unittest.main()
