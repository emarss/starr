from bible.models import Bible, BibleComment, BibleNotebook
from django import forms

BIBLE_BOOK_CHOICES = Bible().get_all_bibles_list()

class SearchForm(forms.Form):
	search_key = forms.CharField(min_length=3, widget=forms.TextInput(
			attrs={
				"class": "form-control",
				"min": "3",
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

class BibleNotebookForm(forms.ModelForm):
	class Meta:
		model = BibleNotebook
		fields = [
			'notes'
		]

class BibleCommentForm(forms.ModelForm):
	comment = forms.CharField(min_length=5, widget=forms.Textarea(
			attrs={
				"class": "form-control",
				"min": "5",
				"placeholder": "Type your comment and press enter..."
			}
		))
	class Meta:
		model = BibleComment
		fields = [
			'verse_ref',
			'comment'
		]

class BibleCommentUpdateForm(forms.ModelForm):
	verse_ref_edit = forms.CharField(min_length=5)
	comment_edit = forms.CharField(min_length=5)
	comment_id = forms.IntegerField()
	class Meta:
		model = BibleComment
		fields = [
			'comment_id',
			'comment_edit',
			'verse_ref_edit'
		]