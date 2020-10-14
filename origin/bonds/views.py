from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

from rest_framework.permissions import IsAuthenticated

from .serializers import BondSerializer
from .models import Bond

import json

from .services import get_legal_name


class Bonds(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):

        bonds = Bond.objects.all()
        query_fields = request.GET.dict()

        #TODO: clean, extensible way of delegating this to the Bond model?
        fields = ["isin", "size", "currency", "maturity", "lei", "legal_name"]

        parsed_query_fields = {
            x: query_fields[x] for x in query_fields if x in fields
        }

        if parsed_query_fields:
            bonds = Bond.objects.filter(**parsed_query_fields)
        
        #TODO: decide if returning empty dict actually more desirable behaviour
        if not bonds:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    #TODO: incoming requests assumed to not provide legal_name
    #      need to implement the lei api call
    def post(self, request):

        data = request.data

        if not data["legal_name"]:
            if not data["legal_name"] and data["lei"]:
                data["legal_name"] = get_legal_name(data["lei"])

        serialiser = BondSerializer(data=data)

        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
