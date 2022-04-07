import django_filters
from django_filters import CharFilter

from .models import *
from django.forms import ModelForm

class TuoteFilter(django_filters.FilterSet):
    
    class Meta:
        model = Tuote
        fields = {'nimike': ['icontains'],}
        help_texts = {
            'nimike': None,
        }
        labels = {
            "icontains": "",
            "nimike": ""
        }