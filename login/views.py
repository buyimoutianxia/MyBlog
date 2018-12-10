from django.shortcuts import render, redirect
import hashlib

from . import forms
from . import models
# Create your views here.

def index(request):
    pass
    return render(request, 'login/index.html', locals())

def login(request):
    if request.session.get('is_login',None):
        return redirect('index')
    if request.method =='POST':
        login_form = forms.UserForms(request.POST)
        message = '登录成功'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return  redirect("index")
                else:
                    message = '密码错误'
            except:
                message = '用户名不存在'
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForms()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('index')
    if request.method =='POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            #校验用户名是否已被注册
            same_user_name = models.User.objects.filter(name=username)
            if same_user_name:
                message = '用户名已存在'
                return render(request, 'login/register.html', locals())
            #校验两次输入的密码是否一致
            if password1 != password2:
                message = '两次密码不一致'
                return render(request, 'login/register.html', locals())
            #校验邮箱是否已被注册
            if models.User.objects.filter(email=email):
                message = '该邮箱已被注册'
                return render(request, 'login/register.html', locals())
            #生成用户信息
            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password2)
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('login')

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('index')
    request.session.flush()
    return redirect('index')

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
