import abc
import enum
import inspect
import pathlib
import sys


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


class EnumSerializer:

    def __init__(self, path_to_write_file: str) -> None:
        """
        Override this method to return the relative path to the file that should be written,
        starting at the project's base directory.
        """
        self._path_to_write_file = path_to_write_file

    def export(self) -> None:
        path_to_write_file = self._path_to_write_file
        write_file = pathlib.Path(path_to_write_file)
        _export_enums_to_js(write_file)


def serialize(payload):
    """
    Recursively serializes the keyword arguments into a payload that JsonResponse should be able to consume.
    Any object in the kwargs derived from Serializable will use their `.json()` method.
    Returns the serialized kwargs as a dictionary.
    """
    result = payload
    payload_type = type(payload)

    if isinstance(payload, Serializable) or issubclass(payload_type, Serializable):
        result = payload.json()

    elif isinstance(payload, dict):
        result = {}
        for field, value in payload.items():
            if isinstance(field, SerializableEnum):
                field = field.key()
            result[field] = serialize(value)

    elif isinstance(payload, list):
        result = [serialize(item) for item in payload]

    return result


def _export_enums_to_js(write_file: pathlib.Path):
    """
    Automatically generate a JS class representing enums in this module.
    Generated enums must be derived from SerializableEnum,
    and must override the @classmethod should_export_to_js() to return True.

    Generation happens at server startup, in pazaak/apps.py.
    """
    enums_to_serialize = _get_classes_in_current_module(_should_serialize_to_js)
    with write_file.open('w') as outfile:
        header = [
            '// =========================',
            '// || AUTO-GENERATED FILE ||',
            '// ========================='
        ]

        outfile.write('\n'.join(header))
        outfile.write('\n\n')

        for enum_class in enums_to_serialize:
            _write_enum_as_js_class(enum_class, outfile)
            outfile.write('\n')


def _write_enum_as_js_class(cls: SerializableEnum, outfile: open) -> None:
    enum_name = cls.__name__
    if not cls.should_export_to_js():
        raise ValueError('override should_export_to_js() to return True'.format(enum_name))

    indentation = '    '
    body = ['{0}{1}: {2},'.format(indentation, e.name, _transform_enum_value(e)) for e in cls]
    lines = ['export const {0} = {{'.format(enum_name)] + body + ['};']
    for line in lines:
        outfile.write('{0}\n'.format(line))


def _should_serialize_to_js(member) -> bool:
    return member is not SerializableEnum \
       and issubclass(member, SerializableEnum) \
       and member.should_export_to_js()


def _transform_enum_value(enum_value: enum.Enum):
    """
    If the enum's value is a string, include quotes around it.
    """
    value = enum_value.value
    if type(value) is str:
        value = "'{0}'".format(value)
    return value


def _get_classes_in_current_module(predicate: callable) -> list:
    if __name__ not in sys.modules:
        raise ValueError("Couldn't find '{0}' in {1}".format(__name__, sys.modules))

    current_module = sys.modules[__name__]
    return [cls for _, cls in inspect.getmembers(current_module, lambda member: inspect.isclass(member) and predicate(member))]



if __name__ == '__main__':
    pass