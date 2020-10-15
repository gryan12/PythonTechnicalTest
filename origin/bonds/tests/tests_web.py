from rest_framework.test import APITestCase
from ..services import get_legal_name

class ServicesTest(APITestCase):
    def setUp(self):
        self.valid_lei = "R0MUWSFPU8MPRO8K5P83" 
        self.invalid_lei = "QZPUOSFLUMMPRH8K5P83"

    def test_invalid_api_call_returns_none(self):
        self.assertEqual(None, get_legal_name("an incorrect string"))

    def test_api_call_returns_expected_name(self):
        self.assertEqual("BNP PARIBAS", get_legal_name(self.valid_lei))
    