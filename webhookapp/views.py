# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from hashlib import sha512

import base64, hmac, json, time

@require_POST
@csrf_exempt
def webhook(request):
    # request headers
    event = request.META.get('HTTP_X_PLATFORM_EVENT')
    platform_sid = request.META.get('HTTP_X_PLATFORM_SID')

    # x-payload-signature format:
    # t=timestampvalue,v=tokenvalue
    payload_signature = request.META.get('HTTP_X_PAYLOAD_SIGNATURE')
    t, v = payload_signature.split(',')

    # extract then validate timestamp
    timestamp = t.split('t=')[1]
    now = time.time()
    diff_minutes = (now - int(timestamp)) / 60
    # you can decide to reject the request if it is too old
    print diff_minutes

    # extract then validate signature
    signature = v.split('v=')[1]

    # authentication token
    # don't commit your token to repository!
    # use os.environ.get('AUTHENTICATION_TOKEN')
    auth_token = 'token12345'

    mac = hmac.new(bytes(auth_token), digestmod=sha512)
    mac.update(timestamp + ".")
    # payload body
    mac.update(request.body)
    base64_mac = base64.b64encode(mac.digest())

    if not hmac.compare_digest(bytes(base64_mac), bytes(signature)):
        # invalid signature
        return HttpResponse(status=403)

    # successfully verified signature
    return HttpResponse(status=200)
