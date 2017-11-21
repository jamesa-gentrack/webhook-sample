# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA

import base64, time

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

    # get your application's public key from the developer portal
    public_key = RSA.import_key(open("app-public-key").read())
    sha = SHA512.new(base64.b64encode(request.body))
    verifier = pkcs1_15.new(public_key)

    # extract the base64 encoded signature
    signature = v.split('v=')[1]
    try:
        verifier.verify(sha, base64.b64decode(signature))
        # successfully verified signature
        return HttpResponse(status=200)
    except (ValueError, TypeError):
        # invalid signature
        return HttpResponse(status=400)
