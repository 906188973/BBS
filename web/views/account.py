from django.shortcuts import render, redirect
from web.form.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from web.form.account import HeadForm, PasswordForm, AccountForm
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
    """退出"""
    request.session.flush()
    return redirect('web:home')

def account(request):
    """个人页"""
    head_form = HeadForm()
    password_form = PasswordForm(request)
    user = request.user
    account_form = AccountForm(request, instance=user)
    context = {'head_form': head_form, 'password_form': password_form, 'account_form': account_form}
    return render(request, 'web/account.html', context)

def headupdate(request):
    """更新头像"""
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

def passwordupdate(request):
    """更新密码"""
    if request.method == 'POST':
        form = PasswordForm(request, data=request.POST)
        if form.is_valid():
            obj = models.UserInfo.objects.get(id=request.user.id)
            obj.password = form.cleaned_data['new_password']
            obj.save()

            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'error': form.errors})

def accountupdate(request):
    """更新密码"""
    if request.method == 'POST':
        form = AccountForm(request, data=request.POST)
        if form.is_valid():
            user = models.UserInfo.objects.get(id=request.user.id)
            user.username = form.cleaned_data['username']
            user.describe = form.cleaned_data['describe']
            user.save()

            return JsonResponse({'status': True})
        return JsonResponse({'status': False, 'error': form.errors})

def other(request, id):
    """他人个人页"""
    user = models.UserInfo.objects.get(id=id)
    context = {'user': user}
    obj = models.UserToUser.objects.filter(by_owner=int(id), user=request.user).first()

    if not obj:
        status = False
    else:
        status = obj.status
    context['status'] = status
    return render(request, 'web/other.html', context)

def concerned_user(request, id):
    """关注"""
    if request.method == 'POST':
        obj = models.UserToUser.objects.filter(by_owner=int(id), user=request.user).first()
        if obj:
            obj.status = True
            obj.save()
        else:
            usertouser = models.UserToUser()
            by_owner = models.UserInfo.objects.get(id=int(id))
            if by_owner == request.user:
                return JsonResponse({'status': 'False'})
            usertouser.user = request.user
            usertouser.by_owner = by_owner
            usertouser.save()

        return JsonResponse({'status': 'True'})

def unconcerned_user(request, id):
    """取消关注"""
    if request.method == 'POST':

        obj = models.UserToUser.objects.filter(by_owner=int(id), user=request.user).first()
        obj.status = False
        obj.save()
        return JsonResponse({'status': 'True'})