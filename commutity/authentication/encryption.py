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
    def _generate_cipher(key: bytes, iv: bytes) -> Crypto.Cipher.AES:
        """ Returns a Crypto.Cipher.AES object using key and iv.
            A Cipher object using the same key/initialization vector CANNOT be used to decrypt the same message;
            i.e., you must create 2 objects - one to encrypt, and the other to decrypt.
        """
        return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)

    @classmethod
    def generate_string(cls, size: int) -> str:
        """ Generates and returns a random string of length 'size' """
        alphabet_size = len(cls._alphabet)
        result = ''
        for i in range(size):
            c = cls._alphabet[random.randrange(alphabet_size)]
            result += c.lower() if random.randrange(2) else c.upper()
        return result


    _encoding = 'utf-8'
    _ckey = bytes('fah82bF4CodQvGhfv6Am'[:16], encoding=_encoding)
    _civ = b'\x1aKas88\x04W\xeef\x0e-\xb4lm3'


    @classmethod
    def default_key(cls) -> str:
        return cls._ckey.decode(encoding=cls._encoding)

    @classmethod
    def default_iv(cls) -> bytes:
        return cls._civ

    @classmethod
    def c_encrypt(cls, plaintext: str) -> bytes:
        """ Performs AES encryption on plaintext,
            returning the cipher-text data in bytes.
        """
        cipher = cls._generate_cipher(cls._ckey, cls.default_iv())
        return cipher.encrypt(bytes(plaintext, cls._encoding))

    @classmethod
    def c_decrypt(cls, encrypted: bytes) -> str:
        cipher = cls._generate_cipher(cls._ckey, cls.default_iv())
        decrypted = cipher.decrypt(encrypted)
        return decrypted.decode(encoding=cls._encoding)


    def __init__(self, key=None, iv=None):
        """ Initialize a new PasswordEncryptor object.
            If {key,iv}='default', use the default class key;
            else if {key,iv}=None, randomly generate one.
            If it is provided, it must be a 16-byte string (str with len 16).
        """
        if key == 'default':
            key = self.default_key()
        elif key is None:
            key = self.generate_string(Crypto.Cipher.AES.block_size)
        elif len(key) < Crypto.Cipher.AES.block_size:
            raise ValueError('AES encryption requires 16-byte string as a key')

        if iv == 'default':
            iv = self.default_iv()
        elif iv is None:
            iv = Crypto.Random.new().read(Crypto.Cipher.AES.block_size)

        self._key = bytes(key[:16], self._encoding)
        self._iv = iv

    @property
    def key(self) -> str:
        """ Returns the encryption key """
        return self._key.decode(encoding=self._encoding)

    @property
    def iv(self) -> bytes:
        """ Returns the randomly-generated initialization vector """
        return self._iv

    def encrypt(self, plaintext: str) -> bytes:
        cipher = self._generate_cipher(self._key, self.iv)
        return cipher.encrypt(bytes(plaintext, self._encoding))

    def decrypt(self, encrypted: bytes) -> str:
        cipher = self._generate_cipher(self._key, self.iv)
        decrypted = cipher.decrypt(encrypted)
        return decrypted.decode(encoding=self._encoding)

