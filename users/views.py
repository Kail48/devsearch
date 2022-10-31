import profile
from django.shortcuts import render
from .models import Profile
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