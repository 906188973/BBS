from django.shortcuts import render, redirect
from web.form.bbs import ForumForm, TopicForm, FloorForm
from django.http import JsonResponse, HttpResponseRedirect
from web.models import Topic, Forum, Floor, Comment, UserToForum, Collect, UserInfo, ForumPower
from django.db.models import Max
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

def create_forum(request):
    """创建版块"""
    if request.method == 'GET':
        form = ForumForm()
        context = {'form': form}
        return render(request, 'web/create_forum.html', context)
    form = ForumForm(request.POST, request.FILES)
    print(request.FILES)
    if form.is_valid():
        print('进入')
        forum = form.save(commit=False)
        forum.moderator = request.user
        forum.save()
        # return JsonResponse({'status': True, 'data': '/'})
    return redirect('web:home')
    # return JsonResponse({'status': False, 'error': form.errors})

def fourm(request, forum_id):
    """显示所有帖子主题"""
    forum = Forum.objects.get(id=forum_id)
    topics = forum.topic_set.order_by('date_added')
    obj = UserToForum.objects.filter(user=request.user, status=True).all()

    user_forum = []
    for i in obj:
        user_forum.append(i.forum.id)
    """创建新贴"""
    if request.method != 'POST':
        form_topic = TopicForm()
        form_floor = FloorForm()
    else:
        form_topic = TopicForm(request.POST)
        form_floor = FloorForm(request.POST)
        if form_topic.is_valid() and form_floor.is_valid():
            topic = form_topic.save(commit=False)
            topic.forum = forum
            topic.owner = request.user
            topic.floor_count = 1
            topic.save()

            floor = form_floor.save(commit=False)
            floor.owner = request.user
            floor.topic = topic
            floor.floor_number = 1
            floor.save()

            forum.topic_count += 1
            forum.save()
            # return redirect('web:forum', args=[forum_id])
            return HttpResponseRedirect(reverse('web:forum', args=[forum_id]))
    context = {'forum': forum, 'form_topic': form_topic, 'form_floor': form_floor}
    context['user_forum'] = user_forum

    if topics:
        context['topics'] = topics
    return render(request, 'web/topics.html', context)

def topic(request, topic_id):
    """显示帖子"""
    topic = Topic.objects.get(id=topic_id)
    floors = topic.floor_set.order_by('date_added')
    obj = Collect.objects.filter(user=request.user, status=True).all()
    collect = []
    for i in obj:
        collect.append(i.topic.id)
    """回复帖子"""
    if request.method != 'POST':
        form = FloorForm()
    else:
        form = FloorForm(request.POST)
        if form.is_valid():
            obj = Floor.objects.filter(topic=topic).aggregate(max=Max('floor_number'))
            floor = form.save(commit=False)
            floor.topic = topic
            floor.owner = request.user
            floor.floor_number = obj['max'] + 1
            floor.save()

            topic.floor_count += 1
            topic.save()

            # return redirect('web:topic', args=[topic_id])
            return HttpResponseRedirect(reverse('web:topic', args=[topic_id]))
    context = {'topic': topic, 'floors': floors, 'form': form}
    context['collect'] = collect
    return render(request, 'web/topic.html', context)

def update_comment(request):
    data = {}
    if request.method == 'POST':
            user = request.user
            text = request.POST.get('reply_text', '')
            floor_id = int(request.POST.get('floor_id', ''))
            floor = Floor.objects.get(id=floor_id)
            comment_id = int(request.POST.get('comment_id'))

            comment = Comment()
            comment.owner = user
            comment.text = text
            comment.floor = floor

            if comment_id != 0:

                obj = Comment.objects.get(id=comment_id)
                comment.by_owner = obj.owner
                data['by_owner'] = obj.owner.username
                data['owner_status'] = True
            else:
                data['owner_status'] = False
            comment.save()

    # referer = request.META.get('HTTP_REFERER', reverse('tiebas:index'))
    # return redirect(referer)
            data['status'] = True
            data['username'] = comment.owner.username
            data['comment_time'] = comment.date_added.strftime('%Y-%m-%d %H:%M:%S')
            data['text'] = comment.text
            data['reply_id'] = comment.id
    else:
        data['status'] = False
    return JsonResponse(data)

def topic_del(request, id):
    if request.method == 'POST':
        topic_id = int(id)
        obj = Topic.objects.get(id=topic_id)
        forum = obj.forum
        forum.topic_count -= 1
        forum.save()
        obj.delete()
        return JsonResponse({'status': 'True'})

def floor_del(request, id):
    if request.method == 'POST':
        floor_id = int(id)
        obj = Floor.objects.get(id=floor_id)
        topic_obj = obj.topic
        topic_obj.floor_count = topic_obj.floor_count-1
        topic_obj.save()
        obj.delete()
        return JsonResponse({'status': 'True'})

def comment_del(request, id):
    if request.method == 'POST':
        comment_id = int(id)
        Comment.objects.get(id=comment_id).delete()
        return JsonResponse({'status': 'True'})

def concerned(request, id):
    if request.method == 'POST':
        obj = UserToForum.objects.filter(forum_id=int(id), user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
        else:
            user_forum = UserToForum()
            forum = Forum.objects.get(id=int(id))
            user_forum.forum = forum
            user_forum.user = request.user
            user_forum.save()


        return JsonResponse({'status': 'True'})

def unconcerned(request, id):
    if request.method == 'POST':
        obj = UserToForum.objects.filter(forum_id=int(id), user=request.user).first()
        obj.status = False
        obj.save()
        return JsonResponse({'status': 'True'})

def collect(request, id):
    if request.method == 'POST':
        obj = Collect.objects.filter(topic_id=int(id), user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
        else:
            collect = Collect()
            topic = Topic.objects.get(id=int(id))
            collect.topic = topic
            collect.user = request.user
            collect.save()

        return JsonResponse({'status': 'True'})

def uncollect(request, id):
    if request.method == 'POST':
        obj = Collect.objects.filter(topic_id=int(id), user=request.user).first()
        obj.status = False
        obj.save()
        return JsonResponse({'status': 'True'})


def change_power(request, id):

    if request.method == 'GET':
        if request.user.power == 4:
            forums = Forum.objects.all()
        else:
            forums = request.user.forum_set.all()
        user = UserInfo.objects.get(id=id)
        context = {'forums': forums, 'user': user}
        return render(request, 'web/change_power.html', context)
    forum_id = request.POST.get('value')
    forum = Forum.objects.get(id=forum_id)
    user = UserInfo.objects.get(id=id)
    obj = ForumPower.objects.filter(forum=forum, user=user).first()
    if not obj:
        obj = ForumPower()
        obj.forum = forum
        obj.user = user
        obj.status = True
        obj.save()
        if user.power < 3:
            user.power = 2
            user.power_name = '版务'
            user.save()
    return JsonResponse({'status': 'True'})

def moderator(request, id):

    if request.method == 'GET':
        forums = Forum.objects.all()
        user = UserInfo.objects.get(id=id)
        context = {'forums': forums, 'user': user}
        return render(request, 'web/change_power.html', context)
    forum_id = request.POST.get('value')
    forum = Forum.objects.get(id=forum_id)
    user = UserInfo.objects.get(id=id)
    forum.moderator = user
    forum.save()
    user.power = 3
    user.power_name = '版主'
    user.save()
    return JsonResponse({'status': 'True'})