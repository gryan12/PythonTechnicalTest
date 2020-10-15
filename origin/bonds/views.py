import json

from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import BondSerializer
from .models import Bond
from .services import get_legal_name

class Bonds(APIView):
    def get(self, request):

        """
            Filters all bonds by the user making the request
            Filters all bonds by query parameters if parameter keys are Bond fields
            Returns matching bond data
            If parameters present, returns 404 is no matching bonds. 
            If no parameters present, returns empty dict if empty
        """
        
        bonds = Bond.objects.all().filter(user=request.user)
        query_fields = request.GET.dict()

        fields = ["isin", "size", "currency", "maturity", "lei", "legal_name"]

        # ignore anything that is not the name of a field
        parsed_query_fields = {
            x: query_fields[x] for x in query_fields if x in fields
        }

        if parsed_query_fields:
            bonds = Bond.objects.filter(**parsed_query_fields)
        
        #If fetching all (no parameters), empty dict desired behaviour.
        if not bonds and parsed_query_fields: 
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
            Creates and stores a bond if fields with valid data provided
            If no legal name, will make external API call to retrieve
        """
        data = request.data
        if not data["legal_name"]:
            if not data["legal_name"] and data["lei"]:
                data["legal_name"] = get_legal_name(data["lei"])

        serialiser = BondSerializer(data=data)

        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
