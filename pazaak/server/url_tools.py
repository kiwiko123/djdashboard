import abc
import inspect
import re

from django.conf.urls import url


class AutoParseableViewURL(metaclass=abc.ABCMeta):
    """
    Base class to simplify Django URL setup.
    Implementing the url() class method allows the function url_patterns to be called in the top-level urls.py.
    """
    _url_name_pattern = re.compile('\^((?P<name>[^/]+)/)+\$')

    @classmethod
    @abc.abstractmethod
    def url(cls) -> str:
        """
        Implement this by returning the endpoint URL of this view.
        Example:
         return '/api/test/my-endpoint'
        """
        pass

    @classmethod
    def regex_url(cls) -> str:
        """
        Returns the formatted regular expression URL required by Django's url() function.
        Do not override this.
        """
        url = cls.url()
        url = url.strip().lower()
        if url.startswith('/'):
            url = url[1:]
        if not url.endswith('/'):
            url += '/'

        return '^{0}$'.format(url)

    @classmethod
    def name(cls) -> str:
        """
        Returns the final portion of the url() endpoint string.
        Example: if url() returns 'api/test/my-endpoint', returns 'my-endpoint'.
        Do not override this.
        """
        url = cls.regex_url()
        match = cls._url_name_pattern.match(url)
        if not match:
            raise ValueError('failed to auto-parse endpoint name')
        return match.group('name')



def url_patterns(module, predicate: callable) -> [url]:
    """
    Scans module for classes derived from AutoParseableViewURL that have implemented the @classmethod url().
    Returns an auto-generated list of Django URL patterns required by the app's top-level urls.py.
    Call this method on the views module (views.py).
    """
    return [url(cls.regex_url(), cls.as_view(), name=cls.name()) for _, cls in inspect.getmembers(module, predicate=predicate)]


def client_url() -> str:
    return 'http://localhost:3000'


if __name__ == '__main__':
    pass