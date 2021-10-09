from users.models import Drive,  Profile
from posts.models import Post1
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth import authenticate, login as login_User, logout as logout_User

# from .forms import ImageForm



# Create your views here.

def home(request):
    return render(request, "users/home.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']    
        password = request.POST['password']
        users = User.objects.filter(email=email).first()
        if users is not None:
            username = users.username
            user =  authenticate(request, username=username, password=password)
            if user is not None:
                print("user is not none true")
                login_User(request, user)
                return redirect(reverse("home"))
            else:
                print("error message wala")
                return render(request, 'users/home.html', {'message': "Invalid Credentials!"})
        else:
            return render(request, 'users/home.html', {'message': "Invalid Credentials!"})
    print("not post")
    return redirect(reverse("home"))



def logout(request):
    logout_User(request)
    return redirect(reverse("home"))

def register(request):
    

    if request.method == 'POST':

        err_lst = []

        username = request.POST['email']
        fname = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        location = request.POST['location']
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
            p1 = Profile(user = u1, location = location)
            p1.save()
            print("User created successfully")
            return render (request, 'users/home.html', {'message': "Registration Succsessful! Please Login"})
        else:
            return render(request, 'users/register.html', {'err_lst': err_lst})

    else:
        return render (request, 'users/register.html')


def profile(request):
    if not request.user.is_authenticated:
        return redirect(reverse("home"))

    else:
        p = Profile.objects.get(user = request.user)
        userDrives = request.user.in_drives.all()
        context = {'profile': p, 'isLoggedIn': True, 'userDrives':userDrives}
        return render(request, 'users/profile.html', context)

def createDrive(request):
    if not request.user.is_authenticated:
        return render(request, "users/home.html", {"message":"Please Login!"})
    else:
        if request.method == "POST":
            drive = request.POST['drive']
            target = request.POST['target']
            desc = request.POST['desc']
            location = request.POST['location']

            current_user = request.user

            d1 = Drive(host =current_user, drive_name = drive, location = location, target = target, desc = desc)
            d1.save()
            d1.members.add(current_user)

            return render (request, "users/create_drive.html", {"message":"Drive created successfully"})
        return render(request, "users/create_drive.html")

def joinDrive(request):
    if not request.user.is_authenticated:
        return render(request, "users/home.html", {"message":"Please Login!"})
    else:
        context ={'drives' : Drive.objects.all()}
        return render(request, "users/join_drive.html", context)

def ourTeam(request):
    return render(request, "users/our_team.html")



# def upload(request):
#     """Process images uploaded by users"""
#     if request.method == 'POST':
#         caption = request.POST.get('caption')
#         driveName = request.POST.get('driveName')
#         post = Post.objects.create(caption=caption) #img=img
#         post.save()
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             img_obj = form.instance
#             img_obj = request.FILES.get('image')
#             return render(request, 'users/upload.html', {'form': form, 'img_obj': img_obj})
#     else:
#         form = ImageForm()
#     return render(request, 'users/upload.html', {'form': form})

# def blog_view(request):
#     posts = Post.objects.all()
#     return render(request, 'users/blog.html', {'posts':posts})

# def posts(request):
#     current_user = request.user
#     context = {
#         'posts' : Post.objects.all(),
#         'users' : User.objects.all()
#     }
#     return render(request, 'users/blog.html', context)

def indi_drive_join(request, drive_pk):
    drive = Drive.objects.get(pk=drive_pk)
    inDrive = False
    if request.user in drive.members.all():
        inDrive = True
    context = {'drive': drive, 'inDrive':inDrive}
    if request.method == 'POST':
        drive.members.add(request.user)
        inDrive = True
        context = {'drive': drive, 'inDrive':inDrive}
        return render(request, 'users/drive_temp.html', context)
    return render(request, 'users/drive_temp.html', context)

def drive_home(request, drive_pk):
    drive = Drive.objects.get(pk = drive_pk)
    message = ''
    if request.method == 'POST':
        hid = request.POST['hiddenValue']
        if hid == "post":
            print(hid)
            caption = request.POST['caption']
            image = request.FILES['imagepost']
            author = request.user

            post = Post1(drive = drive, author =author, photo = image, caption = caption)
            post.save()
            message = "Posted Succesfully"
        else:
            inc = int(request.POST['inc'])
            drive.count += inc
            drive.save()
            message = f"{inc} trees planted succesfully."
    context = {'drive' : drive, 'treeCount' : drive.count, 'message' : message}

    return render(request, 'users/drive_home.html', context)