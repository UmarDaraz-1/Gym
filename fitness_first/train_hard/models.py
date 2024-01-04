

from django.db import models
from django.utils import timezone

"""class Member(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_date = models.DateField()
    picture = models.ImageField(upload_to='members/', blank=True, null=True)
    active = models.BooleanField(default=True)"""



class Member(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_date = models.DateField()
    picture = models.ImageField(upload_to='member_pictures/', blank=True, null=True)
    captured_picture = models.ImageField(upload_to='captured_pictures/', blank=True, null=True)
    
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Non Active', 'Non Active'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(default=timezone.now)
