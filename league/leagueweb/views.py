from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from . forms import ProfileUpdateForm, UserUpdateForm
from django.utils.translation import gettext_lazy as _
from .models import Order, Customer
from .models import Profile

User = get_user_model()


def profile(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
    cartItems = 0
    if request.user.is_authenticated:
        # if not hasattr(request.user, 'customer'):
        #     customer = Customer.objects.create(
        #         user=request.user,
        #         name=request.user.first_name,
        #         email=request.user.email
        #     )
        order = Order.objects.get(
            customer=request.user.customer,
            complete=False
        )
        cartItems = order.get_cart_item
    return render(
        request,
        'user_profile/profile.html',
        {'user_': user, 'cartItem': cartItems}
    )


@login_required
@csrf_protect
def profile_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated."))
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        if not hasattr(request.user, 'profile'):
            request.user.profile = Profile.objects.create(user=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(
        request,
        'user_profile/profile_update.html',
        {'user_form': user_form, 'profile_form': profile_form}
    )


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        messages.info(
            request,
            _('In order to sign up, you need to logout first')
        )
        return redirect('main')
    if request.method == "POST":
        error = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        # error = validate_signup_form(
        #     User,
        #     request,
        #     _,
        #     username,
        #     email,
        #     password,
        #     password_confirm,
        # )
        error = False
        if (not username
                or len(username) < 3
                or User.objects.filter(username=username).exists()):
            error = True
            messages.error(
                request,
                _('Username is too short or already exists.')
            )
        if (not email
                or len(email) < 3
                or User.objects.filter(email=email).exists()):
            error = True
            messages.error(
                request,
                _('Email is invalid or user with this email already exists.')
            )
        if (not password
                or not password_confirm
                or password != password_confirm
                or len(password) < 8):
            error = True
            messages.error(
                request,
                _("Password must be at least 8 characters long and match.")
            )
        if not error:
            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            if not hasattr(request.user, 'customer'):
                customer = Customer.objects.create(
                    user=user,
                    name=user.first_name,
                    email=user.email
                )
                user.customer = customer
                Order.objects.create(
                    customer=customer,
                    complete=False
                )
            user.set_password(password)
            user.save()
            messages.success(request, _("User registration successful!"))
            return redirect('login')
    return render(request, 'user_profile/signup.html')


class HomePageView(TemplateView):
    template_name = 'html/home.html'


class CustomLoginView(LoginView):
    template_name = 'html/login.html'


def home_view(request):
    return render(request, 'html/home.html')


def login_view(request):
    return render(request, 'html/login.html')
