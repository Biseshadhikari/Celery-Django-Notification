from django.shortcuts import render,redirect
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import *
from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.http import JsonResponse


# Create your views here.

def index(request):

    if request.method == "POST": 
        creator_id = request.POST.get("creator")
        creator = Creator.objects.filter(pk = creator_id ).first()
        if creator.subscribers.filter(pk=request.user.pk).exists(): 
            creator.subscribers.remove(request.user)
        else: 
            creator.subscribers.add(request.user)
        return redirect('/index')
    creators = Creator.objects.all()
    return render(request, 'index.html',{'creators':creators})


def post_list(request):
    posts = Post.objects.all()
    notifications = Notification.objects.filter(user = request.user,is_seen =False)

    return render(request, 'post_list.html', {'posts': posts,'notification':notifications.count(),'notifications':notifications})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = Creator.objects.get(user = request.user)
            post.save()


            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})


def manageNotification(request):
    notifications = Notification.objects.filter(user = request.user,is_seen = False)
    for notification in notifications:
        notification.is_seen = True
        notification.save()
    notifications = Notification.objects.filter(user = request.user,is_seen =False).count()
    return JsonResponse({ 
        'notificationCount':notifications
    })

# def manageNotification(request):
#     # Fetch all unread notifications for the user
#     notifications = Notification.objects.filter(user=request.user, is_seen=False)

#     # Update the 'is_seen' attribute for each notification
#     for notification in notifications:
#         notification.is_seen = True

#     # Save all updated notifications at once
#     Notification.objects.bulk_update(notifications, ['is_seen'])

#     # Count the remaining unread notifications for the user
#     remaining_notifications_count = Notification.objects.filter(user=request.user, is_seen=False).count()

#     # Return the count of remaining unread notifications
    # return JsonResponse({'notificationCount': remaining_notifications_count})