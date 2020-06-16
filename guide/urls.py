from django.urls import path

from . import views

app_name = 'guide'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.HomepageView.as_view(), name='homepage'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('about', views.AboutView.as_view(), name='about'),
    path('matchups', views.MatchupsView.as_view(), name='matchups'),
    path('search', views.SearchView, name='search'),
    path('<str:pk>/', views.CharacterView.as_view(), name='character'),
    path('<str:charactername>/vote/', views.VoteView.as_view(), name='vote'),
]