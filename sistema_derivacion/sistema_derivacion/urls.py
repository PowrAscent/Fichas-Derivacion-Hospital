from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path ('logout/', views.logout),
    path('', views.mostrarLogin)

]
