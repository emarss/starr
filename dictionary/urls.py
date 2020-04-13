from django.urls import path

from . import views
app_name = 'dictionary'

urlpatterns = [
	path('', views.home, name='home'),
	# path('dictionary/', views.dictionary, name="dictionary"),
	# path('dictionary/update/<int:id>', views.update_dictionary, name="update_dictionary"),
	# path('dictionary/delete/<int:id>', views.delete_dictionary, name="delete_dictionary"),
]