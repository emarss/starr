from journey.models import Journey
from django import forms

class StoryForm(forms.Form):
	story = forms.CharField(widget=forms.Textarea(
			attrs={
				"class": "form-control",
				"autofocus":"",
				"placeholder": "Tell me something about today, like what have you been up to..."
			}
		))
