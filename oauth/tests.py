from django.test import TestCase

class DummyTest(TestCase):
    def test_dummy(self):
        self.assertIs(True, True)
