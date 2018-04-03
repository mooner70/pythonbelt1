from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$',views.user_registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^appointments$', views.appointments), 
    url(r'^add$', views.add),
    url(r'^appointments/(?P<id>\d+)$', views.edit_appointments), 
    url(r'^delete_from_list/(?P<id>\d+)$', views.delete_from_list),
    url(r'^save_appointments/(?P<id>\d+)$', views.save_appointments)
  ]