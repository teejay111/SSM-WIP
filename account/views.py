from django.shortcuts import render, redirect
import pyrebase
from store.models import Customer

config = {
    'apiKey': "AIzaSyATF5UzBoZ2ECUoChJuLG-ixn0jetUbLAI",
    'authDomain': "ecommerce-93ad0.firebaseapp.com",
    'databaseURL': "https://ecommerce-93ad0-default-rtdb.firebaseio.com/",
    'storageBucket': "gs://ecommerce-93ad0.appspot.com",
}

#config = {
#    'apiKey': "AIzaSyBueLXnniePhT5f95mmeu76_aIxB2xKBJs",
#    'authDomain': "",
#    'databaseURL': "",
#    'storageBucket': "",
#}

firebase = pyrebase.initialize_app(config)
firebaseAuth = firebase.auth()
database = firebase.database()


def login(request):
    try:
        if request.session['uid']:
            return redirect('/')
    except:
        return render(request, "account/login.html")


def register(request):
    try:
        if request.session['uid']:
            return redirect('/')
    except:
        return render(request, "account/signup.html")


def afterLogin(request):
    email = request.POST.get('email')
    pasw = request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user = firebaseAuth.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials!"
        return render(request, "account/login.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return redirect('/')


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "account/login.html")


def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('password')
    address = request.POST.get('address')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        firebaseAuth.create_user_with_email_and_password(email, passs)
        Customer.objects.create(
            email=email, name=name, address=address)
    except Exception as e:
        message = "Registration Failed"
        return render(request, "account/signup.html", {"message": message})

    return render(request, "account/login.html")
