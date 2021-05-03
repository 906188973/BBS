from django.shortcuts import render, redirect
from web.models import Forum, Topic
from web.form.bbs import ForumForm
def home(request):
    """主页"""
    forums = Forum.objects.order_by('date_added')
    obj = Topic.objects.order_by('-floor_count')[:10]
    form = ForumForm()
    context = {'forums': forums, 'hottopic': obj, 'form': form}
    return render(request, 'web/home.html', context)