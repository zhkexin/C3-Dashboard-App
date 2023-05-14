from django.contrib.auth import forms  
from django.shortcuts import redirect, render  
from django.contrib import messages  
from django.contrib.auth.forms import UserCreationForm  
from .forms import CustomUserCreationForm  

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = CustomUserCreationForm() 
    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to topics page.
            login(request, new_user)
        return redirect('web_app:claims')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)
