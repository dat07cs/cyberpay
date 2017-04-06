from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^transactions/', views.transactions, name='transactions'),
    url(r'^deposit/', views.deposit, name='deposit'),
    url(r'^withdraw/', views.withdraw, name='withdraw'),
]
