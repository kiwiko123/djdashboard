import abc
import enum


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


def serialize(payload) -> dict:
    """
    Recursively serializes the keyword arguments into a payload that JsonResponse should be able to consume.
    Any object in the kwargs derived from Serializable will use their `.json()` method.
    Returns the serialized kwargs as a dictionary.
    """
    if isinstance(payload, dict):
        for field, value in payload.items():
            if isinstance(field, SerializableEnum):
                del payload[field]
                field = field.key()
            payload[field] = serialize(value)

    elif isinstance(payload, list):
        payload = [serialize(item) for item in payload]

    elif isinstance(payload, Serializable):
        payload = payload.json()

    return payload