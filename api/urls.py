from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init', views.init, name='init'),  # http://127.0.0.1:8000/api/init
    path('user/pref', views.pref, name='pref'), # http://127.0.0.1:8000/api/user/pref
    path('user/feedback', views.feedback, name='feedback'), # http://127.0.0.1:8000/api/user/feedback
    path('finalseating', views.finalseating, name='finalseating'),  # http://127.0.0.1:8000/api/finalseating

    path('random199', views.random199, name='random199'),  # http://127.0.0.1:8000/api/random199
    path('result', views.result, name='result'),    # http://127.0.0.1:8000/api/result
]