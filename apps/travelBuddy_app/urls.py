from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^addTrip$', views.addTrip),
    url(r'^addTravel$', views.addTravel),
    url(r'^logout$', views.logout),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^join/(?P<id>\d+)$', views.join),
]