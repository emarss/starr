from dictionary.models import Dictionary
from django import forms

class SearchForm(forms.Form):
	word = forms.CharField(widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"autofocus":"",
				"placeholder": "Enter search key here..."
			}
		))
