from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/$', views.index),
    url(r'^processRegistration$', views.registration),
    url(r'^processLogin$', views.login),
    url(r'^travels/$', views.home),
    url(r'^travels/destination/(?P<number>\d+)', views.destination),
    url(r'^travels/add/$', views.add),
    url(r'^addVerify$', views.addVerify),
    url(r'^logout/$', views.logout),
    url(r'^travels/addMe/(?P<number>\d+)', views.addMe),
]
