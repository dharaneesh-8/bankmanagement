from django.contrib import admin
from . models import Bank,Acc_type,Gender
# Register your models here.

@admin.register(Gender)
class Gender_Admin(admin.ModelAdmin):
    ...

@admin.register(Acc_type)
class Account_type(admin.ModelAdmin):
    ...

@admin.register(Bank)
class Bank_(admin.ModelAdmin):
    ...