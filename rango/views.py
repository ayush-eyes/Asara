from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from rango.forms import UserForm, UserProfileForm, CommentForm, ProjectForm, TaskForm, UserUpdateForm
from rango.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User;

# Create your views here.
loggedin_user=None

@login_required
def view_profile(request,user_id_url):
    context = RequestContext(request)
    profile_user = User.objects.get(pk=user_id_url)
    user_profile = UserProfile.objects.get(user=profile_user)
    project_list = Project.objects.filter(project_leader=profile_user)
    project_list1 = []
    for project in Project.objects.all():
        if profile_user in project.project_members.all() and profile_user.username!=project.project_leader.username:
            project_list1.append(project)
    task_list=[]
    for project in project_list1:
        for task in project.project_task.all():
            for USER in task.task_member.all():
                if(USER.username==profile_user.username):
                    task_list.append(task)
    
    for project in project_list:
        for task in project.project_task.all():
            for USER in task.task_member.all():
                if(USER.username==profile_user.username):
                    task_list.append(task)
                    
    
    u = profile_user
    p = UserProfile.objects.get(user=profile_user)
    user_form = UserUpdateForm(initial={'first_name':u.first_name, 'last_name':u.last_name, 'username':u.username,
                                      'email':u.email})
    profile_form = UserProfileForm(initial={'mobile':p.mobile, 'dob':p.dob, 'place':p.place,
                                                'institute':p.institute,'department':p.department, 'gender':p.gender})

    project_form=ProjectForm()
    
    if request.method == 'POST':
        if "edit_profile" in request.POST:
            user_form = UserUpdateForm(data=request.POST, instance=profile_user)
            profile_form = UserProfileForm(request.POST, request.FILES)
            
            if user_form.is_valid() and profile_form.is_valid() :
            
                cd = user_form.cleaned_data
                u = profile_user
                u.first_name = cd['first_name']
                u.last_name = cd['last_name']
                u.email = cd['email']
                u.username = cd['username']
                u.save()
                print(u.username,u.first_name,u.last_name,u.username)
                cd = profile_form.cleaned_data
                p = UserProfile.objects.get(user=profile_user)
                if cd['cv'] != None:
                    p.cv = cd['cv']
                if cd['profile_picture'] != None:
                    p.profile_picture = cd['profile_picture']
                p.mobile = cd['mobile']
                p.dob = cd['dob']
                p.place = cd['place']
                p.institute = cd['institute']
                p.department = cd['department']
                p.save()
                user_profile = UserProfile.objects.get(user=profile_user)
            
            else:
                print user_form.errors
                return HttpResponse("Error in form ")

        elif "create_project" in request.POST:
            form = ProjectForm(request.POST)

            if form.is_valid():
                project = form.save(commit=False)
                project.project_leader = request.user
                notification = Notification()
                notification.save()
                project.project_notification = notification
                project.save()
                project.project_members.add(request.user)
                project.save()
                form.save(commit=True)
                return HttpResponseRedirect("/rango/project/"+str(project.pk))
            else:
                print form.errors

    '''return render_to_response(
            'rango/edit_profile.html',
            {#'first_name':fname, 'last_name':lname, 'username':uname, 'email':email, 'password':password,
             'user_form': user_form, 'profile_form': profile_form},
            context)'''

    
    return render_to_response('rango/view_profile.html',{'profile':user_profile,'profile_user':profile_user,'projects':project_list,
                                                         'projects_as_member':project_list1,'user_form':user_form,'profile_form':profile_form,
                                                         'project_form':project_form,'tasks':task_list, 'id':u.pk ,'loggedin_user':loggedin_user},context)




