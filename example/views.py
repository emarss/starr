from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages


# Create your views here.
def loginForm(request):
	context = {}
	if "message" in request.session:
		context['message'] = request.session['message']
		del request.session["message"]
	if "error" in request.session:
		context['error'] = request.session['error']
		del request.session["error"]

	return render(request, 'login.html', context)

def loginUser(request):
	user = authenticate(request, 
				username=request.POST['username'], 
				password=request.POST['password']
			)
	if user is not None:
		login(request, user)
		return redirect(reverse("home:home"))
	else:
		request.session['error'] = "Please enter the correct username and password for yout account. Note that both fields are case-sensitive."
		return redirect('login')

def logoutUser(request):
	logout(request)
	request.session['message'] = "You are logged out"
	return redirect('login')
