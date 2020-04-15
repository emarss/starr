from bible.models import Bible
from django import forms

BIBLE_BOOK_CHOICES = Bible().get_all_bibles_list()

class SearchForm(forms.Form):
	search_key = forms.CharField(widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"placeholder": "Type search and press enter..."
			}
		))

class RequestForm(forms.Form):
	bible_book = forms.ChoiceField(widget=forms.Select(
			attrs={
				"class": "form-control",	
			}),
		choices = BIBLE_BOOK_CHOICES
	)
	bible_chapter = forms.IntegerField(widget=forms.NumberInput(
			attrs={
				"class": "form-control",
				"value": 1,
				"min":1
			}
		))
	bible_verse = forms.IntegerField(widget=forms.NumberInput(
			attrs={
				"class": "form-control",
				"value": 1,
				"min":1
			}
		))
