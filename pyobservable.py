from collections.abc import Hashable
from types import MethodType
from typing import Callable, Optional, Tuple, Any, Dict, Union, TypeVar
from weakref import WeakValueDictionary

EventHandlerMapping = WeakValueDictionary
Handler = TypeVar('Handler', bound=Callable)


class Observable:
    __slots__ = '_event_mapping',

    def __new__(cls, *args, **kwargs):
        instance = super(Observable, cls).__new__(cls)
        instance._event_mapping = {event: EventHandlerMapping() for c in cls.__mro__ for event in
                                   getattr(c, '_events_', [])}
        return instance

    def __init__(self):
        self._event_mapping: Dict[Hashable, EventHandlerMapping]

    def add_event(self, event_key: Hashable) -> None:
        """"Adds an event to the list of possible events."""
        self._event_mapping[event_key] = EventHandlerMapping()

    def bind(self, event_key: Hashable, handler: Optional[Handler] = None) -> Union[Callable, Handler]:
        """Binds a handler function to the specified event. When handler is None, decorator usage is assumed."""
        event_handlers = self._get_handler_mapping(event_key)

        def bind(callback: Handler) -> Handler:
            if not callable(callback):
                raise TypeError('The provided object is not callable.')
            k, v = self._compute_kv(callback)
            event_handlers[k] = v
            return callback

        return bind if handler is None else bind(handler)

    def unbind(self, event_key: Hashable, handler: Handler) -> None:
        """Removes the provided event handlers from the specified event."""
        event_handlers = self._get_handler_mapping(event_key)
        k = self._compute_kv(handler)[0]
        try:
            del event_handlers[k]
        except KeyError:
            raise ValueError(f'Handler was not found in event key {event_key!r}')

    def unbind_all(self) -> None:
        """Clears all event handlers from all events."""
        for event_handlers in self._event_mapping.values():
            event_handlers.clear()

    def notify(self, event_key: Hashable, *args, **kwargs) -> None:
        """Calls all bound event handlers with the entered arguments. Compatibility between the arguments and the
        handler's function signature is not enforced."""
        for k, v in self._get_handler_mapping(event_key).items():
            func_name = k[0]
            (v if func_name is None else getattr(v, func_name))(*args, **kwargs)

    def _get_handler_mapping(self, event_key: Hashable) -> EventHandlerMapping:
        try:
            return self._event_mapping[event_key]
        except KeyError:
            raise ValueError(f'No such event key {event_key!r}')

    @staticmethod
    def _compute_kv(obj: Any) -> Tuple[Tuple[Optional[str], int], Any]:
        if isinstance(obj, MethodType):
            return (obj.__func__.__name__, id(obj.__self__)), obj.__self__
        else:
            return (None, id(obj)), obj
