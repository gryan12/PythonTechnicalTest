from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from ..models import Bond
from ..serializers import BondSerializer
from ..services import get_legal_name
import requests
import json


def create_mock_bonds():
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

        return b1, b2
    
def make_and_authenticate_test_user():
        test_user_4 = User.objects.create_user(username="test_user_one", password="test_password")
        test_token = Token.objects.create(user=test_user_4)
        client.credentials(HTTP_AUTHORIZATION='Token ' + test_token.key)
        return test_user_4


client = APIClient()
class TestAuthentication(APITestCase):
    def setUp(self):
        create_mock_bonds

    def test_unauthenticated_cannot_access(self):
        response = client.get(reverse('bonds'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_can_access(self):
        make_and_authenticate_test_user()
        response = client.get(reverse('bonds'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cannot_get_others_data(self):

        first_user = make_and_authenticate_test_user()
        create_mock_bonds()
        first_user_response = client.get(reverse('bonds'))

        second_user = User.objects.create_user(username="test_user_two", password="test_password")
        test_token = Token.objects.create(user=second_user)
        client.credentials(HTTP_AUTHORIZATION='Token ' + test_token.key)
        second_user_response = client.get(reverse('bonds'))

        first_user_bonds = Bond.objects.all().filter(user=first_user)
        first_user_serializer = BondSerializer(first_user_bonds, many=True)

        second_user_bonds = Bond.objects.all().filter(user=second_user)
        second_user_serializer = BondSerializer(second_user_bonds, many=True)

        self.assertEqual(first_user_serializer.data, first_user_response.data)
        self.assertEqual(second_user_serializer.data, second_user_response.data)


class BondViewGet(APITestCase):
    def setUp(self):
        make_and_authenticate_test_user()
        self.bond1, self.bond2 = create_mock_bonds()
    
    def test_get_all_bonds(self):
        response = client.get(reverse('bonds'))
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

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

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_filter_returns_404(self):
        response = client.get(
            reverse('bonds'),
            {'isin': "022003040330"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    



class PostBond(APITestCase):

    def setUp(self):
        self.valid_post_data = {
            "isin":"FR0000131104", 
            "size": 100000, 
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83", 
            "legal_name": "BNP PARIBAS"
        }

        self.invalid_post_data = {
            "isin":"1235sdf;;", 
            "size": 10, 
            "currency": "GBP",
            "maturity": "2025-02-28",
            "lei": "QZPUOSFLUMMPRH8K5P83", 
            "legal_name": "Slaughter and May"
        }

        self.invalid_missing_post_data = {
            "isin":"1235sdf;;", 
            "lei": "QZPUOSFLUMMPRH8K5P83", 
            "legal_name": "Slaughter and May"
        }

        self.test_user = make_and_authenticate_test_user()
    
    def test_valid_full_bond_validates(self):
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.valid_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_valid_returns_expected_data(self):
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.valid_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_incorrect_isin_format(self):
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.invalid_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_incorrect_lei_format(self):
        self.invalid_post_data["lei"] = "R0MUWSFPU8MRO8K5P83"
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.invalid_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_missing_fields(self):
        self.invalid_post_data["lei"] = "R0MUWSFPU8MRO8K5P83"
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.invalid_missing_post_data), 
                content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #integration
    def test_integration_fetches_correct_name(self):
        response = client.post(
            reverse('bonds'),
            data = json.dumps(self.valid_post_data), 
            content_type="application/json"
        )

        self.assertEqual("BNP PARIBAS", response.data["legal_name"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_integration_invalid_returns_400(self):
        response = client.post(
            reverse('bonds'),
            data = json.dumps(self.invalid_post_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_can_get_posted_data(self):
        response = client.post(
            reverse("bonds"),
                data=json.dumps(self.valid_post_data), 
                content_type="application/json"
        )
        response = client.get(
            reverse("bonds")
        )
        self.assertEqual(len(response.data), 1)


        

