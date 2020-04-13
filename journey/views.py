from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StoryForm
from .models import Journey
from django.http import JsonResponse
from django.template.response import TemplateResponse


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

	queryset = Journey.objects.filter(user=request.user).order_by("-id")
	context['objects'] = queryset
	context['form'] = StoryForm()
	return render(request, 'journey_home.html', context)

@login_required
def story(request):
	form = StoryForm(request.POST)
	context = {}
	if form.is_valid():
		if(Journey.save_model(form, request)):
			context['result']  = "success"
			context['html'] = TemplateResponse(
									request,
									'includes/success_message.html',
									{'message':"Your story has been kept so secretly"}
								).render().rendered_content
			context['new_story'] = TemplateResponse(
									request,
									'includes/story.html',
									{'object': Journey.objects.filter(
													user=request.user
												).order_by("-id")[:1].get()}
								).render().rendered_content
			return JsonResponse(context, status=200)
		else:
			context['result']  = "fail"
			context['html'] = TemplateResponse(
									request,
									'includes/error_message.html',
									{'error':"Ohhh I am sorry, an error occured, I could not save your story. Please try again."}
								).render().rendered_content
	else:
		context['result']  = "fail"
		context['html'] = TemplateResponse(
							request,
							'includes/error_message.html',
							{'error':form.errors}
						).render().rendered_content
	return JsonResponse(context, status=200)

@login_required
def update_story(request, id):
	form = StoryForm(request.POST)
	context = {}
	if form.is_valid():
		if(Journey.update_model(form, request, id)):
			context['result']  = "success"
			context['html'] = TemplateResponse(
									request,
									'includes/success_message.html',
									{'message':"Your story has been updated"}
								).render().rendered_content
			context['your_story'] = TemplateResponse(
									request,
									'includes/inner_story.html',
									{'object': Journey.objects.get(pk=id)}
								).render().rendered_content
			return JsonResponse(context, status=200)
		else:
			context['result']  = "fail"
			context['html'] = TemplateResponse(
									request,
									'includes/error_message.html',
									{'error':"Ohhh I am sorry, an error occured, I could not save your story. Please try again."}
								).render().rendered_content
	else:
		context['result']  = "fail"
		context['html'] = TemplateResponse(
							request,
							'includes/error_message.html',
							{'error':form.errors}
						).render().rendered_content
	return JsonResponse(context, status=200)

@login_required
def delete_story(request, id):
	obj = Journey.objects.get(pk=id)
	if(request.user == obj.user):
		obj.delete()
		request.session['message'] = "A story was successfully deleted."
	else:
		request.session['error'] = "A story was successfully deleted."

	return redirect("journey:home")