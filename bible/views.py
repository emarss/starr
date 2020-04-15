from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SearchForm, RequestForm
from .models import Bible
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .services import bible_service


# Create your views here.
@login_required
def home(request):
	context = {}

	current_book = "Genesis"
	current_chapter = 1
	context['ot_books'] = Bible().get_old_testment().keys()
	context['nt_books'] = Bible().get_new_testment().keys()
	context['current_book'] = current_book
	context['current_chapter'] = current_chapter


	context['chapter'] = bible_service.get_full_chapter(
							current_book,
							current_chapter
						)

	context['chapters_count'] = Bible().get_all_bibles()[current_book]
	context['verses_count'] = len(context['chapter'].keys())
	print(len(context['chapter'].keys()))	

	context['request_form'] = RequestForm()
	context['search_form'] = SearchForm()
	if "message" in request.session:
		context['message'] = request.session['message']
		del request.session["message"]
	if "error" in request.session:
		context['error'] = request.session['error']
		del request.session["error"]
	return render(request, 'bible_home.html', context)

# Create your views here.
@login_required
def chapter(request):
	context = {}
	print(len(Bible().get_old_testment().keys()))
	form = RequestForm(request.POST)
	if(form.is_valid()):
		current_book = form.cleaned_data['bible_book']
		current_chapter = form.cleaned_data['bible_chapter']

		chapter_dict = bible_service.get_full_chapter(
								current_book,
								current_chapter
							)
		if(len(chapter_dict)):

			context['chapter'] = TemplateResponse(
								request,
								'includes/bible_chapter.html',
								{
									"chapter": chapter_dict
								}
							).render().rendered_content
			context['result'] = "success"
			context['current_book'] = current_book
			context['current_chapter'] = current_chapter
			context['chapters_count'] = Bible(). get_all_bibles()[current_book]
			context['verses_count'] = len(chapter_dict.keys())

		else:
			context['result'] = "fail"
			context['html'] = "An error occured and your request could not be handled. Please refresh page and try again"
	else:
		context['result'] = "fail"
		context['html']  = form.errors
	return JsonResponse(context, status=200)