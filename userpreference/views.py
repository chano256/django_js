from django.shortcuts import render
import os, json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

# Create your views here.
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k,v in data.items():
            currency_data.append({'code': v['code'], 'name': v['name']})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    
    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'preferences': user_preferences})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency =currency
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Modified currency')
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'preferences': user_preferences})
