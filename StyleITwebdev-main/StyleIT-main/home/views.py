from django.shortcuts import redirect, render , HttpResponse
from .models import ShopIT
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from ShopIT import settings

# Create your views here.
def index(request):
    shopIT = ShopIT.objects.all() 
    return render(request,"index.html",{'shopIT':shopIT})
    # return HttpResponse(" My self Piyush yadav")
def about(request):
    #return HttpResponse("zoro is lost again!!! ")
    return render ( request, 'about.html')

def add(request):
    return render ( request, 'add.html')

def contact(request):
    return render ( request, 'contact.html')
def base(request):
    return render ( request, 'base.html')
def cart(request):
    return render ( request, 'cart/cart_summary.html')

def recently(request):
    shopIT = ShopIT.objects.all()  
    return render ( request, 'recently.html', {'shopIT':shopIT})

def footer(request):
    return render ( request, 'footer.html')

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']
        # username = request.POST['username']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect('signin')

    return render ( request, 'auth/signin.html')

def sign_up(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        # username = request.POST['username']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username)>20:
            messages.error(request, "Username must be under 10 characters") 
            return redirect('home')  

        if password != confirmPassword:
            messages.error(request, "Passwords didn't match!") 
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')
        
        

        myuser = User.objects.create_user(username, email, password)
        # myuser.firstname=fname
        # myuser.lastname=lname
        myuser.is_active=False

        myuser.save()

        messages.success(request, "Your Account Has Been Created Successfully.")

        subject = "Welcome to STYLEIT "+myuser.username
        message = "Hello " + myuser.username + " !! \n" + "Welcome to STYLEIT!!\nThank you for visiting our website\nWe have sent u a confirmation email"
        from_email = settings.EMAIL_HOST_USER
        to_list =[myuser.email] 
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        current_site = get_current_site(request)
        email_subject = "Connfirm your email @ StyleIT login!!"
        message2 = render_to_string('auth/email_confirmation.html',{
            'name':myuser.username,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,   
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')


    return render( request, 'auth/sign_up.html')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'auth/activation_failed.html')

def admin(request):
    return HttpResponse('admin/.urls')
