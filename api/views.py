# api views
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def request_token_ready(request, token):
    error = request.GET.get('error', '')
    ctx = RequestContext(request, {
            'error': error,
            'token': token,
            })
    return render_to_response('api/request_token_ready.html', context_instance=ctx)
