from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Location

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'weather/signup.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        locations = Location.objects.filter(user=request.user)
        if form.is_valid():
            if locations.count() < 10:
                form.instance.user = request.user
                form.save()
                return redirect('home')
        else:
            form = LocationForm()
        return render(request, 'weather/home.html', {'locations': locations, 'form': form})
    else:
        return redirect('login'))
