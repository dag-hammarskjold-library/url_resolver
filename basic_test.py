import unittest
import app
from urllib.parse import quote
import json


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()
        self.symbol = "S/RES/2421 (2018)"

    def test_symbol(self):
        resp = self.app.get('/symbol/{}'.format(quote(self.symbol)))
        self.assertEqual(resp.status_code, 200)

    def test_rest(self):
        resp = self.app.get('/symbol/{}?rest=true&lang=en'.format(quote(self.symbol)))
        self.assertEqual(resp.status_code, 200)
        d = json.loads(resp.data)
        self.assertEqual(d['EN'], 'https://digitallibrary.un.org/record/1629899/files/S_RES_2421%282018%29-EN.pdf')
        self.assertTrue('metadata' in d.keys())
        self.assertTrue('EN' in d.keys())
        self.assertTrue('lang' in d.keys())

    def test_redirect(self):
        resp = self.app.get('/symbol/{}?file=true&lang=en'.format(quote(self.symbol)))
        self.assertEqual(resp.status_code, 302)

    def test_raise_error(self):
        resp = self.app.get('/symbol/{}?file=true&lang=en&rest=true'.format(quote(self.symbol)))
        self.assertEqual(resp.status_code, 500)

    def test_empty_db(self):
        rv = self.app.get('/')
        print(rv)
        # assert b'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()
