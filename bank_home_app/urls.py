from django.urls import path
from . import views

urlpatterns = [
    path('',views.bank,name = 'home'),
    path('bank-home',views.bank_home,name='1'),
    path('account-created/', views.account_created, name='account_created'),
    path('validate',views.validate_pin,name='2'),
    path('forgot',views.forgot,name='forgot'),
    path('userhome/<int:pk>',views.userhome,name='3'),
    path('withdraw/<int:pk>',views.withdraw,name='4'),
    path('transfer/<int:pk>',views.transfer,name='5'),
    path('forgotpin/<int:pk>',views.forgotpin,name='forgotpin'),
    path('validate_otp/', views.validate_otp, name='validate_otp'),
    path('pin_reset_success/', views.pin_reset_success, name='pin_reset_success'),
    path('deposit/<int:pk>',views.deposit,name='deposit'),
    path('transaction/<int:pk>',views.transaction_history,name='transaction_history'),
]