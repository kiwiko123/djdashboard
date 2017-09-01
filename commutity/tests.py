import unittest
from django.test import TestCase
from .authentication.encryption import PasswordEncryptor

# Create your tests here.
class TestEncryption(TestCase):

    @unittest.skip('')
    def test_encrypt_password(self):
        encrypted = PasswordEncryptor.encrypt("hello boo!")
        print(encrypted)
        decrypted = PasswordEncryptor.decrypt(encrypted)
        print(decrypted)

    def test_generate_string(self):
        generated = PasswordEncryptor.generate_string(16)
        print(generated)


if __name__ == '__main__':
    pass
