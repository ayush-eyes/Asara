from django.conf.urls import patterns, include, url
from rango import views

urlpatterns = patterns('',
    url(r'^project/(?P<project_id_url>\w+)/$', views.project, name='project'),
    url(r'^profile/(?P<user_id_url>\w+)/$', views.view_profile, name='view_profile'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^search/$',views.search_titles),
    url(r'^user_search/$',views.search_profiles),
    url(r'^task_add_people/$',views.add_member),
    )