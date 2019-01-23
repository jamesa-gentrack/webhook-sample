# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA

import base64, time

@require_POST
@csrf_exempt
def webhook(request):
    # x-payload-signature format:
    # t=timestampvalue,v=tokenvalue
    payload_signature = request.META.get('HTTP_X_PAYLOAD_SIGNATURE')
    t, v = payload_signature.split(',')

    # extract then validate timestamp
    timestamp = t.split('t=')[1]
    now = time.time()
    diff_minutes = (now - int(timestamp)) / 60
    # at this point you can decide to reject the request if it is too old

    payload = b'%s.%s' % (timestamp.encode('utf-8'), request.body)
    sha = SHA512.new(payload)

    # get the application's public key which was provided from the developer portal
    public_key = RSA.import_key(open("pubkey.pem").read())
    verifier = PKCS1_v1_5.new(public_key)

    # extract the base64 encoded signature
    signature = v[2:]
    if not verifier.verify(sha, base64.b64decode(signature)):
        print("Failed to verify signature")
        return HttpResponse(status=400)

    # successfully verified signature
    return HttpResponse(status=200)
