from rest_framework.test import APITestCase, APIClient
from django.db import models
from rest_framework.authtoken.models import Token
from ..models import Bond
from ..serializers import BondSerializer
from django.contrib.auth.models import User

class BondModelTest(APITestCase):

    def setUp(self):
        test_user = User.objects.create_user(username="test_user_one", password="test_password")

        self.valid_bond = {
                "isin" : "FR0000131104", 
                "size" : 100000, 
                "currency" : "EUR",
                "maturity" : "2025-02-28", 
                "lei" : "R0MUWSFPU8MPRO8K5P83", 
                "legal_name" : "BNP PARIBAS",
        }
    
    def test_valid_bond_is_valid(self):
        serializer = BondSerializer(data=self.valid_bond)
        print(serializer.is_valid())
        self.assertTrue(serializer.is_valid())


    def test_invalid_lei_not_valid(self):
        lei_with_punctuation = "R0MUWSFPU8MPRO8K)P83"
        lei_with_invalid_size = "R0MUWSFPU8MPRO8KP83"

        self.valid_bond["lei"] = lei_with_punctuation
        serializer = BondSerializer(data=self.valid_bond)
        self.assertFalse(serializer.is_valid())

        self.valid_bond["lei"] = lei_with_invalid_size

        serializer = BondSerializer(data=self.valid_bond)
        self.assertFalse(serializer.is_valid())

    def test_invalid_isin_not_valid(self):
        isin_with_punctuation = "FR.0001,1104"
        isin_with_invalid_size = "FR00131104"

        self.valid_bond["isin"] = isin_with_punctuation

        serializer = BondSerializer(data=self.valid_bond)
        self.assertFalse(serializer.is_valid())

        self.valid_bond["isin"] = isin_with_invalid_size

        serializer = BondSerializer(data=self.valid_bond)
        self.assertFalse(serializer.is_valid())
