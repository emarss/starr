from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm, RequestForm, BibleNotebookForm, BibleCommentForm, BibleCommentUpdateForm
from .models import Bible, BibleHistory, BibleComment, BibleNotebook, BibleBookmark
from django.http import JsonResponse
from django.template.response import TemplateResponse
from .services import bible_service


# Create your views here.
@login_required
def home(request):
	context = {}

	last_read = BibleHistory.objects.filter(user=request.user).last()
	if(last_read != None):
		current_book = last_read.bible_book
		current_chapter = last_read.bible_chapter
	else:
		current_book = "John"
		current_chapter = 3

	context['ot_books'] = Bible().get_old_testment().keys()
	context['nt_books'] = Bible().get_new_testment().keys()
	context['current_book'] = current_book
	context['current_chapter'] = current_chapter
	context['current_verse_key'] = current_book + " " + str(current_chapter) + ":" + "1"

	context['request_form'] = RequestForm()
	context['search_form'] = SearchForm()
	context['notebook_form'] = BibleNotebookForm()
	context['comment_form'] = BibleCommentForm()
	if "message" in request.session:
		context['message'] = request.session['message']
		del request.session["message"]
	if "error" in request.session:
		context['error'] = request.session['error']
		del request.session["error"]
	return render(request, 'bible_home.html', context)

@login_required
def chapter(request):
	context = {}

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

			chapter_name = current_book + " " + str(current_chapter)
			context['marked_verses'] = list(BibleBookmark.get_bookmarks(request, chapter_name))
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



@login_required
def store_history(request):
	context = {}
	form = RequestForm(request.POST)
	if(form.is_valid()):
		BibleHistory.save_model(form, request)
	return JsonResponse({}, status=200)


@login_required
def history(request):
	context = {}

	context['html'] = TemplateResponse(
						request,
						'includes/bible_history.html',
						{
							"history": BibleHistory.objects.filter(user=request.user).order_by("-id")
						}
					).render().rendered_content
	return JsonResponse(context, status=200)

@login_required
def search(request):
	context = {}
	form = SearchForm(request.POST)
	if(form.is_valid()):
		context["result"] = "success"
		context["search_key"] = form.cleaned_data['search_key']
		search_results = bible_service.perform_search(form.cleaned_data['search_key'])
		context["search_results"] = TemplateResponse(
								request,
								'includes/bible_search_results.html',
								{
									"results": search_results,
									"search_key": form.cleaned_data['search_key']
								}
							).render().rendered_content
	else:
		context["result"] = "fail"
		context["errors"] = form.errors
	return JsonResponse(context, status=200)

@login_required
def notes(request):
	context = {}
	context["html"] = BibleNotebook.get_notes(request).notes
	return JsonResponse(context, status=200)

@login_required
def comment(request):
	context = {}
	context["html"] = TemplateResponse(
							request,
							'includes/bible_comments.html',
							{
								"comments": BibleComment.get_comments(request.POST["verse"], request)
							}
						).render().rendered_content
	return JsonResponse(context, status=200)

@login_required
def store_notes(request):
	context = {}
	form = BibleNotebookForm(request.POST)
	if(form.is_valid()):
		context["result"] = "success"
		BibleNotebook.save_model(form, request)
		context["html"] =  BibleNotebook.get_notes(request).notes
	else:
		context["result"] = "fail"
		context["errors"] = form.errors
	return JsonResponse(context, status=200)

@login_required
def store_comment(request):
	context = {}
	form = BibleCommentForm(request.POST)
	if(form.is_valid()):
		context["result"] = "success"
		BibleComment.save_model(form, request)
		comments = BibleComment.get_comments(form.cleaned_data['verse_ref'], request)
		context["html"] = TemplateResponse(
								request,
								'includes/bible_comments.html',
								{
									"comments": comments,
								}
							).render().rendered_content
	else:
		context["result"] = "fail"
		context["errors"] = form.errors
	return JsonResponse(context, status=200)	

@login_required
def update_comment(request):
	context = {}
	form = BibleCommentUpdateForm(request.POST)
	if(form.is_valid()):
		context["result"] = "success"
		BibleComment.update_model(form, request)
		comments = BibleComment.get_comments(form.cleaned_data['verse_ref_edit'], request)
		context["html"] = TemplateResponse(
								request,
								'includes/bible_comments.html',
								{
									"comments": comments,
								}
							).render().rendered_content
	else:
		context["result"] = "fail"
		context["errors"] = form.errors
	return JsonResponse(context, status=200)

@login_required
def delete_comment(request):
	context = {}
	if BibleComment.delete_comment(request.POST["comment_id"], request):
		context["result"] = "success"
		comments = BibleComment.get_comments(request.POST['verse'], request)
		context["html"] = TemplateResponse(
								request,
								'includes/bible_comments.html',
								{
									"comments": comments,
								}
							).render().rendered_content
	else:
		context["result"] = "fail"
		context["error"] = "An error occurred and you comment was not deleted. Please refresh page and try again"

	return JsonResponse(context, status=200)

@login_required
def mark_verse(request):
	context = {}
	result = BibleBookmark.process(request, request.POST['key'])
	if result == "added":
		context["result"] = "success"
		context["action"] = "added"
	elif result == "removed":
		context["result"] = "success"
		context["action"] = "removed"
	else:
		context["result"] = "fail"
		context["error"] = "An error occurred and you verse was not bookmarked. Please refresh page and try again"

	return JsonResponse(context, status=200)