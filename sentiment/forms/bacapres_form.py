from django import forms
from sentiment.models import Bacapres

class BacapresForm(forms.ModelForm):

    class Meta:
        model = Bacapres
        fields = ('name', 'keyword', 'desc')
