from django.shortcuts import render, redirect
from web.models import Forum, Topic
from web import models
from web.form.bbs import ForumForm
def home(request):
    """主页"""
    forums = Forum.objects.order_by('date_added')
    obj = Topic.objects.order_by('-floor_count')[:20]
    forum = models.UserToForum.objects.filter(user=request.user)
    user_forum = []
    for i in forum :
        user_forum.append(i.forum.id)
    usertouser = models.UserToUser.objects.filter(user=request.user)
    form = ForumForm()
    context = {'forums': forums, 'hottopic': obj, 'form': form, 'user_forum': user_forum}
    context['usertouser'] = usertouser
    return render(request, 'web/home.html', context)