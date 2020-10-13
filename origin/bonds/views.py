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

    #TODO: incoming requests assumed to not provide legal_name
    #      need to implement the lei api call
    def post(self, request):
        data = {
            "isin": request.data.get("isin"),
            "currency": request.data.get("currency"),
            "maturity": request.data.get("maturity"),
            "size": int(request.data.get("size")),
            "lei": request.data.get("lei"),
            "legal_name": request.data.get("legal_name"),
        }
        serialiser = BondSerializer(data=data)

        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
