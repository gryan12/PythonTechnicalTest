from django.db import models
from django.core.validators import RegexValidator

class Bond(models.Model):
    isin = models.CharField(max_length = 12, validators= [
            RegexValidator(
                regex="^[0-9a-zA-Z]{12}$", message="Incorrect format: should be 12 alphanumeric characters", code="nomatch")
    ])
    size = models.IntegerField()
    currency = models.CharField(max_length=10)
    maturity = models.DateField()
    lei = models.CharField(max_length=20, validators =[
        RegexValidator(
            regex="^[0-9a-zA-Z]{20}$", message="Incorrect format: should be 20 alphanumeric characters"
        )
    ])
    legal_name = models.CharField(max_length=50)

    ##placeholders
    def __repr__(self):
        return self.isin 

    def __str__(self):
        return self.isin + " issued by: " + self.legal_name

    def get_lei(self):
        return self.lei
    
    def get_fields_as_str(self):
        return ["isin", "size", "currency", "maturity", "lei", "legal_name"]

