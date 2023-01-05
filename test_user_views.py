from app import app
from unittest import TestCase

class WarblerViewsTestCase(TestCase):
    def test_home(self):
        with app.test_client() as client:
            pass
