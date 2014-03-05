"""
Django URLs
"""
from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^data/$', views.data, name='data'),
                       url(r'^generate/$', views.generate, name='generate'),
                       url(r'^savecoord/$', views.savecoord, name='savecoord'),
                       )
