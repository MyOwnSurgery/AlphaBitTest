from django.urls import path

from . import views

urlpatterns = [
    path('get_new/', views.get_new),
    path('get_issued/', views.get_issued),
    path('get_delivered/', views.get_delivered),
    path('get_handed/', views.get_handed),
    path('get_refused/', views.get_refused),
    path('get_paid_refused/', views.get_paid_refused),
    path('get_complete/', views.get_complete),
    path('get_none/', views.get_none),
]