def user_login(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect("/rango/profile/"+str(request.user.pk))
    if request.method == 'POST':
        if "login" in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    loggedin_user=user
                    print loggedin_user.username
                    return HttpResponseRedirect('/rango/profile/'+str(user.pk))
                else:
                    return HttpResponse("Your Rango account is disabled.")
            else:
                print "Invalid login details: {0}, {1}".format(username, password)
                return HttpResponse("Invalid login details supplied.")


    
        elif "submit" in request.POST:
            registered = False
            print('Hello')
            data1={
                'first_name':request.POST['first_name'],
                'last_name':request.POST['last_name'],
                'email':request.POST['email'],
                'username':request.POST['username'],
                'password':request.POST['pwd']
            }
            user_form = UserForm(data=data1)
            profile_form = UserProfileForm(data=request.POST)
            
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True
                return HttpResponseRedirect('/rango/login/')
            else:
                print user_form.errors, profile_form.errors
                return HttpResponse("Error is found")

            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render_to_response('rango/login.html', {'user_form':user_form,'profile_form':profile_form }, context)

@login_required
def project(request, project_id_url):
    context = RequestContext(request)
    applied=False
    is_member=False
    is_leader=False
    is_other=True
    context_dict = {'project_id':project_id_url}
    project = Project.objects.get(pk=project_id_url)
    members = project.project_members.all()
    applicants = project.project_notification.applicants.all()
    leader = project.project_leader
    curr_user = request.user
    if(curr_user.username==leader.username):
        is_leader=True
        is_other=False
    else:
        if(is_leader!=True):
            for member in members:
                if(member.username == curr_user.username):
                    is_member=True
                    is_other=False

    for USER in applicants:
        if(USER.username==request.user.username):
            applied=True
    data = {
            'task_name':'',
            'task_description':'',
            'task_deadline':'',
            'task_member':members
        }
    if request.method == 'POST':
        if "comment" in request.POST:
            form = CommentForm(request.POST, request.FILES)
        
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comment_user = request.user
                form.save(commit=True)
                project = Project.objects.get(pk=project_id_url)
                tasks = project.project_task.all()
                task_pk = int(request.POST['curr_task'])
                curr_task = tasks.get(pk=task_pk)
                curr_task.task_comment.add(comment)
        elif "add_task" in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                form.save(commit=True)
                project = Project.objects.get(pk=project_id_url)
                project.project_task.add(task)
                return HttpResponseRedirect("/rango/project/%s/"%(project_id_url))
            else :
                return HttpResponseRedirect("")
        
        elif "apply" in request.POST:
            project.project_notification.applicants.add(request.user)
            project.save()
            applied = True
            
        elif "reject_applicant" in request.POST:
            user_pk = int(request.POST['curr_applicant'])
            curr_applicant=User.objects.get(pk=user_pk)
            project.project_notification.applicants.remove(curr_applicant)
            project.project_notification.save()
            project.save()
            applicants=project.project_notification.applicants.all()
            
        elif "accept_applicant" in request.POST:
            user_pk = int(request.POST['curr_applicant'])
            curr_applicant=User.objects.get(pk=user_pk)
            project.project_members.add(curr_applicant)
            project.project_notification.applicants.remove(curr_applicant)
            project.project_notification.save()
            project.save()
            applicants=project.project_notification.applicants.all()
            
        elif "delete_task" in request.POST:
            task_pk = int(request.POST['curr_task'])
            tasks  = project.project_task.all()
            curr_task = tasks.get(pk=task_pk)
            curr_task.task_comment.all().delete()
            curr_task.delete()
            
        elif "complete_task" in request.POST:
            task_pk = int(request.POST['curr_task'])
            tasks = project.project_task.all()
            curr_task = tasks.get(pk=task_pk)
            curr_task.task_complete = True
            curr_task.save()
            
        elif "delete_project" in request.POST:
            tasks = project.project_task.all()
            for task in tasks:
                task.task_comment.all().delete()
            project.project_task.all().delete()
            project.project_notification.delete()
            project.delete()
            return HttpResponseRedirect("/rango/profile/"+str(request.user.pk))
            
        else:
            form = ProjectForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                project.project_name = cd['project_name']
                project.project_description = cd['project_description']
                project.project_department = cd['project_department']
                project.save()
                
    if 'curr_user' in request.GET and request.GET['curr_user']:
        if request.user.username==project.project_leader.username:
            print("HELLO WORLD")
            user_pk = int(request.GET['curr_user'])
            print(user_pk)
            user = User.objects.get(pk=user_pk)
            project.project_members.add(user)
            print(project.project_members)
            project.save()
            
    elif 'curr_member' in request.GET and request.GET['curr_member']:
        if request.user.username==project.project_leader.username:
            print("HELLO WORLD")
            user_pk = int(request.GET['curr_member'])
            task_pk = int(request.GET['curr_task'])
            print(user_pk)
            user = User.objects.get(pk=user_pk)
            curr_task = Task.objects.get(pk=task_pk)
            curr_task.task_member.add(user)
            curr_task.save()
            
            
    project = Project.objects.get(pk=project_id_url)
    members = project.project_members.all()
            
    try:
        data = {
                'project_name':project.project_name,
                'project_description':project.project_description,
                'project_department':project.project_department,
                'project_members':members,
            }
        project = Project.objects.get(pk=project_id_url)
        tasks = project.project_task
        context_dict['project'] = project
        context_dict['tasks'] = tasks
        context_dict['comment'] = CommentForm()
        context_dict['add_task'] = TaskForm(request.POST)
        context_dict['form'] = ProjectForm(data)
        context_dict['applied'] = applied
        context_dict['applicants'] = applicants
        context_dict['is_member']=is_member
        context_dict['is_leader']=is_leader
        context_dict['is_other']=is_other
        
    except Project.DoesNotExist:
        pass
    return render_to_response('rango/project.html',context_dict,context)

    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango/login/")

@login_required
def search_titles(request):
    if request.method=="POST":
        search_text=request.POST['search_text']
        print search_text
        
    else:
        search_text=None
    
    projects1=Project.objects.all()
    print(projects1)
    projects=Project.objects.filter(project_name__contains=search_text)
    print(projects)
    if(search_text==''):
        projects=[]
    return render_to_response('rango/ajax_search.html',{'projects':projects})
    
@login_required
def search_profiles(request):
    if request.method=="GET":
        user_search_text=request.GET['user_search_text']
        project_id=request.GET['project_id']
    else:
        user_search_text=None
    project=Project.objects.get(pk=project_id)
    project_members = project.project_members.all()
    users=User.objects.filter(username__contains=user_search_text)
    users1=User.objects.all()
    L=[]
    for user in users:
        if(user not in project_members):
            L.append(user)
    if (user_search_text==''):
        L=[]
        
    return render_to_response('rango/user_search.html',{'users':L,'project_id':project_id})

@login_required
def add_member(request):
    if request.method=="GET":
        user_search_text=request.GET['task_add_people']
        task_id=request.GET['task_id']
        project_id=request.GET['project_id']
    else:
        user_search_text=None
    
    
    project=Project.objects.get(pk=project_id)
    project_members=project.project_members.all()
    task=Task.objects.get(pk=task_id)
    task_members=task.task_member.all()
    L=[]
    for member in project_members:
        if(member not in task_members):
            L.append(member)
    G=[]
    for member in L:
        if(user_search_text in member.username):
            G.append(member)
    if(user_search_text==''):
        G=[]
        
    return render_to_response('rango/task_add_people.html',{'project_members':G , 'task_id':task_id , 'project_id':project_id})