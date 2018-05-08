## Webhook Example in Python
Python is required to run this sample application. The installer can be downloaded [here](https://www.python.org/downloads/).

### Clone this repository
```
git clone git@github.com:Gentrack/webhook-sample-py.git
cd webhook-sample-py
```

### Install dependencies and apply migration
```
pip install -r requirements.txt
python manage.py migrate
```

### Start development server
```
python manage.py runserver
```

### Test the webhook app
1. Download ngrok [here](https://ngrok.com/).
2. Start ngrok and copy the `https` forwarding URL.
```
ngrok http 8000
```
3. Create a new application in the Developer Portal. Select your new application, then on the **Basic Information** page, click `Copy to clipboard` to copy the public key.
4. Save the copied text as `pubkey.pem` in the root directory of this project.
5. On the **Event Subscriptions** page of the same application, click `Edit`. Add the ngrok `https` URL and append `/webhook/`. You can also select the events you want to subscribe to.
6. Click `Send Test Event` to send simulated events from Portal to your webhook application.
