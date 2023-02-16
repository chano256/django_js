from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
# from validate_email import validate_email

# Create your views here.
# class UsernameValidationView(View):
#     def post(self, request):
#         print('here')
#         data = json.loads(request.body)
#         username = data['username']

#         if not str(username).isalnum(): # if not validate_email(email):
#             return JsonResponse({'username_error': 'username should only contain alphanumeric'}, status=400)
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'username_error': 'username exists'}, status=409)
#         return JsonResponse({'username_valid': True})
    
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Get User data
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        # validate data
        if not User.objects.filter(username=username).exists(): # if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, 'Password too short, less than 6')
                return render(request, 'authentication/register.html', context)
            
            user = User.objects.create_user(username=username)
            user.is_active=False
            user.set_password(password)
            user.save()

            # - get domain we are on
            domain = get_current_site(request).domain
            # - url link for verification
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link=reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            # - encode uid
            # - token - only used once

            email_subject = 'Account Activation'
            activate_url = 'http://'+domain+link
            email_body= 'Activate your account now ' + user.username + ' using link\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'allanochan8@gmail.com',
                ['allandavicham@gmail.com', 'no-reply@kcg.com'],
                reply_to=['allanochan8@gmail.com'],
                headers={'Message-ID': 'foo'},
            )

            email.send(fail_silently=False)

            messages.success(request, 'Account successfully created')
            return render(request, 'authentication/register.html')

        # create account
        return render(request, 'authentication/register.html')
    

class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')