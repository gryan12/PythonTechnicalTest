from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db import models

from .models import Bond
from .serializers import BondSerializer

import json

from .services import get_legal_name


#TODO: use 'accurate' and more test data
#TODO: modularise

#TODO move shared setup to a test utils file
def create_mock_bonds():
        b1 = Bond.objects.create(
            isin = "FR0000131104", 
            size = 100000, 
            currency = "EUR",
            maturity = "2025-02-28", 
            lei = "R0MUWSFPU8MPRO8K5P83", 
            legal_name = "Herbert Smith")

        b2 = Bond.objects.create(
            isin = "GB0000131104", 
            size = 10, 
            currency = "GBP",
            maturity = "2025-02-28",
            lei = "QZPUOSFLUMMPRH8K5P83", 
            legal_name = "Slaughter and May")

        return b1, b2

class BondTest(APITestCase):
    def setUp(self):
        create_mock_bonds()

    def test_lei(self):
        lei_1 = Bond.objects.get(legal_name="Herbert Smith")
        lei_2= Bond.objects.get(legal_name="Slaughter and May")
        self.assertEqual(lei_1.get_lei(), "R0MUWSFPU8MPRO8K5P83")
        self.assertEqual(lei_2.get_lei(), "QZPUOSFLUMMPRH8K5P83")


client = APIClient()
class GetAllBonds(APITestCase):
    def setUp(self):
        create_mock_bonds()
    
    def test_get_all_bonds(self):
        response = client.get(reverse('bonds'))
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFilteredRequest(APITestCase):
    def setUp(self):
        b1, b2 = create_mock_bonds()
        self.bond1 = b1
        self.bond2 = b2
    
    def test_filter_by_legal_name(self):
        response = client.get(
            reverse('bonds'),
            {'legal_name': self.bond1.legal_name}
        )
        
        bonds = Bond.objects.all()
        bonds = Bond.objects.filter(legal_name=self.bond1.legal_name)
        serializer = BondSerializer(bonds, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_size(self):
        response = client.get(
            reverse('bonds'),
            {'size': self.bond1.size}
        )
        
        bonds = Bond.objects.all()
        bonds = Bond.objects.filter(size=self.bond1.size)
        serializer = BondSerializer(bonds, many=True)
        print(response.data, " : ", serializer.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_filter(self):
        response = client.get(
            reverse('bonds'),
            {'isin': "022003040330"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostBond(APITestCase):

    def setUp(self):
        self.valid_post_data = {
            "isin":"GB0000131104", 
            "size": 10, 
            "currency": "GBP",
            "maturity": "2025-02-28",
            "lei": "QZPUOSFLUMMPRH8K5P83", 
            "legal_name": "Slaughter and May"
        }

        self.invalid_post_data = {
            "isin":"", 
            "size": 10, 
            "currency": "GBP",
            "maturity": "2025-02-28",
            "lei": "QZPUOSFLUMMPRH8K5P83", 
            "legal_name": "Slaughter and May"
        }
    
    def test_post_bond(self):
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.valid_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

class ServicesTest(APITestCase):

    def setUp(self):
        self.url = "https://leilookup.gleif.org/api/v2/leirecords?lei="
        self.lei1 = "R0MUWSFPU8MPRO8K5P83"

    def test_can_access_api(self):
        get_legal_name(self.lei1)
        self.assertEqual(1, 1)

    

        




        
