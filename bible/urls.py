from django.urls import path

from . import views
app_name = 'bible'

urlpatterns = [
	path('', views.home, name='home'),
	path('chapter/', views.chapter, name="chapter"),
	path('history/', views.history, name="history"),
	path('search/', views.search, name="search"),
	path('history/store/', views.store_history, name="history_store"),
	path('comment/', views.comment, name="comment"),
	path('comment/store/', views.store_comment, name="comment_store"),
	path('comment/update/', views.update_comment, name="comment_update"),
	path('notes/', views.notes, name="notes"),
	path('notes/store/', views.store_notes, name="notes_store"),
	path('comment/delete/', views.delete_comment, name="comment_delete"),
	path('mark/verse/', views.mark_verse, name="mark_verse"),
]