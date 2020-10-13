from django.db import models

class Bond(models.Model):
    isin = models.CharField(max_length=100)
    size = models.IntegerField()
    currency = models.CharField(max_length=10)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100)

    ##placeholders
    def __repr__(self):
        return self.legal_name + " in: " + self.isin

    def __str__(self):
        return self.legal_name, ", in: " + self.isin + ", maturity: ", self.maturity
    
    def get_lei(self):
        return self.lei

