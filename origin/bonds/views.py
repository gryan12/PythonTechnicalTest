from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from .serializers import BondSerializer
from .models import Bond


class Bonds(APIView):
    def get(self, request):
        bonds = Bond.objects.all()
        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        return Response({})
