from django import forms
from web.models import Inform_Floor
from django.core.exceptions import ValidationError

class InformFloorForm(forms.ModelForm):

    class Meta:
        model = Inform_Floor
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'cols': 115, 'style': "resize:none"})}
