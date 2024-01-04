from django import forms
from .models import Member, Payment

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone_number', 'fee_amount', 'fee_date', 'picture', 'status']

        widgets = {
            'fee_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'