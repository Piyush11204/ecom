from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
  
   path("", views.index, name='home'),
   path("home",views.index, name= 'home'),
   path("signin",views.signin, name= 'signin'),
   path("sign_up",views.sign_up, name= 'sign_up'), 
   path("signout",views.signout, name= 'signout'),
   path("about", views.about, name='about'),
   path("cart", views.cart, name='cart'),
   path("add", views.add, name='add'),
   path("contact", views.contact, name='contact'),
   path("recently", views.recently, name='recently'),
   path("activate/<uidb64>/<token>", views.activate, name='activate'),
   path("footer", views.footer, name='footer'),
   path("admin/", views.admin, name='admin'),
   ]