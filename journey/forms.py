from journey.models import Journey
from django import forms

class StoryForm(forms.Form):
	story = forms.CharField()
