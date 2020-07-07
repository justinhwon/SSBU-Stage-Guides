from django.urls import path

from . import views

app_name = 'guide'
urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.HomepageView.as_view(), name='homepage'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('about', views.AboutView.as_view(), name='about'),
    path('matchups', views.MatchupsView.as_view(), name='matchups'),
    path('matchupsearch', views.MatchupSearchView, name='matchupsearch'),
    path('matchups/<str:pk>/<str:opponentChar>', views.MatchupInfoView.as_view(), name='matchupinfo'),
    path('search', views.SearchView, name='search'),
    path('<str:pk>/', views.CharacterView.as_view(), name='character'),
    path('<str:charactername>/vote/', views.VoteView.as_view(), name='vote'),
    path('privacypolicy', views.PrivacyView.as_view(), name='privacy'),
    path('termsandconditions', views.TermsView.as_view(), name='terms'),
    path('cookiepolicy', views.CookieView.as_view(), name='cookie'),
]