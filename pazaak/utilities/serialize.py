import abc
import enum

from pazaak.utilities.functions import is_from_type


class Serializable(metaclass=abc.ABCMeta):
    """
    Base class to represent an object that can be serialized and consumed by JsonResponse.
    Derived classes must implement the `.context()` method that returns a dictionary representing the object.
    The dictionary should consist only of JSON-compliant builtin Python types.
    Derived instances of this class should be serialized through the `serialize()` function in `pazaak.helpers.utilities`.
    """

    @abc.abstractmethod
    def context(self) -> dict:
        """
        Returns a raw dictionary representing the object.
        This will be passed into serialize().
        """
        pass

    def json(self) -> dict:
        context = self.context()
        return serialize(context)


class _SerializableEnumMeta(enum.EnumMeta, abc.ABCMeta):
    """
    Intermediate metaclass necessary for multiple inheritance with enums.
    """
    pass


class SerializableEnum(Serializable, enum.Enum, metaclass=_SerializableEnumMeta):

    @classmethod
    def should_export_to_js(cls) -> bool:
        """
        Override this to return True if the enum should be auto-exported as a JS class.
        See pazaak.enums.export_enums_to_js() for details.
        """
        return False

    def key(self) -> str:
        """
        Override this to return the value that this enum should use when it's the key in a dictionary.
        For example, if MyEnum.A = 1, then this default implementation when calling serialize() on {MyEnum.A: 'test'} results in {1: 'test'}.
        """
        return self.value

    def context(self) -> dict:
        return {
            'name': self.name,
            'value': self.value
        }


def serialize(payload):
    """
    Recursively serializes the keyword arguments into a payload that JsonResponse should be able to consume.
    Any object in the kwargs derived from Serializable will use their `.json()` method.
    Returns the serialized kwargs as a dictionary.
    """
    result = payload

    if is_from_type(payload, Serializable):
        result = payload.json()

    elif isinstance(payload, dict):
        result = {}
        for field, value in payload.items():
            if is_from_type(field, SerializableEnum):
                field = field.key()
            result[field] = serialize(value)

    elif isinstance(payload, list):
        result = [serialize(item) for item in payload]

    return result


if __name__ == '__main__':
    pass