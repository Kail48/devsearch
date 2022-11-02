from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
def hello(request):
    projects=project.objects.all()
    print(projects)
    context={'projects':projects}
    return render(request,'projects/hello.html', context)
def project_page(request,pid):
    p=project.objects.get(id=pid)
    tags=p.tags.all()
    context={'project':p,'tags':tags}
    return render(request,'projects/project.html',context)

@login_required(login_url='login')
def create_project(request):
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            return redirect('hello')
    form=ProjectForm()
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def update_project(request,pk):
    p=project.objects.get(id=pk)
    form=ProjectForm(instance=p)
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES,instance=p)
        if form.is_valid:
            form.save()
            return redirect('hello')
    form=ProjectForm()
    context={'form':form}
    return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def delete_project(request,pk):
    p=project.objects.get(id=pk)
    if request.method=='POST':
        p.delete()
        return redirect('hello')
    context={'project':p}
    return render(request,'projects/delete_project.html',context)