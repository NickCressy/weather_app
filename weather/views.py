from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Location
from .forms import LocationForm
import requests

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

def get_weather(city):
    api_key = 'key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def home(request):
    if request.user.is_authenticated:
        locations = Location.objects.filter(user=request.user)
        weather_data = []
        for location in locations:
            weather = get_weather(location.city)
            if weather:
                weather_data.append({'city': location.city, 'weather': weather})
        
        if request.method == 'POST':
            form = LocationForm(request.POST)
            if form.is_valid():
                if locations.count() < 10:
                    form.instance.user = request.user
                    form.save()
                    return redirect('home')
        else:
            form = LocationForm()
        return render(request, 'weather/home.html', {'locations': locations, 'form': form, 'weather_data': weather_data})
    else:
        return redirect('login')
