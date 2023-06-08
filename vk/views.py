from django.shortcuts import render,redirect,resolve_url
from django.http import Http404, HttpResponse
from django.db.models import Q
from . import models
from . import forms



def data(request):
    return HttpResponse(1)

def feed(request):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    posts = models.Post.objects.all().order_by('-date')
    context['posts'] = posts
    return render(request, 'vk/feed.html', context=context)

def login(request):
    if request.method == 'GET':
        loginForm = forms.LoginForm().as_p
        context = {'login_form': loginForm}
        return render(request, 'vk/login.html', context=context)
    
    loginForm = forms.LoginForm(request.POST)
    if loginForm.is_valid():
        session = request.session
        username = loginForm.cleaned_data['username']
        user = models.User.objects.get(username = username)
        session['user_id'] = user.pk
        return redirect('feed')

    context = {'login_form': loginForm.as_p}
    return render(request, 'vk/login.html', context=context)


def signout(request):
    session = request.session
    if not 'user_id' in session:
        return redirect('login')
    
    del session['user_id']
    return redirect('login')


def register(request):
     if request.method == 'GET':
        registerForm = forms.RegisterForm().as_p
        context = {'register_form': registerForm}
        return render(request, 'vk/register.html', context=context)
     
     registerForm = forms.RegisterForm(request.POST)
     if registerForm.is_valid():
        user = registerForm.save()
        return redirect('login')

     context = {'register_form': registerForm.as_p} 
     return render(request, 'vk/register.html', context=context)


def profile(request, username = None):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    loginUser = context['user']
    profileUser = None
    is_self = False
    is_friend = False

    if username ==None:
        profileUser = loginUser
        is_self = True

    if profileUser == None:
        findUsers = models.User.objects.filter(username = username)
        if not findUsers.exists:
            raise Http404('No such user')
        
        profileUser = models.User.objects.get(username = username)

    if profileUser == loginUser:
        is_self = True

    firend1 = models.Friend.objects.filter(user1=loginUser, user2=profileUser)
    firend2 = models.Friend.objects.filter(user1=profileUser, user2=loginUser)
    is_send = models.FriendRequest.objects.filter(request_sender= loginUser, request_reciver = profileUser).exists()

    if firend1.exists() or firend2.exists():
        is_friend = True

    posts = models.Post.objects.filter(user=profileUser).order_by('-date')
    context['is_self'] = is_self
    context['is_friend'] = is_friend
    context['is_send'] = is_send
    context['profile_user'] = profileUser
    context['posts'] = posts
        
    return render(request, 'vk/profile.html', context=context)


def newpost(request):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    if request.method == 'GET':
        return render(request, 'vk/newpost.html', context=context)
    
    description = request.POST['description']
    image_file = request.FILES['image']
    print(type(image_file))
    user = context['user']
    post = models.Post()
    post.user = user
    post.description = description
    post.media.save(image_file.name, image_file)
    post.save()

    return redirect('profile')

def sendRequest(request, username=None):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    if username == None:
        return redirect('feed')
    
    user = models.User.objects.get(username=username)
    fr_request = models.FriendRequest()
    fr_request.request_sender = context['user']
    fr_request.request_reciver = user
    fr_request.save()
    return redirect(resolve_url('profile',username=user.username))


def friends(request):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    user = context['user']
    requests = models.FriendRequest.objects.filter(request_reciver = user)
    friends1 = models.Friend.objects.filter(user2=user)
    friends2 = models.Friend.objects.filter(user1=user)
    context['requests'] = requests
    context['friends1'] = friends1
    context['friends2'] = friends2
    return render(request, 'vk/friends.html', context)


def friendsCtrl(request, username = None, method = None):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    if username == None or method == None:
        return redirect('feed')
    
    friend = models.User.objects.get(username=username)
    user = context['user']
    
    if method == 'accept':
        fr_request = models.FriendRequest.objects.get(request_sender= friend, request_reciver = user)
        fr_request.delete()
        friend_model = models.Friend()
        friend_model.user1 = user
        friend_model.user2 = friend
        friend_model.save()
        return redirect('friends')
    
    elif method == 'decline':
        fr_request = models.FriendRequest.objects.get(request_sender= friend, request_reciver = user)
        fr_request.delete()
        return redirect('friends')
    
    elif method == 'delete':
        friends = models.Friend.objects.filter(user1=user, user2=friend)
        if friends.exists():
            friends = models.Friend.objects.get(user1=user, user2=friend)
            friends.delete()
        else:
            friends = models.Friend.objects.get(user1=friend, user2=user)
            friends.delete()
    
    
    
    return redirect('friends')

def allUsers(request):
    context = checkSession(request)
    if not context:
        return redirect('login')
    
    allUsers = models.User.objects.all()
    context['users'] = allUsers
    return render(request, 'vk/allusers.html', context=context)

def checkSession(request):
    session = request.session
    if not 'user_id' in session:
        return False
    
    user = models.User.objects.get(pk=session['user_id'])
    context = {
        'user':user
    }

    return context

