from django import forms

from .models import Tuote

class LisaaTuoteForm(forms.ModelForm):
    class Meta:
        model = Tuote
        fields = '__all__'