# urls
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^', include('blog.urls')),
    (r'^api/', include('api.urls')),
    (r'^admin/(.*)', admin.site.root),
    )

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^accounts/logout/$', 'logout',
        {'next_page': '/'},
        name='logout'),

    url(r'^accounts/login/$', 'login',
        {'template_name': 'accounts/login.html'},
        name='login'),
)
