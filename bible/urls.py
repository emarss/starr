from django.urls import path

from . import views
app_name = 'bible'

urlpatterns = [
	path('', views.home, name='home'),
	path('chapter/', views.chapter, name="chapter"),
	# path('story/update/<int:id>', views.update_story, name="update_story"),
	# path('story/delete/<int:id>', views.delete_story, name="delete_story"),
]