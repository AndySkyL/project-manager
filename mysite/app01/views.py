from django.shortcuts import render, HttpResponse, redirect, reverse
from app01 import models


def login_required(func):
    def inner(request, *args, **kwargs):
        if not request.session.get('user',None):
            print(request.session.get('user'))
            url = request.path_info
            full_login_url = reverse('login_url')+'?next={}'.format(url)
            print(full_login_url)
            return redirect(full_login_url)
        ret = func(request, *args, **kwargs)
        return ret

    return inner


def index(request):
    return render(request, 'index.html')


def logout(request):
    ret = redirect('login_url')
    request.session.flush()
    return ret


def login(request):
    err_msg = ''
    if request.method == 'POST':
        # 获取提交的数据
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if models.user.objects.filter(name=user, pwd=pwd):
            url = request.GET.get('next')
            print(url)
            if url:
                ret = redirect(url)
            else:
                ret = redirect(reverse('project'))

            request.session['user'] = user
            return ret

        else:
            err_msg = '用户名或者密码错误！'

    # 返回一个页面
    return render(request, 'login.html', {'err_msg': err_msg})


@login_required
def project(request):
    projects = models.Publish.objects.all()
    return render(request, 'project.html', locals())


from django.views.decorators.csrf import csrf_exempt,csrf_protect

@ csrf_exempt
# @login_required
def add_project(request):
    err_msg = ''
    if request.method == 'POST':
        new_project = request.POST.get('new_project')

        if not new_project:
            err_msg = '不能为空!'

            return render(request, 'add_project.html', {'err_msg': err_msg})

        object_project = models.Publish.objects.filter(name=new_project)

        if object_project:
            err_msg = '项目已经存在！'

        else:
            models.Publish.objects.create(name=new_project)
            return redirect('project')
    return render(request, 'add_project.html', {'err_msg': err_msg})


@login_required
def update_project(request, pk):
    err_msg = ''
    obj = models.Publish.objects.get(pk=pk)

    if request.method == 'POST':
        new_project = request.POST.get('new_project')

        if not new_project:
            err_msg = '不能为空!'

            return render(request, 'update_project.html', {'pk': pk, 'obj': obj, 'err_msg': err_msg})

        object_project = models.Publish.objects.filter(name=new_project)

        if object_project:
            err_msg = '项目已经存在!'

        else:
            obj.name = new_project
            obj.save()
            return redirect('project')

    return render(request, 'update_project.html', {'pk': pk, 'obj': obj, 'err_msg': err_msg})


@login_required
def del_project(request, pk):
    obj = models.Publish.objects.get(pk=pk)
    obj.delete()

    return redirect(reverse('project'))


from django.views import View
from django.utils.decorators import method_decorator

@method_decorator(login_required,name='get')
class Host_info(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        host_list = models.Hostlist.objects.all()
        return render(request, 'hostinfo.html', {'host_list': host_list})

    def post(self, request):
        pass


class Add_host(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        project_item = models.Publish.objects.all()
        return render(request, 'add_host.html', {'project_item': project_item})

    def post(self, request):
        hostname = request.POST.get('hostname')
        ipaddr = request.POST.get('ipaddr')
        pro_id = request.POST.get('pro')

        models.Hostlist.objects.create(hostname=hostname, ip_addr=ipaddr,
                                       project=models.Publish.objects.get(pk=pro_id))
        # models.Hostlist.objects.create(hostname=hostname, ip_addr=ipaddr, project_id=project)

        return redirect(reverse('host_info'))


class Edit_host(View):
    http_method_names = ['get', 'post']

    def get(self, request, pk):
        project_item = models.Publish.objects.all()
        obj_host = models.Hostlist.objects.get(pk=pk)
        return render(request, 'edit_host.html', {'pk': pk, 'obj_host': obj_host, 'project_item': project_item})

    def post(self, request, pk):
        obj_host = models.Hostlist.objects.get(pk=pk)
        hostname = request.POST.get('hostname')
        ipaddr = request.POST.get('ipaddr')
        pro_id = request.POST.get('pro')

        obj_host.hostname = hostname
        obj_host.ip_addr = ipaddr
        obj_host.project_id = pro_id

        obj_host.save()

        return redirect(reverse('host_info'))


class Del(View):
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        ret = super().dispatch(request,*args,**kwargs)
        print('this is Del dispatch')
        return ret

    def get(self, request, table, pk):
        table_class = getattr(models, table.capitalize())
        table_class.objects.filter(pk=pk).delete()
        return redirect(reverse('host_info'))
