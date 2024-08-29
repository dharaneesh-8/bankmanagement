from django import forms

from . models import Bank

class BankForm(forms.ModelForm):
    pin_num = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Bank
        fields = ['first_name','middle_name','last_name','gender','acc_type','father_name','mother_name','aadhar_num','email','mobile_num','address','pin_num','balance_amount']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Middle Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'mobile_num': forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Residential Address', 'class': 'form-control'}),
            'aadhar_num': forms.TextInput(attrs={'placeholder': 'Aadhar Number', 'class': 'form-control'}),
        }


class PinForm(forms.Form):
    account_num = forms.CharField(max_length=16)
    pin_num = forms.CharField(widget=forms.PasswordInput)

class MobileForm(forms.Form):
    mobile_num = forms.CharField(max_length=10)

class OTPForm(forms.Form):
    otp_1 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1', 'autofocus': 'autofocus'}))
    otp_2 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1'}))
    otp_3 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1'}))
    otp_4 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1'}))
    otp_5 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1'}))
    otp_6 = forms.CharField(max_length=1, widget=forms.TextInput(attrs={'class': 'otp-input', 'maxlength': '1'}))
    new_pin = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        otp = ''.join([cleaned_data.get('otp_1', ''), cleaned_data.get('otp_2', ''), cleaned_data.get('otp_3', ''), cleaned_data.get('otp_4', ''), cleaned_data.get('otp_5', ''), cleaned_data.get('otp_6', '')])
        cleaned_data['otp'] = otp
        return cleaned_data

