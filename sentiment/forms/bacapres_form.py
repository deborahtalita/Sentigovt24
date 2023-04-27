from django import forms
from sentiment.models import Bacapres

class BacapresCreationForm(forms.ModelForm):

    class Meta:
        model = Bacapres
        fields = ('name', 'keyword', 'desc')
