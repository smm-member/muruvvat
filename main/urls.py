from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("",views.home_for_new,name="new_home"),
    path('quran/', views.main, name='main'),
    path('quran/<str:surai_slug>', views.SuraiViewDetail.as_view(), name='surai_detail'),
    path("account/", views.account_for_new,name="account"),
    path("accumulation/", views.accomulation_for_new,name="accomulation"),
    path("accumulation/<int:pk>", views.accomulation_details_for_new,name="accomulation_details"),
    path("application/", views.application_for_new,name="application"),
    path("charity/", views.charity_for_new,name="charity"),
    path("charity/<int:pk>", views.charity_details_for_new,name="charity_details"),
    path("check/<uidb64>", views.check_for_new,name="check"),
    path("contact/", views.contact_for_new,name="contact"),
    path("login/", views.login_for_new,name="login"),
    path("register/", views.register_for_new,name="register"),
    path("arizalar/", views.arizalar_for_new,name="arizalar"),
    path("logout/", views.logout_cr,name="logout")


]