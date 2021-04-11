from django.shortcuts import render, redirect
from web.form.bbs import ForumForm, TopicForm, FloorForm
from django.http import JsonResponse, HttpResponseRedirect
from web.models import Topic, Forum, Floor, Comment, UserToForum, Collect, UserInfo, ForumPower
from web.models import FloorGreat, CommentGreat
from django.db.models import Max
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt

def create_forum(request):
    """创建版块"""
    if request.method == 'GET':
        form = ForumForm()
        context = {'form': form}
        return render(request, 'web/create_forum.html', context)
    form = ForumForm(request.POST, request.FILES)
    if form.is_valid():
        forum = form.save(commit=False)
        forum.moderator = request.user
        forum.save()
        # return JsonResponse({'status': True, 'data': '/'})
    return redirect('web:home')
    # return JsonResponse({'status': False, 'error': form.errors})

def fourm(request, forum_id):
    """显示所有帖子主题"""
    forum = Forum.objects.get(id=forum_id)
    topics = forum.topic_set.order_by('-top', 'date_added')
    obj = UserToForum.objects.filter(user=request.user, status=True).all()

    # 将数据按照规定每页显示 10 条, 进行分割
    paginator = Paginator(topics, 5)

    user_forum = []
    for i in obj:
        user_forum.append(i.forum.id)
    """创建新贴"""
    if request.method != 'POST':
        form_topic = TopicForm()
        form_floor = FloorForm()
        topic_count = 0
        for i in topics:
            topic_count += i.floor_count
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            topic_page = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            topic_page = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            topic_page = paginator.page(paginator.num_pages)
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
    context = {'forum': forum, 'form_topic': form_topic, 'form_floor': form_floor, 'topic_page':topic_page}
    context['user_forum'] = user_forum
    context['topic_count'] = topic_count
    if topics:
        context['topics'] = topics
    return render(request, 'web/topics.html', context)

def topic_del(request, id):
    """删除帖子"""
    if request.method == 'POST':
        topic_id = int(id)
        obj = Topic.objects.get(id=topic_id)
        forum = obj.forum
        forum.topic_count -= 1
        forum.save()
        obj.delete()
        return JsonResponse({'status': 'True'})

def topic(request, topic_id):
    """显示帖子"""
    topic = Topic.objects.get(id=topic_id)
    floors = topic.floor_set.order_by('date_added')
    obj = Collect.objects.filter(user=request.user, status=True).all()
    collect = []
    for i in obj:
        collect.append(i.topic.id)

    obj = UserToForum.objects.filter(user=request.user, status=True).all()
    user_forum = []
    for i in obj:
        user_forum.append(i.forum.id)

    obj = FloorGreat.objects.filter(user=request.user, status=True).all()
    floorgreat = []
    for i in obj:
        floorgreat.append(i.floor.id)

    obj = CommentGreat.objects.filter(user=request.user, status=True).all()
    commentgreat = []
    for i in obj:
        commentgreat.append(i.comment.id)

    paginator = Paginator(floors, 2)
    """回复帖子"""
    if request.method != 'POST':
        form = FloorForm()
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            floors_page = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            floors_page = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            floors_page = paginator.page(paginator.num_pages)
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
    context['floorgreat'] = floorgreat
    context['commentgreat'] = commentgreat
    context['floors_page'] = floors_page
    context['user_forum'] = user_forum
    return render(request, 'web/topic.html', context)

def floor_del(request, id):
    """删除楼层"""
    if request.method == 'POST':
        floor_id = int(id)
        obj = Floor.objects.get(id=floor_id)
        topic_obj = obj.topic
        topic_obj.floor_count = topic_obj.floor_count-1
        topic_obj.save()
        obj.delete()
        return JsonResponse({'status': 'True'})

def update_comment(request):
    """加评论"""
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

def comment_del(request, id):
    """删除评论"""
    if request.method == 'POST':
        comment_id = int(id)
        Comment.objects.get(id=comment_id).delete()
        return JsonResponse({'status': 'True'})

def concerned(request, id):
    """关注"""
    if request.method == 'POST':
        obj = UserToForum.objects.filter(forum_id=int(id), user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
            forum = Forum.objects.get(id=int(id))
            forum.concern_count += 1
            forum.save()
        else:
            user_forum = UserToForum()
            forum = Forum.objects.get(id=int(id))
            user_forum.user = request.user
            user_forum.forum = forum
            user_forum.save()

            forum.concern_count += 1
            forum.save()


        return JsonResponse({'status': 'True'})

def unconcerned(request, id):
    """取消关注"""
    if request.method == 'POST':
        forum = Forum.objects.get(id=int(id))
        forum.concern_count -= 1
        forum.save()

        obj = UserToForum.objects.filter(forum_id=int(id), user=request.user).first()
        obj.status = False
        obj.save()
        return JsonResponse({'status': 'True'})

def collect(request, id):
    """收藏"""
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
    """取消收藏"""
    if request.method == 'POST':
        obj = Collect.objects.filter(topic_id=int(id), user=request.user).first()
        obj.status = False
        obj.save()
        return JsonResponse({'status': 'True'})


def change_power(request, id):
    """更改权限"""
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
    """设置版主"""
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

def floor_great(request, id):
    """楼层点赞"""
    if request.method == 'POST':
        floor = Floor.objects.get(id=id)
        floor.great += 1
        floor.save()

        obj = FloorGreat.objects.filter(floor=floor, user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
        else:
            obj = FloorGreat()
            obj.floor = floor
            obj.user = request.user
            obj.save()

        return JsonResponse({'status': 'True'})

def unfloor_great(request, id):
    """取消楼层点赞"""
    if request.method == 'POST':
        floor = Floor.objects.get(id=id)
        floor.great -= 1
        floor.save()

        obj = FloorGreat.objects.filter(floor=floor, user=request.user).first()
        obj.status = False
        obj.save()

        return JsonResponse({'status': 'True'})

def comment_great(request, id):
    """评论点赞"""
    if request.method == 'POST':
        comment = Comment.objects.get(id=id)
        comment.great += 1
        comment.save()

        obj = CommentGreat.objects.filter(comment=comment, user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
        else:
            obj = CommentGreat()
            obj.comment = comment
            obj.user = request.user
            obj.save()

        return JsonResponse({'status': 'True'})

def uncomment_great(request, id):
    """取消评论点赞"""
    if request.method == 'POST':
        comment = Comment.objects.get(id=id)
        comment.great -= 1
        comment.save()

        obj = CommentGreat.objects.filter(comment=comment, user=request.user).first()
        obj.status = False
        obj.save()

        return JsonResponse({'status': 'True'})

def top(request):
    """置顶"""
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        topic = Topic.objects.get(id=id)
        topic.top = True
        topic.save()
        return JsonResponse({'status': 'True'})

def untop(request):
    """取消置顶"""
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        topic = Topic.objects.get(id=id)
        topic.top = False
        topic.save()
        return JsonResponse({'status': 'True'})

def refined(request):
    """加精"""
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        topic = Topic.objects.get(id=id)
        topic.refined = True
        topic.save()
        return JsonResponse({'status': 'True'})

def unrefined(request):
    """取消加精"""
    if request.method == 'POST':
        id = int(request.POST.get('id'))
        topic = Topic.objects.get(id=id)
        topic.refined = False
        topic.save()
        return JsonResponse({'status': 'True'})