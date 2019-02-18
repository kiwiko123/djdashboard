import abc


class Serializable(metaclass=abc.ABCMeta):
    """
    Base class to represent an object that can be serialized and consumed by JsonResponse.
    Derived classes must implement a `.json()` method that returns a dictionary representing the object.
    The dictionary should consist only of JSON-compliant builtin Python types.
    Derived instances of this class should be serialized through the `serialize()` function in `pazaak.helpers.utilities`.
    """

    @abc.abstractmethod
    def json(self) -> dict:
        pass
