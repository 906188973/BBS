from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from web.form.manage import InformFloorForm
from web.models import Floor, Inform_Floor, ApplyforForum, Forum, Topic
from web.form.bbs import TopicchangeForm

def index(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    inform = Inform_Floor.objects.filter(status=False)
    applyforForum = ApplyforForum.objects.filter(status=False)
    context = {'inform': inform, 'applyforForum': applyforForum}
    return render(request, 'web/manage.html', context)

def inform_floor(request, id):
    floor = Floor.objects.get(id=id)
    if request.method == 'GET':
        form = InformFloorForm()
        context = {'form': form, 'floor':floor}
        return render(request, 'web/inform_floor.html', context)
    form = InformFloorForm(request.POST)
    if form.is_valid():
        forum = form.save(commit=False)
        forum.user = request.user
        forum.floor = floor
        forum.save()
        # return JsonResponse({'status': True, 'data': '/'})
    return redirect('web:home')
    # return JsonResponse({'status': False, 'error': form.errors})

def manage_topic(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    if request.user.power == 2:
        forums = Forum.objects.filter(moderator=request.user)
        topics = []
        for i in forums:
            topics += i.topic_set.all()
    else:
        topics = Topic.objects.all()
    context = {'topics': topics, }
    return render(request, 'web/manage_topic.html', context)

def manage_comment(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    inform = Inform_Floor.objects.filter(status=False)
    applyforForum = ApplyforForum.objects.filter(status=False)
    context = {'inform': inform, 'applyforForum': applyforForum}
    return render(request, 'web/manage_comment.html', context)

def manage_forum(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    inform = Inform_Floor.objects.filter(status=False)
    applyforForum = ApplyforForum.objects.filter(status=False)
    context = {'inform': inform, 'applyforForum': applyforForum}
    return render(request, 'web/manage_forum.html', context)

def manage_user(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    inform = Inform_Floor.objects.filter(status=False)
    applyforForum = ApplyforForum.objects.filter(status=False)
    context = {'inform': inform, 'applyforForum': applyforForum}
    return render(request, 'web/manage_user.html', context)