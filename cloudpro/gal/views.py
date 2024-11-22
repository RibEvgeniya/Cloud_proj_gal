from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserLoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('gallery')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})



import requests
import sys
import json

SMARTCAPTCHA_SERVER_KEY = "<ключ_сервера>"

def check_captcha(token):
    resp = requests.post(
       "https://smartcaptcha.yandexcloud.net/validate",
       data={
          "secret": SMARTCAPTCHA_SERVER_KEY,
          "token": token,
       },
       timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
       print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
       return True
    return json.loads(server_output)["status"] == "ok"

token = "smart-token"
if check_captcha(token):
    print("Passed")
else:
    print("Robot")