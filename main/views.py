from django.shortcuts import render,redirect
from .models import *
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
import random
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import login,authenticate,logout
from django.views.generic import ListView
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
import threading
from django.core.mail import send_mail,EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()



def main(request):
    recently_surais = None
    surai = Surai.objects.all()

    if request.method=="POST":
        surai=[]
        for i in Surai.objects.all():
            if request.POST["q"] in (i.name_en or i.name_ar):
                surai.append(i)
    ls=[]
    while len(ls)<5:
        t=random.randint(1, 114)
        if t not in ls:
            ls.append(t)
    random_surah = Surai.objects.filter(number__in=ls)

    try:
        recently_surais = Surai.objects.filter(slug__in=request.session['recently_views'])
    except:
        pass
    context = {
        'surai':surai,
        'recently_surais':recently_surais,
        'random_surah':random_surah,

    }
    return render(request, 'index.html',context)

class SuraiViewDetail(View):
    def get(self,request,surai_slug): 
        pervous=None
        next_s = None
        surai = get_object_or_404(Surai, slug=surai_slug)
        try:
            pervous = Surai.objects.get(id=(int(surai.id)-1))
        except:
            pass
        try:
            next_s = Surai.objects.get(id=(int(surai.id)+1))
        except:
            pass
        try:
            if surai_slug in request.session['recently_views']:
                request.session['recently_views'].remove(surai_slug)

            request.session['recently_views'].insert(0,surai_slug)

            if len(request.session['recently_views'])>10:
                request.session['recently_views'].pop()
        except:
            request.session['recently_views'] = [surai_slug]
        request.session.modified = True
        
        context = {
            'surai':surai,
            'pervous':pervous,
            'next':next_s,
            }
        return render(request, 'details.html', context)

def check_users(my_user):
    if my_user.is_active==False:
        Profile.objects.get(user=my_user).delete()

def home_for_new(request):
    context = {
        "home":True,
    }
    return render(request,"new/index.html", context)

def account_for_new(request):
    if request.user.is_anonymous==True:
        return redirect("main:new_home")
    my_user = Profile.objects.get(user=request.user)
    if request.method == 'POST' and request.FILES['upload']:

        my_user.poster = request.FILES['upload']
        my_user.save()
        messages.success(request,"Yuklandi")

    context = {
        "account":True,
        "my_user":my_user
    }
    return render(request,"new/account.html", context)

def accomulation_for_new(request):
    if request.user.is_anonymous==True:
        return redirect("main:new_home")
    acc = Jamgarma.objects.all()

    context = {
        "accomulation":True,
        "jamgarmas":acc,
    }
    return render(request,"new/accumulation.html", context)

def accomulation_details_for_new(request,pk):
    ans = Jamgarma.objects.get(id=pk)
    if request.user.is_anonymous==True:
        return redirect("main:new_home")
    context = {
        "accomulation_details":True,
        "jamgarma":ans,
    }
    return render(request,"new/accumulation-details.html", context)


def application_for_new(request):
    if request.user.is_anonymous==True or Profile.objects.get(user=request.user).utype:
        return redirect("main:new_home")
        
    if request.method == "POST":
        idnumber = request.POST["idraqam"]
        idpersonalnumber = request.POST["shaxsiy_raqam"]

        cash = request.POST["miqdori"]
        date = request.POST["date"]
        card_number = request.POST["karta_raqam"]
        message = request.POST["message"]

        okk = Application.objects.create(
            id_card_number = idnumber,
            id_card_personal_number = idpersonalnumber,
            needed_cash = cash,
            deadline = date,
            card_number = card_number,
            desc = message,
            profile = Profile.objects.get(user=request.user),

        )
        okk.health_certificate = request.FILES['file-input']
        okk.save()

        messages.success(request,"Tasdiqlandi")
        return redirect("main:charity")
    context = {
        "application":True,
    }
    
    return render(request,"new/application.html", context)

def charity_for_new(request):
    if request.user.is_anonymous==True:
        return redirect("main:new_home")
    n=Application.objects.all().filter(is_it_for_print=True).filter(is_done=False)
    for i in n:
        i.ca_sh = i.needed_cash - i.payed
        i.save()
        if i.ca_sh <0: 
            i.is_done = True
            i.save()

    context = {
        "charity":True,
        "ans": Application.objects.all().filter(is_it_for_print=True).filter(is_done=False),
    }
    return render(request,"new/charity.html", context)


