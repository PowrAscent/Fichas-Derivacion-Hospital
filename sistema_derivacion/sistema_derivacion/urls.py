from django.contrib import admin
from django.urls import path
from gestion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path ('logout/', views.logout),
    path('', views.mostrarLogin),
    path('panel/', views.panel),
    path('registrar/', views.registrar),
    path('mostrar_registrar/', views.mostrar_registrar),
    path('modificar/<int:id>/', views.modificar),
    path('listar/', views.listar),

]
