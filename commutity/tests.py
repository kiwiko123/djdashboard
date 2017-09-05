import unittest
from django.test import TestCase
from .authentication.encryption import PasswordEncryptor
from .utilities import properties
from . import helper


class TestUtilities(unittest.TestCase):
	def test_helper_get_app_directory(self):
		result = helper.get_app_directory()
		self.assertTrue(result, 'get_app_directory() returned empty string')
		
	def test_helper_get_properties_file(self):
		result = helper.get_properties_file()
		self.assertTrue(result.is_file())
		self.assertTrue(result.name == 'properties.xml')


class TestPropertyManager(unittest.TestCase):
	def test_xml_parsing(self):
		properties_path = helper.get_properties_file()
		manager = properties.PropertyManager(properties_path)
		for k, v in manager._properties.items():
			print('{0}: {1}'.format(k, v))


# Create your tests here.
class TestEncryption(TestCase):

    def test_encrypt_password(self):
        message = 'hello boo!'
        encrypted = PasswordEncryptor.c_encrypt(message)
        decrypted = PasswordEncryptor.c_decrypt(encrypted)
        self.assertNotEqual(message, encrypted)
        self.assertEqual(message, decrypted, 'message != decrypted message')

    def test_generate_string(self):
        generated = PasswordEncryptor.generate_string(16)
        self.assertEqual(16, len(generated))


if __name__ == '__main__':
    unittest.main()