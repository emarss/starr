from django.urls import path

from . import views
app_name = 'journey'

urlpatterns = [
	path('', views.home, name='home'),
	path('story/', views.story, name="story"),
	path('story/update/<int:id>', views.update_story, name="update_story"),
	path('story/delete/<int:id>', views.delete_story, name="delete_story"),
]