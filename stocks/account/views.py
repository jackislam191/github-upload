from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm, UserEditForm, PwdResetConfirmForm
from .models import Account
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
#from django.contrib import messages
# Create your views here.
@login_required
def dashboard(request):
    return render(request, "account/user/dashboard.html")

@login_required
def edit_details(request):
    if request.method == 'POST':
        userform = UserEditForm(instance=request.user, data=request.POST)

        if userform.is_valid():
            userform.save()
    
    else:
        userform = UserEditForm(instance=request.user)
    
    return render(request,'account/user/edit_details.html', {'userform': userform})
@login_required
def user_change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            #messages.success(request, 'Password Changed Successfully!')
            return redirect('account:login')
    else:
        form = SetPasswordForm(user=request.user)
    
    return render(request, 'account/user/user_change_password.html', {'form': form})


def account_register(request):

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            #setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html',{'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')