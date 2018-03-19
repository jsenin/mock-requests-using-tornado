# https://github.com/jsenin/mock-requests-using-tornado
# Demostrate that httmock is able to hook request calls even inside tornado app
# execute: python -m unittest test_fetch.py

import tornado_app
import requests
import unittest
from tornado.testing import AsyncHTTPTestCase
from httmock import urlmatch, HTTMock


MAGIC_STRING = 'Feeling lucky, punk?'

@urlmatch(netloc=r'(.*\.)?google\.com$')
def google_mock(url, request):
    return MAGIC_STRING

class TestMockUsingTornadoApp(AsyncHTTPTestCase):
    def get_app(self):
        return tornado_app.make_app()

    def test_google_request_using_tornado_endpoint(self):
        with HTTMock(google_mock):

            response = self.fetch('/')

            body = response.body.decode()
            self.assertEqual(response.code, 200)
            self.assertEqual(body, MAGIC_STRING)


class TestMockDirectRequest(unittest.TestCase):
    def test_google_request_direct_request(self):
        with HTTMock(google_mock):

            response = requests.get('http://google.com/?q=foo')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, MAGIC_STRING)

class TestDirectRequestWithoutMock(unittest.TestCase):
    def test_google_request_direct_request(self):

        response = requests.get('http://google.com/?q=foo')

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.text, MAGIC_STRING)
