from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from register.forms import UpdateForm
from main.models import Author
from django.utils.text import slugify
from django.contrib.auth import logout as lt 


def signup_view(request):
    context = {}
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('update_profile')

    context.update({
        "form": form,
        "title": "signup",
    })

    return render(request, 'register/signup.html', context)


def signin_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
        "title": "Sign in",
    }
    return render(request, 'register/signin.html', context)


@login_required
def update_profile(request):
    user = request.user
    try:
        author = Author.objects.get(user=user)
    except Author.DoesNotExist:
        author = None

    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            update_profile = form.save(commit=False)
            update_profile.user = user
            if not update_profile.slug:
                update_profile.slug = slugify(update_profile.user.username)
                # Ensure unique slug
                counter = 1
                base_slug = update_profile.slug
                while Author.objects.filter(slug=update_profile.slug).exists():
                    update_profile.slug = f"{base_slug}-{counter}"
                    counter += 1
            update_profile.save()
            return redirect("signin")
    else:
        form = UpdateForm(instance=author)

    context = {
        "form": form,
        "title": "Update Profile",
    }
    return render(request, 'register/update.html', context)


@login_required
def logout(request):
    lt(request)
    return redirect("home")