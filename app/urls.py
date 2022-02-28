from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.logout, name = 'logout'),
    path('add-todo/', views.add_todo, name = 'add_todo'),
    path('delete-todo/<int:id>/', views.delete_todo, name = 'delete-todo'),
    path('change-status/<int:id>/<str:status>/', views.change_status, name = 'change-status')
]