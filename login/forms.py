from django import forms
class StudentPhone(forms.Form):
    phone_number=forms.CharField(max_length=10,min_length=10)

class Studentotp(forms.Form):
    otp=forms.CharField(max_length=4,min_length=4)

class StudentName(forms.Form):
    username=forms.CharField(max_length=30)