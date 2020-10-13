from rest_framework import serializers
from .models import Bond

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bond
        fields = (
            "isin", 
            "size", 
            "currency", 
            "maturity", 
            "lei", 
            "legal_name",
            )
