from rest_framework.test import APITestCase, APIClient
from django.db import models
from rest_framework.authtoken.models import Token
from ..models import Bond
from ..serializers import BondSerializer
from django.contrib.auth.models import User

class BondModelTest(APITestCase):

    def setUp(self):
        test_user = User.objects.create_user(username="test_user_one", password="test_password")

        b1 = Bond.objects.create(
            isin = "FR0000131104", 
            size = 100000, 
            currency = "EUR",
            maturity = "2025-02-28", 
            lei = "R0MUWSFPU8MPRO8K5P83", 
            legal_name = "BNP PARIBAS")

        b2 = Bond.objects.create(
            isin = "GB0000131104", 
            size = 10, 
            currency = "GBP",
            maturity = "2025-02-28",
            lei = "QZPUOSFLUMMPRH8K5P83", 
            legal_name = "Slaughter and May") 


    def test_lei(self):
        lei_1 = Bond.objects.get(legal_name="BNP PARIBAS")
        lei_2= Bond.objects.get(legal_name="Slaughter and May")
        self.assertEqual(lei_1.get_lei(), "R0MUWSFPU8MPRO8K5P83")
        self.assertEqual(lei_2.get_lei(), "QZPUOSFLUMMPRH8K5P83")
    

    def test_invalid_lei_not_valid(self):
        lei_with_punctuation = "R0MUWSFPU8MPRO8K)P83"
        lei_with_invalid_size = "R0MUWSFPU8MPRO8KP83"

        modelData = {
            "isin" : "FR0000131104", 
            "size" : 100000, 
            "currency" : "EUR",
            "maturity" : "2025-02-28", 
            "lei" : lei_with_punctuation, 
            "legal_name" : "BNP PARIBAS"
        }
        serializer = BondSerializer(data=modelData)
        self.assertFalse(serializer.is_valid())

        modelData["lei"] = lei_with_invalid_size

        serializer = BondSerializer(data=modelData)
        self.assertFalse(serializer.is_valid())



