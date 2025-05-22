import unittest
from service import app
from service.models import Account
from service.models import AccountFactory
from http import HTTPStatus as status

BASE_URL = "/accounts"
HTTPS_ENVIRON = {'wsgi.url_scheme': 'https'}  # For HTTPS testing


class TestAccountService(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True

    def _create_accounts(self, count):
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            resp = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(resp.status_code, status.CREATED)
            created = resp.get_json()
            account.id = created["id"]
            accounts.append(account)
        return accounts

    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create_accounts(5)
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, status.OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_security_headers(self):
        """It should return security headers"""
        response = self.client.get('/', environ_overrides=HTTPS_ENVIRON)
        self.assertEqual(response.status_code, status.OK)
        headers = {
            'X-Frame-Options': 'SAMEORIGIN',
            'X-Content-Type-Options': 'nosniff',
            'Content-Security-Policy': "default-src 'self'; object-src 'none'",
            'Referrer-Policy': 'strict-origin-when-cross-origin'
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_get_account(self):
        """It should Read a single Account"""
        account = self._create_accounts(1)[0]
        resp = self.client.get(f"{BASE_URL}/{account.id}", content_type="application/json")
        self.assertEqual(resp.status_code, status.OK)
        data = resp.get_json()
        self.assertEqual(data["name"], account.name)

    def test_account_not_found(self):
        """It should return 404 if Account not found"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.NOT_FOUND)

    def test_update_account(self):
        """It should Update an existing Account"""
        test_account = AccountFactory()
        resp = self.client.post(BASE_URL, json=test_account.serialize())
        self.assertEqual(resp.status_code, status.CREATED)

        new_account = resp.get_json()
        new_account["name"] = "Something Known"
        resp = self.client.put(f"{BASE_URL}/{new_account['id']}", json=new_account)
        self.assertEqual(resp.status_code, status.OK)
        updated_account = resp.get_json()
        self.assertEqual(updated_account["name"], "Something Known")

    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        resp = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(resp.status_code, status.NO_CONTENT)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        resp = self.client.delete(BASE_URL)
        self.assertEqual(resp.status_code, status.METHOD_NOT_ALLOWED)


if __name__ == "__main__":
    unittest.main()
