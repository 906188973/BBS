from django.shortcuts import render, redirect
from web.models import Forum, Topic
def home(request):
    """主页"""
    forums = Forum.objects.order_by('date_added')
    obj = Topic.objects.order_by('-floor_count')[:10]
    context = {'forums': forums, 'hottopic':obj}
    return render(request, 'web/home.html', context)