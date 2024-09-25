from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Course, Enrollment
from .forms import SignUpForm, LoginForm, PasswordReset
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings


from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.generic import FormView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomSetPasswordForm

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

#custompassword reset view
class CustomPasswordResetView(FormView):
    template_name = 'registration/custom_password_reset_form.html'  # Your custom template
    success_url = reverse_lazy('password_reset_done')  # Redirect after successful email send
    form_class = PasswordReset  # Using the default password reset form

    def form_valid(self, form):
        # Process form and send reset email
        email = form.cleaned_data['email']
        associated_users = User.objects.filter(email=email)

        if associated_users.exists():
            for user in associated_users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Construct the custom password reset URL
                current_site = get_current_site(self.request)
                domain = current_site.domain
                reset_url = f"http://{domain}/custom-reset/{uid}/{token}/"

                # Prepare email content
                subject = "Password Reset Request"
                message = render_to_string('registration/custom_password_reset_email.html', {
                    'reset_url': reset_url,
                    'user': user,
                    'domain': domain,
                    'protocol': 'https' if self.request.is_secure() else 'http',
                })
                
                # Send the email
                send_mail(subject, message, 'portfolio@softtechzdigitalsolution.com', [user.email], fail_silently=False)

        return super().form_valid(form)
#confirm password reset
#class CustomPasswordResetConfirmView(PasswordResetConfirmView):
  #  template_name = 'registration/custom_password_reset_confirm.html'  # Specify the custom template
  #  success_url = reverse_lazy('password_reset_complete')  # Redirect on success
    #form_class = SetPasswordForm  # Use Django's built-in form for setting new password

    #def form_valid(self, form):
        # Optionally, add custom logic here (e.g., logging or notifications)
       # return super().form_valid(form)



#class CustomPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
  #  template_name = 'registration/custom_password_reset_confirm.html'  # Custom template
   # form_class = CustomSetPasswordForm  # Use the custom form
   # success_url = reverse_lazy('password_reset_complete')  # Redirect after success
    #success_message = "Your password has been set successfully."  
def CustomPasswordResetConfirmView(request, uidb64, token):
    user = User.objects.filter(pk=urlsafe_base64_decode(uidb64)).first()
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'registration/custom_password_reset_confirm.html', {'form': form})
    else:
        return redirect('password_reset_complete')
# landing page function(home)
#@login_required
def home(request):
    return render(request, "EduSphere/index.html")
def forget(request):
    return render(request, "registration/forget.html")
#def register(request):
    #if request.method == 'POST':
       # form = CustomUserCreationForm(request.POST)
       # if form.is_valid():
          #  user = form.save()
           # login(request, user)  # Automatically log in the user after registration
           # return redirect('home')  # Redirect to the homepage after successful registration
    #else:
        #form = CustomUserCreationForm()
    #return render(request, 'registration/register.html', {'form': form})

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
             user = form.save()
             msg = 'user created'
             return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'registration/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminpage')
            elif user is not None and user.is_instructor:
                login(request, user)
                return redirect('intructors')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('learners')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'EduSphere/admin.html')


def intructors(request):
    return render(request,'EduSphere/instructors.html')


def learners(request):
    return render(request,'EduSphere/learner.html')

