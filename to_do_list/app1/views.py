from django.shortcuts import render,redirect
from .models import Members,Task
from django.http import JsonResponse
from django.template.loader import render_to_string

from .decorators import login_check

import re
# Create your views here.
def home(request):
    return render(request,'app1/home.html')

def signin_register(request):
    def validate_details(name,email,password):
        errors={}
        if not re.match('^[a-zA-Z0-9]+$',name):
            errors['name']='Invalid name. Use only letters and digits.'
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",email):
            errors['email']="Email is invalid. Please enter a valid email address."
        elif Members.objects.filter(email=email).exists():
            errors['email']="Email already Exists."
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",password):
            errors['password']="Invalid password. should contain letter,digit,special charater, length at least 8."
        return errors
    
    #actual start of function

    if request.method=='POST':
        if 'signin' in request.POST:
            email=request.POST['logemail']
            password=request.POST['logpass']
            try:
                 member=Members.objects.get(email=email,password=password)
                 if member:
                     request.session['ActiveUserEmail']=email
                     request.session['ActiveUserName']=member.name
                     return redirect('app1:all_tasks')
            except Members.DoesNotExist as e:
                response=redirect('app1:sign_in')
                response.set_cookie('msg_info','Invalid Email or Password.',5)
                return response
        if 'register' in request.POST:
            
            name=request.POST['logname']
            email=request.POST['logemail']
            password=request.POST['logpass']
            errors=validate_details(name,email,password)
            if errors:
                response=redirect('app1:sign_in')
                for key in errors.keys():
                    response.set_cookie(f'{key}_error',errors[key],15)
                for key in ['name','password','email']:
                    response.set_cookie(f'{key}',request.POST[f'log{key[:5] if key.endswith('l') else key[:4]}'],5)
                return response
            new_user=Members(name=name,email=email,password=password)
            new_user.save()
            response=redirect('app1:sign_in')
            response.set_cookie('msg_alert','Registration Successful, Please Log in.',5)
            return response
    return render(request,'app1/signin_register.html')

@login_check
def all_tasks(request):
    email=request.session['ActiveUserEmail']
    user=Members.objects.get(email=email)
    if request.method=='POST':
        task=request.POST['task']
        new_task=Task(user=user,title=task)
        new_task.save()
        return redirect('app1:all_tasks')
    tasks=Task.objects.filter(user=user)
    context={
        'name':user.name,
        'tasks':tasks
    }
    return render(request,'app1/all_tasks.html',context)

@login_check
def delete_task(request,pk):
    email=request.session['ActiveUserEmail']
    user=Members.objects.get(email=email)
    try:
        task=Task.objects.get(user=user,pk=pk)
        task.delete()
    except Task.DoesNotExist as e:
        pass
    return redirect('app1:all_tasks')

@login_check
def update_task(request,pk):
    email=request.session['ActiveUserEmail']
    user=Members.objects.get(email=email)
    try:
        task=Task.objects.get(user=user,pk=pk)
    except Task.DoesNotExist as e:
        pass

    context={
        'task':task
    }
    return render(request,'app1/update_task.html',context)

@login_check
def update_title(request):
    if request.method=='POST':
        pk=int(request.POST['pk'])
        updated_title=request.POST['task']
        task=Task.objects.get(pk=pk)
        task.title=updated_title
        task.save()
        return redirect('app1:all_tasks')

@login_check
def logout(request):
    if 'ActiveUserEmail' in request.session:
        del request.session['ActiveUserEmail']
        del request.session['ActiveUserName']
        response=redirect('app1:sign_in')
        response.set_cookie('msg_info','Logout Successfully.',5)
    else:
        response=redirect('app1:sign_in')
        response.set_cookie('msg_info','You are not Logged in.',5)
    return response
@login_check
def update_completed_status(request):
    print('I am here 1')
    email=request.session['ActiveUserEmail']
    task_pk=request.POST.get('task_pk','')
    completed_status=eval(request.POST['completed_status'])
    print(email,task_pk,completed_status)
    if task_pk:
        try:
            task=Task.objects.get(pk=task_pk)
            print('I am here 2')
        except Task.DoesNotExist:
            pass
        else:
            print('I am here 3')
            task.completed_status=not completed_status
            task.save()
            tasks=Task.objects.filter(user=email).order_by('-pk')
            tbody_html = render_to_string('app1/ajax/tbody.html', {'tasks': tasks})
            print('I am here 4')
            return JsonResponse({'completed_status_change':True,'tbody_html':tbody_html})
    print('I am here 5')
    return JsonResponse({'error': 'Invalid request'})