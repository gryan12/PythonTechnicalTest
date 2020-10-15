#from rest_framework.test import APITestCase, APIClient
#from django.db import models
#from rest_framework.authtoken.models import Token
#from .models import Bond
#from .serializers import BondSerializer

class BondModelTest(APITestCase):
    def setUp(self):
        make_and_authenticate_test_user()
        create_mock_bonds()

    def test_lei(self):
        lei_1 = Bond.objects.get(legal_name="BNP PARIBAS")
        lei_2= Bond.objects.get(legal_name="Slaughter and May")
        self.assertEqual(lei_1.get_lei(), "R0MUWSFPU8MPRO8K5P83")
        self.assertEqual(lei_2.get_lei(), "QZPUOSFLUMMPRH8K5P83")
    
    