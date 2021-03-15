from django.shortcuts import render, redirect
from web.models import Forum, UserToForum
def home(request):
    """主页"""
    forums = Forum.objects.order_by('date_added')
    obj = UserToForum.objects.filter(user=request.user, status=True).all()
    user_forum = []
    for i in obj:
        user_forum.append(i.forum.id)
    context = {'forums': forums, 'user_forum': user_forum}
    return render(request, 'web/home.html', context)