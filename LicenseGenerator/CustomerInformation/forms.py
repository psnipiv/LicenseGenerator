# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 20:38:21 2018

@author: pilla
"""
from django import forms
from .models import LicenseInformation

class NewLicenseInformationForm(forms.ModelForm):
    product = forms.CharField(label='Product',
        widget=forms.Textarea(
            attrs={'rows': 1, 'placeholder': 'Enter the product information'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    noofusers = forms.IntegerField(label='No. of Users')
    noofdaystrial = forms.IntegerField(label='Trial Period(Days)')

    class Meta:
        model = LicenseInformation
        fields = ['product','noofusers','noofdaystrial']