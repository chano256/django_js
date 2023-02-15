from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
# from validate_email import validate_email

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        print('here')
        data = json.loads(request.body)
        print(data)
        username = data['username']

        if not str(username).isalnum(): # if not validate_email(email):
            return JsonResponse({'username_error': 'username should only contain alphanumeric'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username exists'}, status=409)
        return JsonResponse({'username_valid': True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get User data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        # validate data
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    print(context.username)
                    messages.error(request, 'Password too short, less than 6')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        # create account

        return render(request, 'authentication/register.html')