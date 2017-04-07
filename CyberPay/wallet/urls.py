from django.conf.urls import url

from . import views

app_name = 'wallet'
urlpatterns = [
    url(r'^transactions/', views.transactions, name='transactions'),
    url(r'^deposit/', views.deposit, name='deposit'),
    url(r'^withdraw/', views.withdraw, name='withdraw'),
]
