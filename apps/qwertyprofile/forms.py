from django import forms

from .models import QwertyProfile

class QwerterProfileForm(forms.ModelForm):
    class Meta:
        model = QwertyProfile
        fields = ('avatar',)