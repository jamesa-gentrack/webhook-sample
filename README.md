1. Install python - https://www.python.org/downloads/windows/.
2. Open a command prompt window and change to a directory where you want to save your project.
3. Install django package:
```
pip install django
```
4. Start a new django project:
```
django-admin startproject webhook
```
5. This will create a new directory in the current directory and will be the root of your project. You can now add an application to your project:
```
cd webhook
python manage.py startapp webhookapp
```
6. Add a URL where the BillReady event will be sent. It is highly advisable to open the webhook folder in an editor that supports projects (e.g. Visual Studio Code, Sublime Text, Notepad++, etc) so you can easily navigate the project tree.
```
## open webhook/urls.py in your editor and add the following lines
 
from webhookapp import views
 
# add a new url item in urlpatterns
url(r'^webhook/', views.webhook, name='webhook'),
```
7. Add a new function that will handle the request sent to the URL defined in #6.
```
## open webhookapp/views.py and add the following lines
 
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from hashlib import sha512
 
import base64, hmac, time
 
@require_POST
@csrf_exempt
def webhook(request):
    # request headers
    # you can validate these values or use them for something else
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
    # do something with the payload..
    return HttpResponse(status=200)
```
8. Run a development server to test:
```
## in root project directory
python manage.py runserver
```
9. You can now send requests to your application at http://localhost:8000/webhook.
