import abc


class Serializable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def json(self) -> dict:
        pass


def serialize(**payload) -> dict:
    for field, value in payload.items():
        if isinstance(value, Serializable):
            payload[field] = value.json()

    return payload