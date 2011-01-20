# urls
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
#from piston.authentication import HttpBasicAuthentication
from piston.authentication import OAuthAuthentication
#from piston.doc import documentation_view

from api.handlers import BlogpostHandler

#auth = HttpBasicAuthentication(realm='My sample API')
auth = OAuthAuthentication(realm="Test Realm")

blogposts = Resource(handler=BlogpostHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),
    # automated documentation url(r'^$', documentation_view),
)

urlpatterns += patterns(
    'piston.authentication',
    url(r'^oauth/request_token/$','oauth_request_token'),
    url(r'^oauth/authorize/$','oauth_user_auth'),
    url(r'^oauth/access_token/$','oauth_access_token'),
)
