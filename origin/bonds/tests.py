from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db import models

from .models import Bond
from .serializers import BondSerializer


#todo move shared setup to a test utils file
def create_mock_bonds():
        Bond.objects.create(
            isin = "FR0000131104", 
            size = 100000, 
            currency = "EUR",
            maturity = "2025-02-28", 
            lei = "R0MUWSFPU8MPRO8K5P83", 
            legal_name = "Herbert Smith")

        Bond.objects.create(
            isin = "GB0000131104", 
            size = 10, 
            currency = "GBP",
            maturity = "2025-02-28",
            lei = "QZPUOSFLUMMPRH8K5P83", 
            legal_name = "Slaughter and May")

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

        
