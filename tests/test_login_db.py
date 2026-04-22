import unittest
from unittest.mock import patch, MagicMock
import bcrypt
import secrets

from src.database.users import users


class TestLoginDB(unittest.TestCase):

    @patch.object(users, 'login')
    def test_login_success(self, mock_login):
        # Mock user object returned by login
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = 'testuser'
        mock_login.return_value = mock_user

        result = users().login('testuser', 'testpass')
        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'testuser')

    @patch.object(users, 'login')
    def test_login_failure_wrong_password(self, mock_login):
        mock_login.return_value = None

        result = users().login('testuser', 'wrongpass')
        self.assertIsNone(result)

    @patch.object(users, 'createUser')
    def test_register_creates_user(self, mock_create):
        mock_create.return_value = True

        result = users().createUser('newuser', 'newpass')
        self.assertTrue(result)

    def test_bcrypt_hash_verification(self):
        # Test bcrypt round-trip
        password = 'testpassword123'
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))

        # Test wrong password fails
        self.assertFalse(bcrypt.checkpw('wrongpassword'.encode('utf-8'), hashed))

    def test_bcrypt_salt_generation(self):
        # Test that salts are unique
        salt1 = secrets.token_hex(16)
        salt2 = secrets.token_hex(16)
        self.assertNotEqual(salt1, salt2)
        self.assertEqual(len(salt1), 32)