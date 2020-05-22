from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Journey(models.Model):
	def __str__(self):
		return self.story

	story			= models.TextField();
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	created_at		= models.DateTimeField(auto_now=True)
	updated_at		= models.DateTimeField(auto_now_add=True)
	
	def save_model(form, request):
		story = Journey()
		story.user = request.user
		story.story = form.cleaned_data['story']
		story.save()
		return True

	def update_model(form, request, id):
		try:
			story = Journey.objects.get(id = id, user=request.user)
		except Journey.DoesNotExist:
			return True		
		story.story = form.cleaned_data['story']
		story.save()
		return True

	def delete_model(request, id):
		try:
			story = Journey.objects.get(id = id, user=request.user)
		except Journey.DoesNotExist:
			return True		
		story.delete()
		return True