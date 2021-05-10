from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from web.form.manage import InformFloorForm
from web.models import Floor, Inform_Floor, ApplyforForum, Forum, Topic
from web.form.bbs import TopicchangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from web import models

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
    count = len(topics)
    paginator = Paginator(topics, 20)
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
    context = {'count': count, 'topic_page': topic_page}
    return render(request, 'web/manage_topic.html', context)

def manage_floor(request):
    if request.user.power == 1 or not request.user:
        return redirect('web:home')
    if request.user.power == 2:
        forums = Forum.objects.filter(moderator=request.user)
        topics = []
        for i in forums:
            topics += i.topic_set.all()
        floors = []
        for i in topics:
            floors += i.floor_set.all()
    else:
        floors = models.Floor.objects.all()
    count = len(floors)
    paginator = Paginator(floors, 20)
    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        floor_page = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        floor_page = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        floor_page = paginator.page(paginator.num_pages)
    context = {'count': count, 'floor_page': floor_page}
    return render(request, 'web/manage_floor.html', context)

def manage_forum(request):
    if request.user.power != 3:
        return redirect('web:home')
    forums = Forum.objects.all()
    count = len(forums)
    paginator = Paginator(forums, 20)
    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        forum_page = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        forum_page = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        forum_page = paginator.page(paginator.num_pages)
    context = {'count': count, 'forum_page': forum_page}
    return render(request, 'web/manage_forum.html', context)

def manage_user(request):
    if request.user.power != 3:
        return redirect('web:home')
    user = models.UserInfo.objects.all()
    count = len(user)
    paginator = Paginator(user, 20)
    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        user_page = paginator.page(page)
    # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        user_page = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        user_page = paginator.page(paginator.num_pages)
    context = {'count': count, 'user_page': user_page}
    return render(request, 'web/manage_user.html', context)

def forum_del(request, id):
    """删除版块"""
    if request.method == 'POST':
        forum_id = int(id)
        obj = Forum.objects.get(id=forum_id)
        obj.delete()
        return JsonResponse({'status': 'True'})

def user_del(request, id):
    """删除用户"""
    if request.method == 'POST':
        user_id = int(id)
        obj = models.UserInfo.objects.get(id=user_id)
        obj.delete()
        return JsonResponse({'status': 'True'})