from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Dictionary
from .forms import SearchForm
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .services import dictionary_service


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

	context['form'] = SearchForm(request.POST)
	context['history'] = Dictionary.objects.filter(user=request.user).order_by("-id")[:20]

	return render(request, 'dict_home.html', context)

@login_required
def search_word(request):
	context = {}
	form = SearchForm(request.POST)
	if form.is_valid():
		result = dictionary_service.perfom_search(form.cleaned_data['word'])
		context['result']  = "success"
		if(result['result'] == "found"):
			Dictionary.save_model(form, request)
		context['search_results'] = TemplateResponse(
							request,
							'includes/dict_result.html',
							{
								'result': result['result'],
								'response': result['response'],
								'word': form.cleaned_data['word']
							}
						).render().rendered_content
		context['history'] = TemplateResponse(
								request,
								'includes/dict_words.html',
								{
									'response': Dictionary.objects.filter(user=request.user).order_by("-id")[:20]
								}
							).render().rendered_content
		return JsonResponse(context, status=200)
	else:
		context['result']  = "fail"
		context['html'] = TemplateResponse(
							request,
							'includes/error_message.html',
							{'error':"An error occured, I could not perfom your search. Please try again."}
						).render().rendered_content
		return JsonResponse(context, status=200)