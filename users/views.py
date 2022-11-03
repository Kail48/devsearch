import profile
from django.shortcuts import render,redirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm,ProfileForm
# Create your views here.
def profiles(request):
    all_profiles=Profile.objects.all()
    print(all_profiles)
    context={'profiles':all_profiles}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    u_profile=Profile.objects.get(id=pk)
    topSkills=u_profile.skill_set.exclude(description__exact="")
    otherSkills=u_profile.skill_set.filter(description="")
    context={'profile':u_profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)

def loginPage(request):
    
   
    if request.user.is_authenticated:
        return redirect('profiles') 
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exist")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or password incorrect')
        print(request.POST)
    return render(request,"users/login_register.html")

def logoutUser(request):
    logout(request)
    messages.success(request,'Logged out Succesfully')
    return redirect('login')

def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            print('somehow passed form validation')
            user1=form.save(commit=False)
            user1.username=user1.username.lower()
            user1.save()
            print("saved")
            messages.success(request,"Your account has been created!")
            login(request,user1)
            return redirect('user_account')
        else:
            messages.error(request,"someting wong!")
            context={'page':page,'form':form}
            return render(request,'users/login_register.html',context)
            
    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile=request.user.profile
    topSkills=profile.skill_set.exclude(description__exact="")
    context={'profile':profile,'topSkills':topSkills}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_account')

    
    context={'form':form}
    return render(request,'users/profile_form.html',context)