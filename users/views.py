from users.models import Drive, Post
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth import authenticate, login as login_User, logout as logout_User
from .forms import ImageForm



# Create your views here.

def home(request):
    return render(request, "users/home.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']    
        password = request.POST['password']
        users = User.objects.filter(email=email).first()
        username = users.username
        user =  authenticate(request, username=username, password=password)
        if user is not None:
            login_User(request, user)
            return redirect(reverse("home"))
        else:
            return render(request, 'users/login.html', {'message': "Invalid Credentials!"})
    
    return render(request, 'users/login.html')


def logout(request):
    logout_User(request)
    return redirect(reverse("home"))

def register(request):
    

    if request.method == 'POST':

        err_lst = []

        username = request.POST['insta']
        fname = request.POST['fullname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        hashed_password = make_password(password1)

        users = User.objects.all()

        if(password1 != password2):
            err_lst.append("Passwords not Matching!")
        if User.objects.filter(username=username).exists():
            err_lst.append("Account with this Instagram Id already exist.")
        if User.objects.filter(email=email).exists():
            err_lst.append("This Email is Already linked to an existing Account.")

        if len(err_lst) == 0:
            u1 = User(username = username, first_name = fname,  email= email, password = hashed_password)
            u1.save()
            print("User created successfully")
            return render (request, 'users/register.html', {'success_message': "Registration Succsessful!"})
        else:
            return render(request, 'users/register.html', {'err_lst': err_lst})

    else:
        return render (request, 'users/register.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse("home"))

    else:
        return render(request, 'users/profile.html', {'isLoggedIn': True})

def createDrive(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    else:
        if request.method == "POST":
            drive = request.POST['drive']
            target = request.POST['target']
            desc = request.POST['desc']
            location = request.POST['location']

            current_user = request.user

            d1 = Drive( drive_name = drive, location = location, target = target, desc = desc)
            d1.save()
            d1.host.add(current_user)
            return render (request, "users/create_drive.html", {"message":"Drive created successfully"})
        return render(request, "users/create_drive.html")

def joinDrive(request):
    context ={'drives' : Drive.objects.all()}
    return render(request, "users/join_drive.html", context)

def ourTeam(request):
    return render(request, "users/our_team.html")



def upload(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        caption = request.POST.get('caption')
        driveName = request.POST.get('driveName')
        post = Post.objects.create(caption=caption) #img=img
        post.save()
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            img_obj = request.FILES.get('image')
            return render(request, 'users/upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'users/upload.html', {'form': form})

def blog_view(request):
    posts = Post.objects.all()
    return render(request, 'users/blog.html', {'posts':posts})

def posts(request):
    current_user = request.user
    context = {
        'posts' : Post.objects.all(),
        'users' : User.objects.all()
    }
    return render(request, 'users/blog.html', context)

def adrive(request):
    return render(request, 'users/drive_temp.html')