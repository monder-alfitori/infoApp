from django import forms
from .models import *
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 



class SignUpForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'قم بإدخال اسم مستخدم صالح', 
            'maxlength': '16', 
            'minlength': '6', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'أدخل كلمة مرور', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'تأكيد كلمة المرور', 
            'maxlength':'22',  
            'minlength':'8' 
            }) 

 
 
    username = forms.CharField(max_length=20, label=False, min_length=3, help_text='Required. 3 characters or fewer.',) 
 
    class Meta: 
        model = User 
        fields = ('username', 'password1', 'password2', )