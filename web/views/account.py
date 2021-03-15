from django.shortcuts import render, redirect
from web.form.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from web.form.account import HeadForm
from django.http import HttpResponse, JsonResponse
from web import models
from django.db.models import Q
import datetime



def register(request):
    """注册"""
    if request.method == 'GET':
        form = RegisterModelForm()
        context = {'form': form}
        return render(request, 'web/register.html', context)

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        #注册完成直接登录
        username = form.cleaned_data['username']
        user_obj = models.UserInfo.objects.get(username=username)
        request.session['user_id'] = user_obj.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        return JsonResponse({'status': True, 'data': '/'})
    return JsonResponse({'status': False, 'error': form.errors})

def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    print('选择')
    if form.is_valid():
        return JsonResponse({'status': True})
    print('成功')
    return JsonResponse({'status': False, 'error': form.errors})

def login_sms(request):
    """短信登录"""
    if request.method == 'GET':
        form = LoginSMSForm()
        context = {'form': form}
        return render(request, 'web/login_sms.html', context)
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        #用户输入正确， 登录成功
        mobile_phone = form.cleaned_data['mobile_phone']
        #把用户名写入到session中
        user_object = models.UserInfo.objects.get(mobile_phone=mobile_phone)
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        return JsonResponse({"status": True, 'data': "/"})
    return JsonResponse({"status": False, "error": form.errors})

def login(request):
    """用户名和密码登录"""
    form = LoginForm(request)
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_obj = models.UserInfo.objects.filter(
                Q(email=username)|Q(mobile_phone=username)).filter(
                password=password).first()
            if user_obj:
                #登录成功
                request.session['user_id'] = user_obj.id
                request.session.set_expiry(60 * 60 * 24 * 14)
                return redirect('web:home')
            form.add_error('username', '用户名或密码错误')
    context = {'form': form}
    return render(request, 'web/login.html', context)

def image_code(request):
    """生成图片验证码"""
    from io import BytesIO
    from utils.image_code import check_code

    image_object, code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.flush()
    return redirect('web:home')

def account(request):
    return render(request, 'web/account.html')

def headupload(request):
    if request.method == 'POST':
        # 取出文件后缀名,这里前端给我传的文件key为`文件`,大部分默认文件key为`file`
        fmt = str(request.FILES.get('head_portrait').name).split('.')[-1]
        # 设置文件名`用户特征信息`是我自己定义的变量,你可以在这里设置你需要传入的变量
        name = "{}.{}".format(request.user.username, fmt)
        # 修改文件名直接让文件.name等于新的文件名即可
        request.FILES.get('head_portrait').name = name
        img = request.FILES.get('head_portrait', '')

        id = request.user.id
        obj = models.UserInfo.objects.get(id=id)
        obj.head_portrait = img
        obj.save()
        return redirect('web:account')
    form = HeadForm()
    context = {'form': form}
    return render(request, 'web/headupload.html', context)

def other(request, id):
    user = models.UserInfo.objects.get(id=id)
    context = {'user': user}
    return render(request, 'web/other.html', context)