def charity_details_for_new(request,pk):
    if request.user.is_anonymous==True:
        return redirect("main:new_home")
    kot = Application.objects.get(id=pk)
    kot.ca_sh = kot.needed_cash - kot.payed
    if kot.ca_sh < 0:
        kot.is_done = True
    kot.save()
    context = {
        "charity_details":True,
        "ans":Application.objects.get(id=pk)
    }

    return render(request,"new/charity-details.html", context)


def contact_for_new(request):
    context = {
        "contact":True,
    }
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        theme = request.POST["subject"]
        message = request.POST["message"]

        Contact.objects.create(
            name=name,
            email=email,
            theme=theme,
            message=message
        ).save()

        messages.success(request,"Muvaffaqiyatli yuborildi.")
    return render(request,"new/contact.html", context)

def login_for_new(request):
    if request.user.is_anonymous==False:
        return redirect("main:account")
    context = {
        "login":True,
    }
    if request.method == "POST":
        phone = str(request.POST["phone"])
        ls="998"
        flag=False
        kk=3
        if phone[0]=="+": kk+=1
        for i in range(kk):
            if phone[i]!=ls[i]:
                if phone[i]!="+":
                    flag=True
                    break
        if flag: phone=ls+phone

        password = str(request.POST["password"])
        try:
            user = Profile.objects.get(user=User.objects.get(username=phone))
            if user.password==password:
                login(request,User.objects.get(username=phone),backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request,"Muvaffaqiyatli kirish.")
                return redirect("main:account")
            else:
                messages.error(request,"Noto'g'ri kod.")
        except:
            messages.error(request,"Noto'g'ri kod.")

    return render(request,"new/login.html", context)



def check_for_new(request,uidb64):
    if request.user.is_anonymous==False:
        return redirect("main:account")
    context = {
        "check":True,
    }
    try:
        kr_user=User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
        my_user=Profile.objects.get(user=kr_user)     
    except Exception as error:
        pass

    if request.method == "POST":
        code=int(request.POST["kod"])
        if my_user.code==code:
            my_user.user.is_active=True
            my_user.user.save()
            my_user.save()

            login(request,my_user.user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request,"Muvaffaqiyatli kirish.")

            return redirect("main:account")
        else:
            messages.error(request,"Noto'g'ri kod.")
            return redirect("main:check",uidb64=uidb64)

    return render(request,"new/check.html", context)




def register_for_new(request):
    if request.user.is_anonymous==False:
        return redirect("main:account")

    context = {
        "register":True,
    }
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        viloyat = request.POST["region"]
        tuman = request.POST["location"]
        location = viloyat + " " + tuman
        utype = request.POST["type"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        try:
            my_user = User.objects.create_user(phone,email,password1)
        except:
            messages.error(request,"Telefon raqam yoki email allaqachon ro'yxatdan o'tgan!")
            return render(request, 'new/index.html',context)
        
        my_user.is_active=False
        my_user.save()

        


        uid=urlsafe_base64_encode(force_bytes(my_user.pk))


        

        code = random.randint(100000,1000000)
        code_for_user = Profile.objects.get(user=my_user)
        code_for_user.password=password1
        code_for_user.name=name
        code_for_user.phone=phone
        code_for_user.adress=location
        code_for_user.utype=utype
        code_for_user.code=code


        code_for_user.save()
        

        email_message = EmailMessage(
            "Elektron pochtangizni tasdiqlang.",
            str(code),
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )

        email_message.content_subtype = "html"


        threading.Timer(600, check_users,[my_user]).start()

        EmailThread(email_message).start()
        messages.success(request,"Emailingizga ko'd yuborildi, ko'dni kiriting!")
        
        return redirect("main:check",uidb64=uid)

    return render(request,"new/register.html", context)

def arizalar_for_new(request):
    if request.user.is_staff==False:
        return redirect("main:new_home")

    context={
        "application":Application.objects.all().filter(is_it_for_print=False)
    } 
    try:
        id_ = request.GET["id"]
        sec_ = request.GET["sec"]
        app = Application.objects.get(id=id_)
        if sec_ == "accept":
            app.is_it_for_print=True
            app.save()
            messages.success(request,"Tasdiqlanndi.")
        else:
            app.delete()
            messages.success(request,"Ochirildi.")

    except Exception as error: pass

    return render(request,"new/arizalar.html",context)
def logout_cr(request):
    logout(request)
    messages.success(request,"Muvaffaqiyatli chiqdiz.")

    return redirect("main:new_home")