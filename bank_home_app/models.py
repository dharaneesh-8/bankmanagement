from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import random
from datetime import timedelta 
from django.utils import timezone


class Gender(models.Model):
    gender = models.CharField(max_length=15)

    def __str__(self):
        return self.gender
    
class Acc_type(models.Model):
    acc_type = models.CharField(max_length=15)

    def __str__(self):
        return self.acc_type
    
class Bank(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    acc_type = models.ForeignKey(Acc_type, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    aadhar_num = models.CharField(max_length=12, unique=True)
    mobile_num = models.CharField(max_length=10, default='0000000000',unique=True)
    email = models.EmailField(default='example@example.com', blank=True, null=True)
    address = models.TextField()
    account_number = models.BigIntegerField(unique=True, editable=False)
    pin_num = models.CharField(max_length=256)
    balance_amount = models.BigIntegerField(default=0)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_timestamp = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  
            last_account = Bank.objects.order_by('-account_number').first()
            if last_account:
                self.account_number = last_account.account_number + 1
            else:
                self.account_number = 1234567891
        super().save(*args, **kwargs)
        
    def set_pin(self, raw_pin):
        self.pin_num = make_password(raw_pin)
        self.save()

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin_num)
    
    def generate_otp(self):
        self.otp = f'{random.randint(100000,999999)}'
        self.otp_timestamp = timezone.now()  
        self.save()

    def verify_otp(self, otp_input):
        if self.otp == otp_input:
            otp_validity_period = timezone.now() - timedelta(minutes=10)
            if self.otp_timestamp > otp_validity_period:
                return True
        return False
    

    def __str__(self):
        return f'Account_Number : {self.account_number}'

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('pin_change', 'PIN Change'),  
    )

    account = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.transaction_type.capitalize()} of {self.amount} on {self.timestamp}'

