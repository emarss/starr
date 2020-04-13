from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Dictionary(models.Model):
	def __str__(self):
		return self.word

	word			= models.CharField(max_length=50);
	user			= models.ForeignKey(User, on_delete=models.CASCADE)
	created_at		= models.DateTimeField(auto_now=True)
	updated_at		= models.DateTimeField(auto_now_add=True)