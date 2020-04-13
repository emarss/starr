from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Dictionary

# Create your views here.
@login_required
def home(request, *args, **kwargs):
	context = {}
	if "message" in request.session:
		context['message'] = request.session['message']
		del request.session["message"]
	if "error" in request.session:
		context['error'] = request.session['error']
		del request.session["error"]

	return render(request, 'dict_home.html', context)