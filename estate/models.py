from django.db import models
from django.conf import settings
# Create your models here.

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=255)
    
class Unit(models.Model):
    unit_name = models.CharField(max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveIntegerField(choices=[(1, '1BHK'), (2, '2BHK'), (3, '3BHK'), (4, '4BHK')])
    
class DocumentProof(models.Model):
    proof_name = models.CharField(max_length=255)
    document = models.FileField(upload_to=f'{settings.MEDIA_ROOT}/documents') 

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    document_proof = models.ForeignKey(DocumentProof, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()
    monthly_rent_date = models.DateField()
    property = models.CharField(max_length=255)

