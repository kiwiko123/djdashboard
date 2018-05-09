import random

try:
    import Crypto.Cipher
    import Crypto.Random
except ImportError as e:
    e.args = ("module 'encryption' requires pycrypto - install with 'pip3 install pycrypto'",)
    raise


class DecryptionError(Exception):
    pass

class PasswordEncryptor:
    """ 
    Utility class for performing standard 2-way AES encryption on text (e.g., passwords).
    @classmethods provide quick and simple encryption/decryption using a default key.
    Or, more securely, initialize an object to use a custom key.
    """
    _alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789_-=+!@#$%^&*()'
    __encoding = 'utf-8'
    _ckey = bytes('fah82bF4CodQvGhf'[:16], encoding=__encoding)
    _civ = b'\x1aKas88\x04W\xeef\x0e-\xb4lm3'

    @staticmethod
    def _generate_cipher(key: bytes, iv: bytes) -> Crypto.Cipher.AES:
        """
        Returns a Crypto.Cipher.AES object using key and iv.
        A Cipher object using the same key/initialization vector CANNOT be used to decrypt the same message;
        i.e., you must create 2 objects - one to encrypt, and the other to decrypt.
        """
        return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)

    @classmethod
    def generate_string(cls, size=Crypto.Cipher.AES.block_size, alphabet=None) -> str:
        """
        Generates and returns a random (plaintext) string of length 'size'.
        'alphabet' is a string of characters to pull from.
        By default, 'alphabet' consists of 26 letters, 10 digits, and several symbol-like characters.
        """
        if alphabet is None:
            alphabet = cls._alphabet
        alphabet_size = len(alphabet)
        result = ''
        for i in range(size):
            c = alphabet[random.randrange(alphabet_size)]
            result += c.lower() if random.randrange(2) else c.upper()

        return result

    @classmethod
    def generate_iv(cls) -> bytes:
        """
        Generates and returns a random initialization vector of size 16.
        """
        return Crypto.Random.new().read(Crypto.Cipher.AES.block_size)

    @classmethod
    def default_key(cls, decode=True) -> str or bytes:
        """
        Returns the default key of the class.
        If decode=True, returns the decoded key as a string.
        Otherwise, returns the key as bytes.
        """
        result = cls._ckey
        return result.decode(encoding=cls.__encoding) if decode else result

    @classmethod
    def default_iv(cls) -> bytes:
        """
        Returns the default initialization vector of the class.
        """
        return cls._civ

    @classmethod
    def default_encoding(cls) -> str:
        """
        Returns the default encoding of the class.
        """
        return cls.__encoding

    @classmethod
    def set_default_encoding(cls, new_encoding: str) -> None:
        """
        Override the default encoding (utf-8) used to encrypt/decrypt content.
        """
        cls.__encoding = new_encoding

    @classmethod
    def c_encrypt(cls, plaintext: str) -> bytes:
        """
        Performs AES encryption on plaintext,
        returning the cipher-text data in bytes.
        Uses the default key and initialization vector for convenience (over added security).
        """
        encryptor = cls(key='default', iv='default', encoding=cls.default_encoding())
        return encryptor.encrypt(plaintext)

    @classmethod
    def c_decrypt(cls, encrypted: bytes) -> str:
        """
        Decrypts the encrypted-text argument, returning it in plain text.
        Uses the default key and initialization vector for convenience (over added security).
        """
        encryptor = cls(key='default', iv='default', encoding=cls.default_encoding())
        return encryptor.decrypt(encrypted)


    def __init__(self, key=None, iv=None, encoding='utf-8'):
        """ 
        Initialize a new PasswordEncryptor object.
        If {key,iv}='default', use the default class values;
        else if {key,iv}=None, randomly generate one.
        Raises TypeError if key is not a string, or iv is not bytes.
        Raises ValueError if key is not length 16.
        Default encoding is utf-8.

        Instance methods function the same as their class counterparts;
        see the class method docstrings for clarification.
        """
        self._encoding = encoding
        self._key = None
        self._iv = None

        if key == 'default':
            key = self.default_key()
        elif key is None:
            key = self.generate_string(Crypto.Cipher.AES.block_size)

        if iv == 'default':
            iv = self.default_iv()
        elif iv is None:
            iv = self.generate_iv()

        self.key = key
        self.iv = iv

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, new_encoding: str) -> None:
        self._encoding = new_encoding

    @property
    def key(self) -> bytes:
        return self._key

    @key.setter
    def key(self, new_key: str or bytes) -> None:
        if type(new_key) is str:
            if len(new_key) != Crypto.Cipher.AES.block_size:
                raise ValueError('AES encryption requires a length-{0} string as a key'.format(Crypto.Cipher.AES.block_size))
            self._key = bytes(new_key, self.encoding)
        elif type(new_key) is bytes:
            self.key = new_key.decode(encoding=self.encoding)
        else:
            raise TypeError('key must be a string or bytes; instead received {0}'.format(type(new_key)))

    @property
    def iv(self) -> bytes:
        return self._iv

    @iv.setter
    def iv(self, new_iv: bytes) -> None:
        if type(new_iv) is not bytes:
            raise TypeError('initialization vector must be a bytes object; instead received {0}'.format(type(new_iv)))
        self._iv = new_iv

    def encrypt(self, plaintext: str) -> bytes:
        cipher = self._generate_cipher(self.key, self.iv)
        return cipher.encrypt(bytes(plaintext, self.encoding))

    def decrypt(self, encrypted: bytes) -> str:
        cipher = self._generate_cipher(self.key, self.iv)
        decrypted = cipher.decrypt(encrypted)

        try:
            return decrypted.decode(encoding=self.encoding)
        except UnicodeDecodeError:
            raise DecryptionError('failed to decrypt string; perhaps the key or initialization vector is incorrect')


if __name__ == '__main__':
    pass