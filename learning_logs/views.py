from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.

def index(request):
    """"Головна сторінка 'Журналу спостережень'."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Відображає всі теми."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Показати одну тему та відповіді"""
    topic = Topic.objects.get(id=topic_id)
    # Пересвідчитись чи користувач власник цієї теми
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Додати нову тему"""
    if request.method != 'POST':
        # жодних даних не відправлено; створити порожню форму
        form = TopicForm()
    else:
        # Відправлений POST; обробити дані
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Показати порожню або недійсну форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Додати нову відповідь"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # жодних даних не відправлено; створити порожню форму
        form = EntryForm()
    else:
        # Відправлений POST; обробити дані
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Показати порожню або недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редагувати відповідь"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # жодних даних не відправлено; створити порожню форму
        form = EntryForm(instance=entry)
    else:
        # Відправлений POST; обробити дані
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Показати порожню або недійсну форму.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
