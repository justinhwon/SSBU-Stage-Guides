from django.urls import path

from . import views

app_name = 'guide'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.HomepageView.as_view(), name='homepage'),
    path('<str:pk>/', views.CharacterView.as_view(), name='character'),
]