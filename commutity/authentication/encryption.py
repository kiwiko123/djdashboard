import random
import Crypto.Cipher
import Crypto.Random


class PasswordEncryptor:
    """ Utility class for performing standard 2-way AES encryption on text (e.g., passwords).
        @classmethods provide quick and simple encryption/decryption using a default key.
        Or, more securely, initialize an object to use a custom key.
    """
    _alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789_-=+!@#$%^&*()'

    @staticmethod
    def _generate_cipher(key: bytes, iv: str) -> Crypto.Cipher.AES:
        """ Returns a Crypto.Cipher.AES object using key and iv.
            A Cipher object using the same key/initialization vector CANNOT be used to decrypt the same message;
            i.e., you must create 2 objects - one to encrypt, and the other to decrypt.
        """
        return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)

    @classmethod
    def generate_string(cls, size: int) -> str:
        alphabet_size = len(cls._alphabet)
        result = ''
        for i in range(size):
            c = cls._alphabet[random.randrange(alphabet_size)]
            result += c.lower() if random.randrange(2) else c.upper()
        return result


    _encoding = 'utf-8'
    _key = bytes('fah82bF4CodQvGhfv6Am'[:16], _encoding)
    _iv = Crypto.Random.new().read(Crypto.Cipher.AES.block_size)
    _cipher = _generate_cipher.__func__(_key, _iv)


    @classmethod
    def encrypt(cls, plaintext: str) -> bytes:
        """ Performs AES encryption on plaintext,
            returning the cipher-text data in bytes.
        """
        return cls._cipher.encrypt(bytes(plaintext, cls._encoding))

    @classmethod
    def decrypt(cls, encrypted: bytes) -> str:
        cipher = cls._generate_cipher(cls._key, cls._iv)
        return cipher.decrypt(encrypted)


    def __init__(self, key=None):
        """ Initialize a new PasswordEncryptor object.
            If key=None, randomly generate a key.
            If it is provided, it must be a 16-byte string (str with len 16).
        """
        if key is None:
            key = self.generate_string(Crypto.Cipher.AES.block_size)
        elif len(key) < Crypto.Cipher.AES.block_size:
            raise ValueError('AES encryption requires 16-byte string as a key')
        self._key = bytes(key[:16], self._encoding)
        self._cipher = self._generate_cipher(self._key, self._iv)

    @property
    def key(self) -> str:
        """ Returns the encryption key """
        return self._key

    def encrypt(self, plaintext: str) -> bytes:
        return self._cipher.encrypt(bytes(plaintext, self._encoding))

    def decrypt(self, encrypted: bytes) -> str:
        cipher = self._generate_cipher(self._key, self._iv)
        return cipher.decrypt(encrypted)

