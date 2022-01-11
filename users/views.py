from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Реєстрація нового користувача"""
    if request.method != 'POST':
        # Показати форму рєстрації
        form = UserCreationForm()
    else:
        # Опрацювати заповнену форму
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Ауторизувати користувача та скерувати його на головну сорінку.
            login(request, new_user)
            return redirect('learning_logs:index')
    #Показти порожню або недійсну форму
    context = {'form': form}
    return render(request, 'registration/register.html', context)