from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('builder/', views.builder),
    # path('editor/', views.editor),
    path('about/', views.about),
    path('blog/', views.blog),
    path('guide/', views.guide),
    path('getcombo/', views.get_combo),
    path('getstances/', views.get_stances),
    path('gettransitions/', views.get_transitions),
    path('gettricks/', views.get_tricks),
    path('shorten/', views.shorten),
    path('get_set_tricks/', views.get_set_tricks),
    path('regenerate/', views.regenerate),
    path('load_combo/', views.load_combo),
    path('test/', views.test),
    path('game/', views.game),
]